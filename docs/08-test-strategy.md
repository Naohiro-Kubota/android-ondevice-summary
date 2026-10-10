# 08. テスト戦略・PoC・リリースゲート

**版:** v2.7 / **状態:** テスト方針確定、実測値・PoC結果は未承認。

## 1. TESTレジストリ

| ID | テスト戦略 |
|---|---|
| TEST-001 | 要件IDとテストケース・証跡を対応付ける |
| TEST-002 | JVM Unit/Component Testを基本とする |
| TEST-003 | 全PRでEmulator Smokeを実行、網羅的テストは定期・RC |
| TEST-004 | ML Kit実SDKをPixel 9 Pro XLで検証 |
| TEST-005 | Release候補で日英各20記事の人間レビューを必須化 |
| TEST-006 | SSRF・DNS・リダイレクト等の禁止条件を自動検証 |
| TEST-007 | Release候補ごとにFirebase3製品の自動/明示収集・送信を検証 |
| TEST-008 | テスト証跡と未解決リスクをビルドごとに記録 |
| TEST-009 | P0未合格・ADR未承認・重大未解決問題をリリースゲートにする |
| TEST-010 | 固定評価セットと人間の採点規則を維持 |
| TEST-011 | AI/抽出変更時は影響範囲の追加記事を評価 |
| TEST-012 | PRと定期/RCのEmulator実行範囲を分離 |
| TEST-013 | Pixel1台の検証範囲と他端末未検証リスクを明記 |
| TEST-014 | BLOCKED/NOT_RUNをPASSとして扱わない |

## 2. テストレベル

| レベル | 対象 | 環境 | PR | 定期 | RC |
|---|---|---|---|---|---|
| L1 | モデル・URL・ERR・TelemetryHostPolicy | JVM | 必須 | 必須 | 必須 |
| L2 | UseCase・SessionCoordinator・Inference Gate | JVM Fake | 必須 | 必須 | 必須 |
| L3 | 共有Intent・ライフサイクル・Android API | Emulator | Smoke | 全件 | 全件 |
| L4 | Compose SCR-001〜006操作 | Emulator | Smoke | 全件 | 全件 |
| L5 | ML Kit/AICoreの機能・モデル取得 | Pixel 9 Pro XL | なし | 関連変更時 | 必須 |
| L6 | 記事抽出・日英要約品質 | 自動+人間 | 自動の関連分 | 任意 | 日英20件ずつ必須 |
| L7 | Security/Privacy/Firebase実送信 | 制御環境+Pixel | ポリシー単体 | 関連変更 | RCごと必須 |
| L8 | 端末性能・メモリ・互換性 | Pixel 9 Pro XL | なし | 関連変更 | 必須 |

## 3. Acceptance Criteriaの重点対応

| 検証系列 | 主要ID | 主な手段 |
|---|---|---|
| 共有・二重処理 | AC-001〜008, AC-095〜114, AC-162 | JVM Fake + Intent Instrumentation |
| HTTP安全性 | AC-009〜025, NAC-015〜021, NAC-065 | Fake DNS、制御HTTPサーバー、接続先制御の実装検査 |
| 本文抽出・言語・長文 | AC-026〜037, AC-055〜056, NAC-066〜068 | fixture、正解本文、実機AI |
| モデル・AI | AC-038〜063, AC-115〜123, AC-135〜139, AC-161 | Fake Future、遅延実行、Pixel実機 |
| ライフサイクル | AC-068〜073, AC-100〜108, NAC-087 | Emulator + Pixel |
| セッション整合性 | AC-095〜123, AC-125〜132 | SessionId/ExecutionIdの乱順序テスト |
| Firebase・データ保持 | AC-140〜158, NAC-079〜085, NAC-089〜090 | Policy単体 + RC実送信 |
| 人間品質レビュー | AC-159〜167, NAC-088, NAC-098〜102 | 日英固定40記事 + 追加レビュー |
| 実装ガバナンス | NAC-103〜116 | Task/ADR状態・PRマージ条件検査 |

## 4. セッション・並列AIの必須試験

1. A取得中にBを新共有しAの遅延成功が来ても、Bだけ有効。
2. A要約中にB→Cと連続共有しても、最新C以外はAI実行権を獲得しない。
3. A推論のキャンセルFutureが完了しても、**安全解放未確認なら**新推論を起動しない。
4. A翻訳中のB要約も共通ゲートで直列化する。
5. 資源待機がPoC承認の有限上限に達したらERR-015とし、並列化によって回避しない。
6. モデル取得中の旧記事失効で、取得重複や旧セッション再開を起こさない。
7. 画面回転では二重起動しない。トップ最前面喪失ではキャンセルし復帰後SCR-001。
8. プロセス終了後の旧起動Intent自動再実行を防止し、新しい同一URL共有だけを新Sessionとして扱う。

## 5. セキュリティ試験

loopback、IPv4/IPv6私設・リンクローカル・メタデータ宛、DNSの変化、IPv4-mapped IPv6、手動/多段リダイレクト、HTTPS→HTTP、巨大/圧縮HTML、429/5xx/4xx、タイムアウト、明示キャンセルを試験する。制御されたテストサーバーを使用し、他人のネットワークへ攻撃的な試験を行わない。

**合格基準:** 禁止された宛先へソケット接続を発生させず、定義した制限下で終了。上限値はPoCから決定し、決定前は正式合格にしない。

## 6. AI品質評価

- RCごとに固定日本語20記事・英語20記事を**各1件として**評価（同一記事20回ではない）。AI/抽出変更時は追加記事を評価。
- 自動: URL/抽出/長さ/言語/箇条数/部分要約フラグと、可能な数値・事実のチェック。
- 人間: 本文が当該記事か、重要な事実・数値・固有名詞・否定・条件・翻訳が変質していないかを採点。完全文字列一致で判定しない。
- 等級: `Critical`重大な事実誤認、`Major`中心的内容の取り違え、`Minor`表現・軽微な欠落、`Pass`。
- 未解決Criticalがあれば原則Release停止。品質率・許容値・抽出混入率はPoC後に提案・承認する。
- テスト記事・正解本文は再配布可能なコンテンツまたは作成したfixtureを用い、実ユーザーの記事を取り込まない。

## 7. 技術PoC台帳（TV-001〜016）

| ID | 優先度 | PoC内容 | 完了証跡 |
|---|---|---|---|
| TV-001 | P0 | 日本語要約・英語要約→日本語翻訳 | Pixel実行結果とモデル/OS/SDKの構成 |
| TV-002 | P1 | HTML本文抽出品質 | 日英記事・非記事の正解との比較、混入率 |
| TV-003 | P1 | 400文字の受理境界・長文入力の切り詰め | 399/400/401文字と長文テスト |
| TV-004 | P1 | 言語判定の閾値 | 言語別の判定/誤判定/不明比率 |
| TV-005 | P0 | HTTP SSRF・DNS・転送・上限制御 | 禁止接続が発生しない再現試験 |
| TV-006 | P0 | Firebase自動ネットワーク計測と禁止情報 | SDK設定・送信・受信表示の総合検証 |
| TV-007 | P0 | 要約・翻訳の停止と安全資源解放 | 旧AI中断→新AI実行の安全確認手段 |
| TV-008 | P1 | AI解放待機上限と失敗条件 | 実機計測から上限値を提案・承認 |
| TV-009 | P1 | Summarizationモデル取得共有 | 同一モデル重複開始の抑止 |
| TV-010 | P1 | Translationモデル取得共有・Wi-Fi条件 | ダウンロード条件・継続再利用の実測 |
| TV-011 | P0 | 最前面喪失と構成変更の識別 | 回転継続・離脱取消の実機再現 |
| TV-012 | P0 | 起動Intentの再処理・プロセス死 | 二重実行防止、独立した新共有認識 |
| TV-013 | P0 | 選定OkHttp版とFirebase自動計測 | バージョン組合せ・送信情報 |
| TV-014 | P1 | Readability系の保守性・Android互換・ライセンス | 依存監査・評価結果 |
| TV-015 | P0 | 公式Summarization対応端末・言語機能差 | 公式一覧日付、Pixel実機可用性 |
| TV-016 | P0 | Firebaseホスト名加工・SDK自動収集 | 禁止文字列の非送信を含む検証 |

**代替AIの条件:** TV-001が不合格なら、クラウドLLMを使わずオンデバイス代替を調査しADR-003へ記録。導入・対象端末変更は人間承認。

## 8. GATEレジストリ（GATE-01〜12）

| ID | Gate | 合格条件 |
|---|---|---|
| GATE-01 | Build | Release相当のビルドが成功 |
| GATE-02 | 静的解析 | 重大Lint・依存方向違反がない |
| GATE-03 | 自動テスト | PR必須とRCのEmulator全件が合格 |
| GATE-04 | 要件追跡 | MUST要件に検証手段・結果が対応付く |
| GATE-05 | Security | P0禁止通信・脆弱性試験に合格 |
| GATE-06 | AI成立性 | P0 PoC（含む解放ゲート）が合格 |
| GATE-07 | AI品質 | 自動+人間の日本語20・英語20記事レビュー合格 |
| GATE-08 | Privacy | RCごとのFirebase三製品の実送信検証合格 |
| GATE-09 | Compatibility | Pixel9 Pro XLの必須実機テスト合格、他機種未検証リスクを開示 |
| GATE-10 | Performance | Pixel実測に基づく承認済み目標に適合 |
| GATE-11 | ADR | ADR-001〜007の必要な決定がAccepted |
| GATE-12 | Human Approval | MG-06とPlay公開資格・必要手続きを確認して人間がGoを承認 |

## 9. テスト結果と禁止される判定

状態は`PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`を区別。P0でBLOCKED/NOT_RUNがあればPASSと扱わない。Pixel1台以外の端末テストは、今回の必須試験に含めないため、未検証リスクとして記録する（他機種の試験をPASSと捏造しない）。

## 10. CI案

`pr-check`: build+lint→JVM Unit/Component→Security/Privacy Policy→Emulator Smoke→追跡検査。  
`scheduled-regression`: Emulator全件。  
`release-check`: Emulator全件+PoC/ADR/MG/Pixel/40記事/Firebaseの証跡リンクを照合。  
CI基盤・静的解析ツールの正式選定はADR-007で承認する。GitHub Actionsを第一候補とするが実装済みではない。
