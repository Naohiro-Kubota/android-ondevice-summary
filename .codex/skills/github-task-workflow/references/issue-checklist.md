# Issueの確認項目

## TASK作成

- **Issueを作る前に重複検索する**。GitHub Issuesが正本であり、Taskの進捗コピーを`docs/tasks`へ作らない。
- Task ID、PLAN ID、目的・対象外、優先度、変更予想ファイル、先行Issue・ADR・TV、FR/NFR/ARCH/AC/NACを含める。
- 先行Issueはclosedだけでは十分でない。DoD・承認が記録されているか確認する。
- `Proposed`なADRは採用承認ではない。全P0と主要ADRの一括ゲート（MG-02a/02b）を通す。
- `IN_PROGRESS`中のIssueを探し、自己のTask含め**2件以下**。API/権限不足で全件確認できない場合は安全側に判断し人間へ確認する。

## GitHub CLI例（読み取り）

```bash
gh auth status
gh repo view --json nameWithOwner
gh issue list --state all --limit 200 --search 'TASK-007'
gh issue view 123 --json number,title,state,labels,body,url
```

ラベル名・ProjectフィールドはGitHubの実設定に合わせる。ローカルで特定のラベルが存在すると仮定しない。更新コマンドやPR作成はユーザー承認・権限内で実施する。

## 完了報告

1. Issue URL / PR URL / Branch・Worktree
2. 実装差分と要件・ACの対応
3. 実施テストのコマンドと実測結果。PASS/FAIL/BLOCKED/NOT_RUN
4. Emulator、Pixel、Firebase、40記事品質評価のうち適用したものと未実施
5. Security・Privacy上の影響
6. 残課題・人間承認待ち、MG適用有無
7. 次にREADYにできるTask
