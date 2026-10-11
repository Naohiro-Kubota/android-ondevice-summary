# Trusted・承認済み保存先の運用

## 1. 人間による保存先の承認（対話必須）

保存先は**作業リポジトリの外**に用意する。例: `/Users/owner/projects/worktrees`。

```bash
mkdir -p ../worktrees
python3 .codex/skills/worktree-management/scripts/worktree.py authorize-root \
  --repo . --root ../worktrees
```

スクリプトが表示する絶対パスを確認し、要求された確認文字列を**人間が端末へ直接入力**する。CodexにTTYや承認文字列を渡して自動実行させない。

保存先の承認記録はユーザーごとの`$CODEX_HOME/worktree-management/approved-roots.json`（通常`~/.codex/`以下）に作成する。リポジトリへコミットしない。

## 2. Trustedの登録

作成スクリプトは、許可済み格納先に作成した正確なWorktreeパスを`$CODEX_HOME/config.toml`の `[projects."<worktreeの絶対パス>"]` に追記し`trust_level = "trusted"`を設定する。

- 既存設定を削除・置換しない。競合する既存設定があれば停止する。
- **親パスや任意のユーザーディレクトリを一括Trustedにしない。**
- `config.toml`に構文エラーがある場合は変更しない。
- この設定はユーザー固有。保存先の人間承認は初回のみで、Worktreeごとの再承認は不要。Codexが各Worktreeを開いて設定の読込とルールの実効性を確認する。

## 3. 確認

```bash
python3 .codex/skills/worktree-management/scripts/worktree.py inspect \
  --repo . --path ../worktrees/task-001-bootstrap
```

- コマンドの出力がTrusted設定の存在を示しても、**Codex実行時のルール適用を完全保証はできない**。Codexセッションで確認できない場合は作業を開始しない。
- `.codex/rules`の内容は、Worktreeに追跡・配置されたファイルを使用する。
- Codex CLIがある場合は`codex execpolicy check`で、禁止操作が実行されないことを**判定のみ**確認する（削除・pushの実行はしない）。
- `gh`認証・権限は別に確認する。

## 4. 失敗時

Skill未読込、Trusted未確認、ルール不適用、Python不足、Codexバージョンの仕様相違、既存設定との競合は`BLOCKED`。無断で直接Worktreeコマンドへ切り替えず人間へ報告する。
