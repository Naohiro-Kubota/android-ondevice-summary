#!/usr/bin/env python3
"""Run only against disposable local Git repos and a temporary Codex HOME."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SELF = Path(__file__).with_name("worktree.py")


def cmd(args, env=None, expected=0):
    p = subprocess.run(args, text=True, capture_output=True, env=env)
    if p.returncode != expected:
        raise AssertionError(f"expected={expected} actual={p.returncode}\n{p.stdout}\n{p.stderr}")
    return p


def main():
    with tempfile.TemporaryDirectory(prefix="codex-worktree-selftest-") as dirname:
        base = Path(dirname).resolve()
        repo, target_root, codex = base / "repo", base / "worktrees", base / "codex-home"
        repo.mkdir(); target_root.mkdir(); codex.mkdir()
        env = dict(os.environ, CODEX_HOME=str(codex))
        cmd(["git", "init", "-b", "main", str(repo)])
        cmd(["git", "-C", str(repo), "config", "user.email", "local-test@example.invalid"])
        cmd(["git", "-C", str(repo), "config", "user.name", "Local Test"])
        (repo / ".codex/rules").mkdir(parents=True)
        (repo / ".codex/skills/worktree-management").mkdir(parents=True)
        (repo / "AGENTS.md").write_text("# fixture\n")
        (repo / ".codex/rules/sample.rules").write_text("# fixture\n")
        (repo / ".codex/skills/worktree-management/SKILL.md").write_text("---\nname: worktree-management\ndescription: Test\n---\n")
        cmd(["git", "-C", str(repo), "add", "."])
        cmd(["git", "-C", str(repo), "commit", "-m", "fixture"])
        common = [sys.executable, str(SELF)]
        # Explicit user authorization cannot be forged by non-interactive calls.
        cmd(common + ["authorize-root", "--repo", str(repo), "--root", str(target_root)], env, expected=2)
        cmd(common + ["create", "--repo", str(repo), "--root", str(target_root), "--name", "task-001-setup", "--branch", "task/001-setup"], env, expected=2)
        (codex / "worktree-management").mkdir()
        (codex / "worktree-management/approved-roots.json").write_text(json.dumps({"version": 1, "entries": [{"repo": str(repo), "root": str(target_root)}]}))
        cmd(common + ["create", "--repo", str(repo), "--root", str(target_root), "--name", "task-001-setup", "--branch", "task/001-setup"], env)
        config = (codex / "config.toml").read_text()
        assert "trust_level" in config and str(target_root / "task-001-setup") in config
        cmd(common + ["inspect", "--repo", str(repo), "--path", str(target_root / "task-001-setup")], env)
        cmd(common + ["create", "--repo", str(repo), "--root", str(target_root), "--name", "task-001-setup", "--branch", "task/001-setup"], env, expected=2)
        dirty = target_root / "task-001-setup" / "untracked.txt"
        dirty.write_text("keep")
        cmd(common + ["remove", "--repo", str(repo), "--path", str(dirty.parent), "--merged-into", "main"], env, expected=2)
        dirty.unlink()
        cmd(common + ["remove", "--repo", str(repo), "--path", str(target_root / "task-001-setup"), "--merged-into", "main"], env)
        assert not (target_root / "task-001-setup").exists()
    print("PASS: unapproved/TTY refusal, create, exact trust, inspect, duplicate refusal, dirty refusal, merged-only removal")


if __name__ == "__main__":
    main()
