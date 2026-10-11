---
name: release-readiness
description: Android記事要約アプリのマイルストーンとRelease候補の受入可否を監査する。CI・Pixel 9 Pro XL・日英各20記事の人間レビュー・Firebase 3製品の送信検証・Google Play公開要件・MG承認の照合時に使用する。
---

# Release候補・マイルストーン判定

リリース・公開操作は**人間の最終承認後のみ**。Codexは判定資料を作り、承認待ちを`PASS`にしない。

## 手順

1. `docs/08-test-strategy.md`、`docs/09-implementation-plan.md`、`docs/10-codex-instructions.md`からGATE-01〜12とMG-01〜06、対象Issueを取得。
2. `docs/MILESTONE-APPROVAL-TEMPLATE.md`に従い、承認者・日時・対象コミット・証跡を集計。Issueに根拠リンクを登録。
3. 実施テストをPASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLEで整理。**証跡不在はPASSではない**。
4. Release候補ではPR CI、Emulator網羅的テスト、Pixel 9 Pro XL実機、日英各20記事の**人間**品質レビュー、Release候補固有のFirebase 3製品の実送信検証を必須とする。
5. P0・Security・Privacy・AI資源解放の重大未解決問題、MUST未達、主要ADR未承認があればSTOP。
6. Google Playアカウントは**未作成・不明**。実際のアカウント条件を確認する。必要なクローズドテストは省略しない。人間承認のないPlay公開はしない。
7. Pixel以外の実機動作は未検証のままであり、対応保証として記載しない。既知リスクに明記する。
8. 判定表と人間への承認依頼を作る。Codex自身がMG-06やReleaseを承認しない。

例の判定マトリクスは[release-gates.md](references/release-gates.md)を参照する。
