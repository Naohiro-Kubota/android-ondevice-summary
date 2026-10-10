# Androidオンデバイス記事要約アプリ — 要求・設計ベースライン v2.7

**文書作成日:** 2026-10-10  
**状況:** 16ステップの要求・論理設計を完了。実装・PoC・ADR承認は未実施。  
**言語:** 日本語（ソース上の識別子・API名は英語を使用）

## 文書一覧（10本）

1. [01-product-overview.md](docs/01-product-overview.md) — プロダクト概要・スコープ・前提・意思決定
2. [02-user-requirements.md](docs/02-user-requirements.md) — ユーザーストーリー・ユースケース・制約・不変条件
3. [03-functional-requirements.md](docs/03-functional-requirements.md) — FR、ERR、ACの正本
4. [04-nonfunctional-requirements.md](docs/04-nonfunctional-requirements.md) — NFR、NACの正本
5. [05-screens-and-flows.md](docs/05-screens-and-flows.md) — SCR、PF、画面状態遷移
6. [06-architecture.md](docs/06-architecture.md) — ARCH、ポート／アダプター、ライフサイクル
7. [07-data-design.md](docs/07-data-design.md) — DATA、保持・破棄・外部送信
8. [08-test-strategy.md](docs/08-test-strategy.md) — TEST、TV、リリースGATE、証跡
9. [09-implementation-plan.md](docs/09-implementation-plan.md) — PLAN、TASK、MG、依存関係
10. [10-codex-instructions.md](docs/10-codex-instructions.md) — COD、GitHub Issues、Worktree、CI、報告

## Codex運用ファイル

- [AGENTS.md](AGENTS.md) — 常時遵守する短い開発Policy
- [ADRテンプレート](docs/adr/ADR-TEMPLATE.md) — 提案・証跡・人間の承認
- [GitHub Issueテンプレート](.github/ISSUE_TEMPLATE/implementation-task.md) — タスク正本
- [マイルストーン承認テンプレート](docs/MILESTONE-APPROVAL-TEMPLATE.md) — MG承認証跡
- [検証結果テンプレート](docs/POC-REPORT-TEMPLATE.md) — TV/PoC結果
- [追跡可能性レポート](docs/TRACEABILITY.md) — IDの充足と関連

## 重要な開始ゲート

**PLAN-004以降の本実装は、P0 PoCの合格（MG-02a）とADR-001〜007の人間による採用承認（MG-02b）の両方を満たすまで禁止。** PLAN-001の基盤・FakeおよびPLAN-002の検証コードは例外として着手可能。

並列実行は最大2タスク、異なるWorktreeを使用。Task状態の正本はGitHub Issues、要件とADRの正本はこのリポジトリの文書。コードは未作成。

## 原典と再構成について

この成果物は会話で確定した要求を統合し、連番IDの完全なレジストリを作成したベースラインです。初期ステップの全ID原文が会話の直近メッセージに再掲されていない箇所は、合意済みの振る舞いから説明文を整合的に**再構成**しています。したがって、過去の個別版ファイルがある場合はMG-01で原文との差分照合を行い、差分を承認してください。IDの存在・重複・形式・参照先は自動検査済みでも、過去文言との逐語一致まで証明するものではありません。

## 外部仕様（参照日: 2026-10-10）

- [Google Play 新しい個人アカウントのテスト要件](https://support.google.com/googleplay/android-developer/answer/14151465?hl=ja)
- [ML Kit GenAI Summarization](https://developers.google.com/ml-kit/genai/summarization/android?hl=ja)
- [ML Kit Translation](https://developers.google.com/ml-kit/language/translation/android?hl=ja)
- [Codex 設定リファレンス: project trust](https://developers.openai.com/ja-JP/docs/config-file/config-reference)

最新のSDK、Google Play審査条件、法令・プライバシー要件、依存バージョンはPoCまたは公開直前に再確認します。
