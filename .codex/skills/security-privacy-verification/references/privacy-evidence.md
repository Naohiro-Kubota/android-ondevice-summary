# セキュリティ・プライバシーの検証証跡

## 記録項目

| 対象 | 必須記録 |
|---|---|
| ビルド | コミットSHA、APK/AAB識別、Debug/Release、実施日時 |
| SDK | Firebase3製品、OkHttp・Gradleプラグインのバージョン |
| 端末 | Pixel 9 Pro XLのOS/Play services/ML Kitモデル情報 |
| 送信試験 | 人工的な機密文字列、送信先、観測方法、観測の限界 |
| 診断属性 | URLホストのみか、SessionId等が無いか、各SDKでチェック |
| 自動収集 | Analytics自動イベント、Crashlytics自動ログ、Performanceネットワーク計測 |
| 結果 | PASS/FAIL/BLOCKED/NOT_RUN。未確認をPASSとしない |

## セキュリティ観点

- URL取得は実接続先の安全性まで確認し、DNS事前検証のみで通過にしない。
- 端末側に残るHTTPキャッシュ・Session UI state・SavedStateHandle・Clipboardの持続性を分けて点検する。
- フック・外部計測SDKに本文・AI入出力が漏れないことを観測可能な範囲で検証する。
- TLS暗号化で通信内容が見えないことを、送信データが安全という証拠にしない。
- SDKの仕様上、十分な検証が不能なら当該自動収集を不採用にする。
