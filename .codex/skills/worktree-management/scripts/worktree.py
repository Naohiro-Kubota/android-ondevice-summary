#!/usr/bin/env python3
"""Fail-closed Worktree management. Python >=3.11, POSIX, stdlib only."""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import tomllib
import fcntl
from contextlib import contextmanager
from pathlib import Path


class Blocked(Exception):
    pass


def canonical(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def command(argv: list[str], *, cwd: Path | None = None, checked=True):
    try:
        result = subprocess.run(argv, text=True, capture_output=True, cwd=cwd, check=False)
    except FileNotFoundError as e:
        raise Blocked(f"コマンドが見つかりません: {argv[0]}") from e
    if checked and result.returncode:
        raise Blocked(f"実行失敗: {argv[0]} {argv[1] if len(argv)>1 else ''}: {result.stderr.strip()}")
    return result


def repository(raw: str) -> Path:
    root = canonical(raw)
    reported = command(["git", "-C", str(root), "rev-parse", "--show-toplevel"]).stdout.strip()
    if root != canonical(reported):
        raise Blocked("--repoにはGitリポジトリルートを指定してください")
    return root


def worktree_root(repo: Path, raw: str) -> Path:
    raw_path = Path(raw).expanduser().absolute()
    if raw_path.is_symlink():
        raise Blocked("シンボリックリンクの保存先を利用できません")
    root = raw_path.resolve()
    if not root.is_dir() or root == repo or repo in root.parents or root in repo.parents:
        raise Blocked("保存先は、作成済みのリポジトリ外ディレクトリを指定してください")
    info = root.stat()
    if info.st_uid != os.getuid() or info.st_mode & stat.S_IWOTH:
        raise Blocked("保存先は現在ユーザー所有かつworld-writableでないことが必要です")
    return root


def config_home() -> Path:
    return canonical(os.environ.get("CODEX_HOME", Path.home() / ".codex"))


@contextmanager
def configuration_lock():
    home = config_home()
    home.mkdir(parents=True, exist_ok=True)
    lock = home / ".worktree-management.lock"
    if lock.is_symlink():
        raise Blocked("ロックファイルのシンボリックリンクは禁止です")
    with lock.open("a+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def atomic_write(path: Path, data: bytes, mode: int = 0o600):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise Blocked("シンボリックリンクを上書きできません")
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".worktree-management-")
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "wb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.lexists(tmp):
            os.unlink(tmp)


def approved_file() -> Path:
    return config_home() / "worktree-management" / "approved-roots.json"


def approved_entries() -> list[dict[str, str]]:
    path = approved_file()
    if not path.exists():
        return []
    if path.is_symlink():
        raise Blocked("承認台帳のシンボリックリンクは禁止です")
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Blocked("承認台帳が読み取れません") from e
    entries = obj.get("entries") if isinstance(obj, dict) else None
    if not isinstance(entries, list) or not all(isinstance(x, dict) and set(x) == {"repo", "root"} for x in entries):
        raise Blocked("承認台帳の形式が不正です")
    return entries


def ensure_approved(repo: Path, root: Path):
    if {"repo": str(repo), "root": str(root)} not in approved_entries():
        raise Blocked("保存先が人間により承認されていません。authorize-rootを人間が実行してください")


def user_config() -> dict:
    path = config_home() / "config.toml"
    if path.is_symlink():
        raise Blocked("config.tomlのシンボリックリンクは禁止です")
    if not path.exists():
        return {}
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as e:
        raise Blocked("Codexのユーザー設定に構文エラーがあります。変更しません") from e


def trust_level(path: Path) -> str | None:
    projects = user_config().get("projects", {})
    value = projects.get(str(path)) if isinstance(projects, dict) else None
    return value.get("trust_level") if isinstance(value, dict) else None


def add_exact_trust(path: Path):
    config = config_home() / "config.toml"
    with configuration_lock():
        projects = user_config().get("projects", {})
        if not isinstance(projects, dict):
            raise Blocked("Codex設定のprojectsが不正です")
        if str(path) in projects:
            if trust_level(path) == "trusted":
                return
            raise Blocked("既存の非Trusted設定があります。人間による変更が必要です")
        raw = config.read_bytes() if config.exists() else b""
        new_section = ("\n\n[projects." + json.dumps(str(path), ensure_ascii=False) + ']\ntrust_level = "trusted"\n').encode()
        new_value = raw + new_section
        try:
            tomllib.loads(new_value.decode())
        except (UnicodeError, tomllib.TOMLDecodeError) as e:
            raise Blocked("Trustedの追記後に設定が不正となるため中止") from e
        mode = stat.S_IMODE(config.stat().st_mode) if config.exists() else 0o600
        atomic_write(config, new_value, mode)


def list_worktrees(repo: Path) -> dict[str, dict[str, str]]:
    lines = command(["git", "-C", str(repo), "worktree", "list", "--porcelain"]).stdout.splitlines() + [""]
    found: dict[str, dict[str, str]] = {}
    state: dict[str, str] = {}
    for line in lines:
        if not line:
            if "worktree" in state:
                found[str(canonical(state["worktree"]))] = state
            state = {}
        elif " " in line:
            k, v = line.split(" ", 1)
            state[k] = v
        else:
            state[line] = "true"
    return found


def authorize(args):
    repo, root = repository(args.repo), None
    root = worktree_root(repo, args.root)
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise Blocked("authorize-rootは人間の対話端末からのみ許可します。Codexは代行不可")
    confirm = f"AUTHORIZE {root}"
    print(f"対象リポジトリ: {repo}\nWorktree保存先: {root}")
    if input(f"人間が承認する場合だけ正確に入力: {confirm}\n> ") != confirm:
        raise Blocked("人間の承認文字列が一致しません")
    with configuration_lock():
        entries = approved_entries()
        item = {"repo": str(repo), "root": str(root)}
        if item not in entries:
            entries.append(item)
            atomic_write(approved_file(), (json.dumps({"version": 1, "entries": entries}, indent=2, ensure_ascii=False) + "\n").encode())
    print("PASS: 保存先の人間承認を記録しました")


def create(args):
    repo = repository(args.repo)
    root = worktree_root(repo, args.root)
    ensure_approved(repo, root)
    if not re.fullmatch(r"[a-z][a-z0-9-]{2,79}", args.name):
        raise Blocked("Worktree名は小文字英数字とハイフン、3〜80文字")
    branch = args.branch
    if not branch.startswith(("task/", "poc/")) or command(["git", "check-ref-format", "--branch", branch], checked=False).returncode:
        raise Blocked("ブランチはgitで有効なtask/...かpoc/...にしてください")
    target = root / args.name
    if os.path.lexists(target):
        raise Blocked("同名Worktreeが存在します。上書き禁止")
    if command(["git", "-C", str(repo), "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"], checked=False).returncode == 0:
        raise Blocked("ブランチが存在します。上書き禁止")
    command(["git", "-C", str(repo), "worktree", "add", "-b", branch, str(target), "HEAD"])
    print(f"Created: {target}")
    try:
        add_exact_trust(target)
    except Blocked as e:
        raise Blocked(f"Worktree作成済みですがTrusted登録に失敗: {e}。自動削除しません") from e
    print("PASS: Worktreeの正確なパスをTrusted登録。Codexの再起動と実効確認が必要")


def inspect(args):
    repo = repository(args.repo)
    target = canonical(args.path) if args.path else repo
    active = str(target) in list_worktrees(repo)
    rules = target / ".codex/rules"
    report = {
        "path": str(target),
        "git_worktree_registered": active,
        "trust_config": trust_level(target) or "NOT_SET",
        "AGENTS_present": (target / "AGENTS.md").is_file(),
        "rules_present": rules.is_dir() and any(rules.glob("*.rules")),
        "skill_present": (target / ".codex/skills/worktree-management/SKILL.md").is_file(),
        "runtime_rules_effective": "NOT_RUN (requires Codex session validation)",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not (report["git_worktree_registered"] and report["trust_config"] == "trusted" and report["AGENTS_present"] and report["rules_present"] and report["skill_present"]):
        raise Blocked("必須の静的設定が不足。変更作業を開始しないでください")
    print("PASS: 静的確認のみ。新Codexセッションでルール適用を確認してください")


def remove(args):
    repo, target = repository(args.repo), canonical(args.path)
    current = list_worktrees(repo).get(str(target))
    if target == repo or current is None:
        raise Blocked("登録済みサブWorktreeではありません")
    root = worktree_root(repo, str(target.parent))
    ensure_approved(repo, root)
    if not re.fullmatch(r"[a-z][a-z0-9-]{2,79}", target.name):
        raise Blocked("Worktree名が承認済み形式ではありません")
    branch_ref = current.get("branch", "")
    if not branch_ref.startswith("refs/heads/"):
        raise Blocked("対象ブランチを特定できません")
    branch = branch_ref[len("refs/heads/"):]
    if command(["git", "-C", str(target), "status", "--porcelain", "--untracked-files=all"]).stdout.strip():
        raise Blocked("未コミットまたは未追跡の変更が残っています。削除しません")
    if args.merged_into:
        status = command(["git", "-C", str(repo), "merge-base", "--is-ancestor", branch, args.merged_into], checked=False)
        if status.returncode:
            raise Blocked("統合先にマージ済みと確認できません。Squashなら--merged-prを利用")
    else:
        result = command(["gh", "pr", "view", str(args.merged_pr), "--json", "state,mergedAt,headRefName,headRefOid"], cwd=repo)
        try:
            data = json.loads(result.stdout)
        except ValueError as e:
            raise Blocked("PR状態JSONが不正です") from e
        if data.get("state") != "MERGED" or not data.get("mergedAt") or data.get("headRefName") != branch:
            raise Blocked("対象ブランチのPRマージ済みを確認できません")
        local_head = command(["git", "-C", str(target), "rev-parse", "HEAD"]).stdout.strip()
        if data.get("headRefOid") != local_head:
            raise Blocked("PRマージ時点とWorktreeのHEADが異なります。未統合変更がないか確認してください")
    command(["git", "-C", str(repo), "worktree", "remove", str(target)])
    print("PASS: Worktree削除。ブランチとユーザーTrustedエントリは削除していません")


def main():
    if sys.version_info < (3, 11):
        raise Blocked("Python 3.11以上が必要です（追加依存なし）")
    parser = argparse.ArgumentParser(description="承認済みWorktree保存先の管理")
    sub = parser.add_subparsers(dest="action", required=True)
    for name, func in (("authorize-root", authorize), ("create", create), ("inspect", inspect), ("remove", remove)):
        p = sub.add_parser(name)
        p.add_argument("--repo", required=True)
        if name in ("authorize-root", "create"):
            p.add_argument("--root", required=True)
        if name == "create":
            p.add_argument("--name", required=True)
            p.add_argument("--branch", required=True)
        if name in ("inspect", "remove"):
            p.add_argument("--path", required=name == "remove")
        if name == "remove":
            g = p.add_mutually_exclusive_group(required=True)
            g.add_argument("--merged-into")
            g.add_argument("--merged-pr", type=int)
        p.set_defaults(func=func)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except Blocked as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        sys.exit(2)
