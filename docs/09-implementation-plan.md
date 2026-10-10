# 09. 実装計画・依存関係・タスクバックログ

**版:** v2.7 / **状態:** 実装計画確定。コード実装・PoC・ADRは未実施。

## 1. 実行方式の最終決定

**重要:** P0の技術検証が**すべて**合格し、主要ADR-001〜007が**すべて**人間によりAcceptedとして承認され、MG-02a/02bの承認記録が揃うまで、PLAN-004以降の本実装を開始してはいけない。**個別ADRのみの先行承認によって本実装を段階解禁しない。**

例外的にPLAN-001の技術非依存のアプリ基盤骨格、FakeによるPoC/状態遷移検証、およびPLAN-002の検証専用コードは着手可能。検証コードは原則本実装と分離し、品質確認なしに本番へ流用しない。

- 実装は「共有→安全取得→抽出→日本語要約→英語翻訳→診断・異常系」の**Vertical Slice**で進める。
- Codexの独立タスクは**最大2件**まで、**別Git Worktree**で並列に実施する。
- 通常タスクはCI・コードレビューで進め、主要マイルストーン（MG）で人間が承認する。
- Taskの状態・担当・依存・PRは**GitHub Issuesを正本**とする。READMEやMarkdownへ同じ状態を別管理しない。
- 日本向けGoogle Play公開は内部テスト→一般公開を希望するが、必須のクローズドテスト等が適用される場合は省略しない。

## 2. PLANレジストリ

| ID | フェーズ | 成果物 | 承認・移行ゲート |
|---|---|---|---|
| PLAN-001 | 開発基盤・PoC準備 | Kotlin/Compose骨格、Fake、CI、Skill運用 | MG-01 |
| PLAN-002 | P0技術PoC | 検証コード、Pixel実測、PoCレポート | MG-02a |
| PLAN-003 | ADR比較・採否承認 | ADR-001〜007のAccepted記録 | MG-02b |
| PLAN-004 | アプリ基盤本実装 | SessionCoordinator、共有AIゲート、DI、Intent制御 | MG-03 |
| PLAN-005 | Vertical Slice機能実装 | 共有、安全取得、抽出、日英要約、UI、ERR | MG-04 |
| PLAN-006 | 統合・品質・セキュリティ | Security、Firebase、AI品質、性能、トレーサビリティ | MG-05 |
| PLAN-007 | RC・公開準備 | RC、Pixel検証、40記事レビュー、Play要件・公開承認 | MG-06 |

## 2.1 未承認ADRレジストリ（ADR-001〜007）

| ID | 決定対象 | 初期状態 |
|---|---|---|
| ADR-001 | HTTPクライアントと接続先安全性 | Proposed |
| ADR-002 | HTML解析・主本文抽出 | Proposed |
| ADR-003 | オンデバイス要約・翻訳方式 | Proposed |
| ADR-004 | AI停止・解放確認・共通排他制御 | Proposed |
| ADR-005 | Firebase診断・自動計測方式 | Proposed |
| ADR-006 | Androidライフサイクルと共有Intentの制御 | Proposed |
| ADR-007 | CI・テスト・静的解析ツール | Proposed |

これらは**番号と選定課題の登録**であり、ADRをAcceptedとして実ファイル化した意味ではない。PoC/比較の証跡が揃ってから人間が判断する。

## 3. TASKレジストリ（TASK-001〜039）

| ID | PLAN | 作業 | 依存・開始ゲート | DoD上の特記事項 |
|---|---|---|---|---|
| TASK-001 | 001 | 単一:appのAndroid Kotlin/Compose骨格 | なし | Build成功・SCR-001表示 |
| TASK-002 | 001 | 手動DI・AppContainerの骨格 | 001 | Fakeのコンストラクタ注入を検証 |
| TASK-003 | 001 | JVM/Emulator CIの骨格 | 001 | PRジョブ構築・Smoke成功 |
| TASK-004 | 001 | Domainモデル・Port・ERR骨格 | 001 | SDK非依存Unit Test合格 |
| TASK-005 | 001 | FR/AC/NFR/NAC追跡基盤 | 001 | ID連番・参照・証跡形式が検査可能 |
| TASK-006 | 002 | 日英要約・翻訳可用性PoC | 001 | TV-001/015 Pixel証跡 |
| TASK-007 | 002 | 安全なHTTP・OkHttp評価PoC | 001 | TV-005/013で禁止接続遮断 |
| TASK-008 | 002 | Firebase3製品Privacy PoC | 001 | TV-006/016の明示・自動送信評価 |
| TASK-009 | 002 | AI停止・解放・排他PoC | 006 | TV-007/008、不能なら不合格 |
| TASK-010 | 002 | モデル取得・再利用PoC | 006 | TV-009/010、Wi-Fi/同意の実測 |
| TASK-011 | 002 | Intent/最前面/プロセス死PoC | 001 | TV-011/012、誤キャンセル防止 |
| TASK-012 | 003 | ADR-001〜006の比較・採否案 | 006〜011、必要なP1証跡 | 人間承認。未合格ADRはAcceptedにしない |
| TASK-013 | 003 | ADR-007のCI/静的解析選定 | 003 | 人間承認 |
| TASK-014 | 004 | SessionCoordinator本実装 | MG-02a/b、002、004 | Session/Execution乱順序テスト |
| TASK-015 | 004 | 共通AIゲート・モデル管理本実装 | MG-02a/b、014 | 解放安全・重複取得・待機上限 |
| TASK-016 | 004 | Single Activity/Intent/最前面Adapter | MG-02a/b、014 | 回転継続・前面喪失取消 |
| TASK-017 | 005 | 共有・起動Slice | 014、016 | SCR-001/002、同一URL新共有 |
| TASK-018 | 005 | 安全なHTML取得Slice | 017、ADR-001 | SSRF・DNS・転送試験 |
| TASK-019 | 005 | 本文抽出・言語Slice | 018、ADR-002 | HTML品質・400文字境界・言語ERR |
| TASK-020 | 005 | 日本語要約Slice | 015、019、ADR-003/004 | SCR-003/004、モデル・要約・取消 |
| TASK-021 | 005 | 英語要約→日本語翻訳Slice | 020 | 共通AIゲート、英語品質 |
| TASK-022 | 005 | コピー・元記事外部起動Slice | 020 | セッション破棄・Clipboard |
| TASK-023 | 005 | ERR全件の整合・再試行Slice | 018〜021 | ERR-001〜017。各Sliceでも必要なERRを実装 |
| TASK-024 | 005 | Firebase診断Slice | 015、ADR-005 | 禁止情報非送信・診断失敗隔離 |
| TASK-025 | 006 | Security統合検証 | 018、023 | TV-005/セキュリティGATE |
| TASK-026 | 006 | Firebase Privacy統合検証 | 024 | 三製品の自動・明示収集が適合 |
| TASK-027 | 006 | AI品質・性能改善 | 020、021 | 承認済み品質・P50/P95基準 |
| TASK-028 | 006 | Android統合・UIテスト | 017〜023 | Emulator網羅的試験 |
| TASK-029 | 006 | 要件追跡監査 | 025〜028 | MUSTから証跡まで辿れる |
| TASK-030 | 007 | Release候補ビルド作成 | MG-05 | バージョン・構成を固定 |
| TASK-031 | 007 | Pixel 9 Pro XL実機試験 | 030 | 実SDK・ライフサイクル試験合格 |
| TASK-032 | 007 | 日本語20・英語20記事レビュー | 030、031 | 人間の判定記録 |
| TASK-033 | 007 | RCのFirebase Privacy検証 | 030 | 当該RCの実送信・設定証跡 |
| TASK-034 | 007 | Release判定資料作成 | 031〜033、037、038 | GATE-01〜12、他端末未検証リスク |
| TASK-035 | 007 | 最終Go/No-Go承認 | 034、039 | 人間がRelease承認 |
| TASK-036 | 001 | Worktree Skill/Trusted運用の整備 | 001 | Skillの実在と安全な作成/削除/ルール適用 |
| TASK-037 | 001/007 | Playアカウント作成・公開資格の確認 | なし | アカウント種別/作成日/資格を記録 |
| TASK-038 | 007 | 必須クローズドテスト対応（条件付き） | 037、内部テスト | 適用時は必須人数/期間・製品版アクセス取得。不適用は根拠記録 |
| TASK-039 | 007 | Play Store公開前の最終チェック | 030、037/038 | Data Safety、プライバシー、国/審査/必要書類 |

### 並列化の例

- 許可候補: TASK-007（HTTP PoC）とTASK-008（Firebase PoC）の並列実行、異なるWorktree。
- 禁止候補: TASK-009がTASK-006の実SDK実行に依存するのに、完了していない006を前提に本実装をすること。
- 同じファイルを集中的に変更するタスク同士は、IDが違っても競合するため並列化しない。2件上限に達したら次を起動しない。

## 4. マイルストーン（人間の承認ゲート）

| ID | 承認内容 | 完了条件 |
|---|---|---|
| MG-01 | 開発基盤 | Project・CI・Test Double・Trusted/Skill運用の準備 |
| MG-02a | P0 PoC | TV-001,005,006,007,011,012,013,015,016等、対象P0の合格と証跡 |
| MG-02b | 主要ADR | **ADR-001〜007すべてがAccepted**、採用版・承認者・日付を確認 |
| MG-03 | アプリ基盤 | State・AI Gate・Intent・ライフサイクルの検証 |
| MG-04 | 主要機能 | 日英のSliceと関連AC・UI・ERR検証 |
| MG-05 | 統合・品質 | Security、Privacy、品質・性能、未解決リスク評価 |
| MG-06 | Release | Pixel/40記事/RC Privacy/GATEとPlay公開資格の人間承認 |

**注意:** `MG-02a`はPoC成功、`MG-02b`は技術採用の意思決定。互換性・ライセンス・保守などのP1証跡が不足するADRをAcceptedにしてはならない。Gateの完了はIssueコメントや承認記録に根拠リンクを付ける。

## 5. GitHub Issuesの状態・DoD

**正本:** GitHub IssuesのTASK-IDラベル・本文・依存関係・PR・マイルストーン。ローカルのIssueテンプレートは入力形式であって状態管理台帳ではない。

Issue状態: `TODO`, `READY`, `IN_PROGRESS`, `BLOCKED`, `IN_REVIEW`, `DONE`。`DONE`はPR/CIだけでなくDoDが満たされた場合。PoC/ADR前の本実装はBLOCKED。

### Definition of Done

- 該当Task/要求/AC/NAC/ADR/PoCへのリンクと依存条件を確認済み。
- 変更対象・範囲外を記録し、独立Worktreeで変更・レビュー・統合。
- 実装と対応する正常/異常/キャンセルの自動テストを同一Sliceで提供。
- 必須CIがすべて合格（未実施はPASS扱いにしない）。
- 記事データ・診断データの安全性要件に違反しない。
- ADR/仕様/テスト文書を更新し、必要な人間のMG承認がある。
- 実機必須タスクはPixel実機の試験結果があり、未実施の場合DONEにしない。
- PRマージ・Issue更新・Worktreeの安全な清掃を記録する。

## 6. Google Play公開経路

**現時点のアカウント:** 未作成・不明。公開可否は未決定。

1. Internal Testingを実施する。
2. Play Consoleのアカウント種別・作成日・製品版アクセスを確認する（TASK-037）。
3. 2023-11-13以降作成の新規個人アカウント等で公式のクローズドテスト義務が適用される場合、必要人数・連続日数・申請を完了する（TASK-038）。現時点の公式説明では**12人以上が14日間連続でオプトイン**。
4. App Content、Data Safety、プライバシーポリシー、公開国、日本語ストア説明、必要審査を確認する（TASK-039）。
5. MG-06で人間が最終承認した場合のみ製品版を公開する。

参照: https://support.google.com/googleplay/android-developer/answer/14151465?hl=ja 。公開時には最新要件を再確認する。任意のクローズドテストは計画に追加しないが、公式に必須なら省略しない。

## 7. 実施していないこと

本書は計画であり、Issue作成・PoC・ADR Accepted・Releaseビルド作成の実績を意味しない。Codexの作業結果は必ず実行結果と区別して報告する。
