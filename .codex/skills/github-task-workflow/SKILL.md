---
name: github-task-workflow
description: Android記事要約アプリのGitHub IssuesをTask管理の正本として運用する。TASKの起票、依存・承認ゲートの確認、READY判定、最大2タスクの並列制御、PR紐付け、DoD更新、完了報告が必要なときに使用する。
---

# GitHub Issue駆動ワークフロー

Task管理の**唯一の正本はGitHub Issues**。仕様・要件・ADRの正本はリポジトリ`docs/`。Taskの状態を別Markdownへ複製しない。

## 着手前

1. `AGENTS.md`と`docs/09-implementation-plan.md`、`docs/10-codex-instructions.md`を読む。
2. `gh auth status`、`gh repo view`で利用可能性を確認。権限がなければIssue案を生成してBLOCKEDを報告し、作成済みと偽らない。
3. Task IDで既存Issueを検索し、重複作成しない。例: `gh issue list --state all --search 'TASK-007'`。
4. [issue-checklist.md](references/issue-checklist.md)に従い、FR/NFR/ARCH/AC/NAC、PoC・ADR・先行Issue、変更範囲、DoDを確認する。
5. 本実装（PLAN-004以降）なら、全P0 PoC・ADR-001〜007・MG-02a/02bの**人間の承認証跡**を確認する。不明または未達ならBLOCKED。
6. 現在の稼働タスク数をIssue/Projectsの正本で数える。**最大2件**（PoCを含む）。同じファイル・Portを同時変更するTaskは並列化しない。
7. Worktreeの作成・Trustは`worktree-management` Skillへ委譲する。

## 起票・更新

- `.github/ISSUE_TEMPLATE/implementation-task.md`を原型にする。タイトルは`[TASK-XXX] ...`。
- 状態はGitHub Projectフィールドまたは状態ラベル（TODO/READY/IN_PROGRESS/BLOCKED/IN_REVIEW/DONE）に統一し、フィールドが未整備なら人間へルールを確認する。
- 一度に作業するTaskは1件。Taskスコープ外の変更は新規Issue案に分離する。
- PRに`TASK-XXX`・Issueリンク・対象AC・テスト証跡を明記する。PR作成やIssue更新は必要な権限・承認の範囲内で行う。
- 自動テストPASSだけでMG承認やPoC合格を宣言しない。

## 完了判定

- コード・テスト・ドキュメント・CI結果・レビュー・必要MGの承認記録を確認する。
- `NOT_RUN`、`BLOCKED`をPASSへ書き換えない。未完了なら`IN_REVIEW`や`BLOCKED`のまま。
- Task完了後は`release-readiness`ではなく、通常タスクの報告として`docs/10-codex-instructions.md §9`の書式を使う。

詳しいGitHub項目と状態の扱いは[issue-checklist.md](references/issue-checklist.md)を参照する。
