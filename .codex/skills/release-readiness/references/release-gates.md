# Release候補チェックリスト

| Gate | 検証内容 | 判定 |
|---|---|---|
| GATE-01〜03 | ビルド、静的解析、PR必須CI、Emulator全件 | PASS/FAIL/BLOCKED/NOT_RUN |
| GATE-04 | MUST要件とテスト証跡の追跡 | 同上 |
| GATE-05 | SSRF、安全性、禁止通信 | 同上 |
| GATE-06 | Pixelでの日英AI、モデル/キャンセル/排他のPoC | 同上 |
| GATE-07 | 日本語20・英語20記事の人間による品質評価 | 同上 |
| GATE-08 | Firebase3製品のRC個別Privacy検査 | 同上 |
| GATE-09 | Pixel 9 Pro XL実機試験と他端末未検証リスク | 同上 |
| GATE-10 | 承認済みの性能指標・実測 | 同上 |
| GATE-11 | 主要ADR-001〜007すべてAccepted、人間の承認証跡 | 同上 |
| GATE-12 | 人間による最終判定 | 同上 |

Play公開: TASK-037（アカウント条件）→ TASK-038（必要な場合のクローズドテスト）→ TASK-039（国・Data Safety・プライバシー・審査）。任意のクローズドテストを義務とするのではなく、公式条件に従う。

以下の証跡は他に代用不可：Pixel以外のEmulator合格は実機合格ではない。固定文言テストはAI意味評価ではない。ポリシーのUnit TestはFirebase SDK実送信検証ではない。
