# Codexコマンド実行ルール

本ディレクトリの`.rules`は、Codexの**コマンド実行時の承認判断**を補助します。開発要件そのものはルート`AGENTS.md`と`docs/10-codex-instructions.md`を参照してください。

## 収録ルール

| ファイル | 主な制御 |
|---|---|
| `10-git-worktree.rules` | Worktreeの直接変更禁止、Git履歴破壊禁止、push・復元操作の承認 |
| `20-github-release.rules` | PRマージ・Issue終了の承認、リポジトリ/Release/Secretの危険操作禁止 |
| `30-destructive-local.rules` | 強制・再帰削除の禁止、実機データ削除・sudoの承認 |

判定値は`forbidden`（禁止）、`prompt`（承認要求）を利用し、無条件の`allow`は設定していません。

## 設置と有効化

1. **リポジトリルート**の`.codex/rules/`へこのファイル群を配置します。
2. Worktree保存先は人間が事前承認します。承認済み保存先の各Worktreeは管理Skillが正確なパスだけをTrustedに登録し、Codexが確認します。人間による毎回の再承認は不要です。未承認パスを勝手にTrustedにしません。
3. Codexが新Worktreeを開いてルールを読み込みます。Worktreeごとに実行時の適用確認が必要です。
4. `worktree-management` Skill本体は**別途導入が必要**です。未導入ならTASK-036はBLOCKEDとし、直接`git worktree add/remove`へ回避しません。

## 動作確認（Codex CLIが利用可能な環境）

ルールは実行されるコマンドの**引数プレフィックス**で判定されます。次は判定だけを行い、実際の削除・push・公開は行いません。

```bash
codex execpolicy check --pretty --rules .codex/rules/10-git-worktree.rules -- git worktree add ../tmp
codex execpolicy check --pretty --rules .codex/rules/10-git-worktree.rules -- git worktree list
codex execpolicy check --pretty --rules .codex/rules/10-git-worktree.rules -- git push origin task/001
codex execpolicy check --pretty --rules .codex/rules/20-github-release.rules -- gh pr merge 12 --squash
codex execpolicy check --pretty --rules .codex/rules/20-github-release.rules -- gh release create v1.0.0
codex execpolicy check --pretty --rules .codex/rules/30-destructive-local.rules -- rm -rf ../worktrees/task-001
```

期待する判定は、順に`forbidden`、ルール非該当、`prompt`、`prompt`、`forbidden`、`forbidden`です。**CIや実行環境でもルールが効くこと**を別途確かめてください。

全ルールを同時に指定したい場合、`--rules`を繰り返して指定します。

```bash
codex execpolicy check --pretty \
  --rules .codex/rules/10-git-worktree.rules \
  --rules .codex/rules/20-github-release.rules \
  --rules .codex/rules/30-destructive-local.rules \
  -- git push origin main
```

## これだけでは強制できないこと

- `.rules`は**サンドボックス外でのコマンド実行承認**のための機能です。ファイル編集、SDK内部動作、HTTPリクエスト本文を監査する仕組みではありません。
- `git -C <path> worktree ...`や、引数順の異なる`git push`、任意のスクリプト・別ツール経由など、**すべての操作形態を網羅するものではありません**。管理者による権限制約・GitHub Branch Protection/Rulesets・CIを併用してください。
- `git worktree`操作がSkill内部のスクリプトからサブプロセスで呼び出される場合、Codexのコマンドルールが内部コマンドを完全に検査するとは限りません。Skillのコードレビューと許可済みパス制限が必要です。
- P0 PoC/ADR承認、最大2タスク制限、個人情報送信防止、WorktreeのTrusted設定は**`.rules`だけでは検証・保証できません**。AGENTS.md、GitHub Issues、CI、ユーザー承認、実機検証で担保します。
- Codexの承認ポリシー・サンドボックス設定によっては`prompt`が期待どおり発火しない場合があります。ルールの`check`結果だけで動作を保証したとは扱わず、実環境で確認してください。

公式資料：https://developers.openai.com/codex/rules/
