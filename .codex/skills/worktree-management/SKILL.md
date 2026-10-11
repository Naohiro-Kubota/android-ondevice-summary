---
name: worktree-management
description: CodexのGit Worktreeを安全に作成・検査・削除する。TASK単位の並列作業、Trusted状態の確認、未承認パスの信頼登録防止、Worktreeの安全な後片付けが必要なときに使用する。
---

# Worktree管理

`AGENTS.md`、`docs/10-codex-instructions.md`、`.codex/rules/`に従う。**Worktreeの変更は必ずこのSkillのスクリプトを使用する**。直接の`git worktree add/remove`や、独自の回避スクリプトは禁止。

## 前提

- Python **3.11以上**、Git、承認済みのGitリポジトリ。スクリプトはPython標準ライブラリのみ使用。
- GitHub IssuesのTaskがREADYで、並列稼働数が**2未満**、変更対象の競合がないこと。
- Worktree格納先を利用者が事前承認していること。**Codex自身による承認操作の代行は禁止**。
- Codexによる実操作の前に、リポジトリがTrustedとして扱われ、Skillの読込・`.codex/rules`の適用を確認する。

## 操作手順

1. Read-onlyの事前確認: `python3 .codex/skills/worktree-management/scripts/worktree.py inspect --repo .`
2. 未承認の格納先は、**人間が対話端末から**`authorize-root`を実行する。例と注意事項は[trust-workflow.md](references/trust-workflow.md)を参照。
3. 作成: `python3 .codex/skills/worktree-management/scripts/worktree.py create --repo . --root ../worktrees --name task-001-bootstrap --branch task/001-bootstrap`
4. 検査: `python3 .codex/skills/worktree-management/scripts/worktree.py inspect --repo . --path ../worktrees/task-001-bootstrap`
5. 新しいWorktreeでCodexを再起動・開き直し、Trusted状態・ルールの実効性を確認してから作業する。構成ファイルの存在だけで「実効確認済み」としない。
6. マージ後、未コミット/未追跡成果物が無いこと、指定した統合証跡が確認できることを確かめ、`remove`を実行する。

削除（通常マージ）:

```bash
python3 .codex/skills/worktree-management/scripts/worktree.py remove \
  --repo . --path ../worktrees/task-001-bootstrap --merged-into origin/main
```

Squash mergeの場合は`--merged-pr <PR番号>`で**`gh`からMergedを検証できるときのみ**削除する。統合判定不能ならBLOCKEDとし、強制削除はしない。

## 安全性

- 承認済み格納先の**直下**しか作成できず、既存ファイル・既存ブランチは上書きしない。
- `authorize-root`は対話端末でしか動作せず、Codexが代行・模擬承認してはならない。
- 承認済み格納先に限り、作成された**正確なWorktreeパス**をユーザーレベルのCodex trust設定へ登録する。親ディレクトリ全体をTrustedにしない。
- `create`後にTrusted登録に失敗してもWorktreeを勝手に削除しない。理由と後始末を人間へ報告する。
- `git status`が汚れている、統合証跡がない、格納先が許可範囲外の場合、削除は拒否する。
- `git -C ...`などで`.codex/rules`の直接Worktree変更禁止を迂回しない。必ず本スクリプトから操作する。

本Skillのコマンドは**Worktree運用だけ**を支援する。GitHub Issue状態やMG/ADR承認の判定は`github-task-workflow`と`poc-adr-governance`に委ねる。
