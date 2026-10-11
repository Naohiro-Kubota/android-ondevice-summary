---
name: security-privacy-verification
description: Android記事要約アプリのHTTP/SSRF安全性とFirebaseのプライバシー適合性を検証する。URL・DNS・リダイレクト、診断用ホスト名、SDK自動収集、記事の非永続化、Release候補の送信内容監査が必要なときに使用する。
---

# Security / Privacy検証

## 対象

- `docs/04-nonfunctional-requirements.md`、`docs/07-data-design.md`、`docs/08-test-strategy.md`、ADR-001/005。
- **禁止事項の発見はP0**。安全性を十分に確認できない自動収集は有効化しない。

## HTTP検証

1. リクエスト対象はhttp/httpsのみ。禁止ホスト・IP形式、IPv4/IPv6、ユーザー情報、ローカル・プライベート・リンクローカル等を評価する。
2. DNS解決結果の**全候補**と実際の接続先の整合、リダイレクト各段、HTTPS→HTTP downgrade、再解決、圧縮後の展開サイズ、応答上限を確認する。
3. 制御されたローカルテストサーバー・DNS Fake等を使い、第三者サイトへ攻撃的な通信をしない。
4. リソースが必要な場合でもSSRF規則の緩和や全ページ抽出へのフォールバックはしない。

## Firebase・データ取扱い検証

1. Analytics・Crashlytics・Performance Monitoringそれぞれについて、明示的イベントとSDK自動計測を分けて検証する。
2. 元URL、パス、クエリ、ユーザー情報、フラグメント、記事本文、HTML、AI入力/出力、SessionId/ExecutionIdが**いずれの製品にも混入しない**ことを検査する。
3. `TelemetryHostPolicy`の失敗はホスト名省略（fail closed）。許可判定できないホスト名を送信しない。
4. Performance自動計測を検証できない・禁止情報が混入する場合は、計測を無効にし、固定名カスタムトレースへの移行をPoC/ADRで判断する。
5. Crashlytics例外文字列・cause・Breadcrumbs、デフォルトキーのセッション間汚染も対象。
6. **Release候補ごと**に実SDKの収集・送信を評価する。設定ファイルのチェックのみでPASSとしない。
7. GA4の対象データ保持設定が2か月であることを、Release準備で確認する。

検証結果は[privacy-evidence.md](references/privacy-evidence.md)の表に従ってIssue/PoC/Release証跡へ記載し、人間レビューを受ける。
