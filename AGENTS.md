# 開発ポリシー

## 要件と承認
- `docs/`のFR・NFR・AC・NAC・ARCHと承認済みADRに従う。MUST要件・技術選定を独断で変更しない。
- **P0 PoCすべての合格とADR-001〜007すべての人間承認（MG-02a/02b）の前に、PLAN-004以降の本実装へ着手しない。** Fake・基盤骨格・検証専用PoCは例外。
- ADRは提案段階では`Proposed`。人間の承認なく`Accepted`に変更しない。

## TaskとWorktree
- **GitHub IssuesをTask状態・依存・担当・PRの正本**とし、着手前にTask/要件/DoDを確認する。
- 独立タスクだけ**最大2件**まで並列実行する。変更タスクには原則専用Worktreeを使う。
- Worktreeの作成・管理・削除は承認済み`worktree-management` Skill経由とする。Skill未導入、Trusted未確認、`.codex/rules`未適用なら着手せずBLOCKEDと報告する。未承認パスを勝手にTrustedにしない。

## 実装と検証
- Kotlin、Jetpack Compose、Single Activity、単一`:app`、手動DI、Port/Adapterの依存方向を守る。
- 記事のURL・HTML・本文・AI入出力・要約結果を永続化せず、Firebaseに送信しない。診断URLは安全判定したホスト名だけ。アプリ独自相関IDの送信禁止。
- 実装とテストを同じTaskで更新し、PR必須CIが合格するまでマージしない。未実施テストをPASSと報告しない。
- 主要マイルストーンとRelease公開は人間の承認を必要とする。

詳細: `docs/10-codex-instructions.md`、実装計画: `docs/09-implementation-plan.md`。
