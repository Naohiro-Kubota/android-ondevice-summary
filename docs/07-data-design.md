# 07. データモデル・所有権・保存・外部送信

**版:** v2.7 / **状態:** 論理データ設計確定。SDKの自動収集・具体的なホスト名検査は実機検証待ち。

## 1. 基本原則

1. アプリ独自のDB、要約履歴、記事HTML・本文キャッシュを作らない。
2. 記事由来のユーザーコンテンツをアプリ管理下のプロセス復元ストレージへ保存しない。
3. 所有者を明確にし、不要になった時点でアプリが管理する参照を解放する。OS・SDK内部の物理メモリ即時消去は保証しない。
4. 生URL、記事タイトル、本文、HTML、AI入力・英語中間要約・日本語要約をFirebaseへ送信しない。診断用記事URL情報は、**安全と判定したホスト名だけ**。
5. SessionId、ExecutionId、アプリ独自相関IDはFirebaseへ送信しない。Firebase SDK標準識別子はSDK仕様とプライバシー開示に従う。
6. GA4の対象ユーザー・イベントデータ保持設定は**2か月**。Firebase全サービスの保持期間が一律2か月になるという意味ではない。

## 2. DATAレジストリ

| ID | モデル（論理型） | 主要属性 | 所有・保持 |
|---|---|---|---|
| DATA-001 | `ArticleUrl` | 元URL・検証段階 | SessionCoordinator／セッション中のみ |
| DATA-002 | `FetchedPage` | HTML、最終安全URL、HTTP状態 | HTTP取得～本文抽出の実行中 |
| DATA-003 | `ExtractedArticle` | 本文、タイトル?、サイト? | UseCase／要約実行中 |
| DATA-004 | `ArticleLanguage` | JA、EN、UNDETERMINED、UNSUPPORTED | Execution |
| DATA-005 | `SummarizationInput` | AIに渡す本文・切り詰めフラグ | AI操作中 |
| DATA-006 | `SummaryResult` | 日本語箇条1～3項、タイトル?、サイト?、isPartial | 有効Session／SCR-004表示中 |
| DATA-007 | `SummarySession` | SessionId、URL、SessionStatus、最新Execution | SessionCoordinator |
| DATA-008 | `SummaryExecution` | ExecutionId、処理段階、ERR?、Job | 個別実行 |
| DATA-009 | `TelemetryHost`（旧名`TelemetryArticleUrl`） | 安全検査済みのホスト名のみ | 診断イベント生成の一時値 |
| DATA-010 | `TelemetryEvent` | 許可済みイベント種別・処理段階・ERR分類・ホスト? | Reporter内一時値／Firebase SDK |
| DATA-011 | `DiagnosticError` | 公開ERR・原因分類・安全な診断キー | Reporter内一時値／Crashlytics |
| DATA-012 | `PerformanceMeasurement` | 固定トレース名・所要時間・承認属性 | Reporter内一時値／Performance |

DATA-009のIDは従来名称から引き継ぎ、より正確な実装名を`TelemetryHost`とする。型は自由な文字列で生成できないようにし、安全なPolicy内のみで生成する。

## 3. データ不変条件

| ID | 条件 |
|---|---|
| DINV-001 | 要約結果は非空の日本語箇条1～3項目 |
| DINV-002 | 言語が不明・非対応ならAI入力を作成しない |
| DINV-003 | 部分要約フラグは実際に入力を切り詰めた事実と一致 |
| DINV-004 | Session終了後、旧記事コンテンツをUI状態へ残さない |
| DINV-005 | 異なるExecution間でHTML・本文・AI中間結果を共有しない |
| DINV-006 | モデル管理はURL・本文・要約結果を所有しない |

## 4. データの所有権と終了条件

| データ | 主な保持場所 | 解放タイミング | 永続化 |
|---|---|---|---|
| 元URL | SessionCoordinator、Android入力境界 | Session終了、Intent内容の不要参照解放 | 禁止 |
| HTML | ArticleRepository/Extractor | 抽出終了またはキャンセル | 禁止 |
| 抽出本文 | UseCase | AI/翻訳終了またはキャンセル | 禁止 |
| AI入力 | Summarizer/Translator Adapter | 実行完了とSDK資源の安全な解放後 | 禁止 |
| 翻訳前英語要約 | UseCase | 翻訳終了、キャンセル、エラー | 禁止 |
| 日本語要約結果 | SessionCoordinator → UiState | 結果画面を閉じる・新共有・最前面喪失 | 禁止 |
| Session/Execution IDs | SessionCoordinator | Session終了 | 禁止（Firebase送信も禁止） |
| モデル取得状態 | ModelPreparationManager | プロセス/SDKライフサイクル | SDKの資産管理のみ |
| 診断イベント | TelemetryReporter/Firebase SDK | SDK/サービスの管理期間 | 許可範囲内 |

`SavedStateHandle`、`rememberSaveable`、Bundle、ファイル、Room、Preferencesなどに記事本文・元URL・要約を保存しない。クリップボードへの書き込みは利用者の明示操作であり、OS管理のクリップボード残存にはアプリ管理外の制約があることを考慮する。

## 5. TelemetryHostPolicy

**入力:** 元URLから解析されたホスト候補。**出力:** `TelemetryHost?`。

- 必ずホスト名だけを抽出する。scheme、userinfo、port、path、query、fragmentは**送信しない**。
- IDN/Punycode、末尾ドット、大文字小文字を正規化し、公開サフィックス・サブドメイン情報の扱いを安全に検証する。
- IPリテラル、ローカル名、機微情報を表す可能性のあるサブドメイン、判断不能なホストは`null`。
- 安全性を確認できたホストのAllowlist方式を初期候補とし、広すぎるパターンを許可しない。
- ホストを送れなくてもイベント自体はERR・段階などの固定値で記録してよい。
- 最終的な正規化・Allowlist・公開サフィックス方式はPoC/テストと人間の承認を得る。

### 入力例（実ネットワークには接続しない）

| 元URL | 診断候補 | 理由 |
|---|---|---|
| `https://news.example.com/a?token=x` | `news.example.com`（安全確認できた場合のみ） | query/path不使用 |
| `https://alice.private.example.com/a` | 省略 | ホストに機微値の可能性 |
| `https://127.0.0.1/a` | 省略 | IPリテラルは送信せず、記事取得も拒否 |
| `https://example.com/user/alice` | `example.com`（安全確認できた場合のみ） | 個人情報入りpathを完全除外 |

## 6. Firebaseへ送るイベント

**Analytics:** `share_received`, `summary_started`, `summary_completed`, `summary_failed`, `summary_cancelled`, `model_download_started`, `model_download_completed`。承認済みの状態分類（言語・ERR・段階など）のみ付加。アプリ独自の相関IDは禁止。

**Crashlytics:** 期待済み処理失敗を安全な分類値から新規に構成した非致命的例外として記録。正常なモデル未取得・キャンセル・Telemetry失敗は対象外。同じExecutionの同じ失敗は重複させない。元例外のmessage/cause/URLが混入したstack traceを無検査で渡さない。可能な場合は例外単位の診断キーを使い、別Sessionに流用しない。

**Performance:** `article_fetch`, `article_extract`, `language_detect`, `model_prepare`, `summary_inference`, `summary_translate`, `summary_total`の固定名を使用。動的URLや生記事情報をtrace名・属性・metricへ付けない。

## 7. SDK自動収集と保持

共通Reporterを経由しないFirebase SDK標準の収集が存在する。特にPerformanceの自動HTTP計測はURLパス等を含む可能性があるため、送信範囲を**RCごと**に検証する。十分に安全確認できない場合は自動計測を無効化し、固定名のカスタムトレースを使う。Crashlyticsの自動収集・AnalyticsのBreadcrumbも禁止情報混入の検査対象。

| 主体 | 管理範囲 | 必須対応 |
|---|---|---|
| アプリ | 元記事・入力・結果の一時メモリ | セッション終了時に参照解放。復元・キャッシュ禁止 |
| ML Kit / Android | ダウンロード済モデル、SDK内部一時情報 | API/OS仕様と安全な解放・権限を検証 |
| Firebase SDK | 端末上の送信待ちイベント・クラッシュデータ | SDK標準情報・禁止値混入・送信設定を検証 |
| GA4 | 対象ユーザー・イベントデータ | 保持設定2か月。設定証跡をRCへ紐づけ |
| Crashlytics / Performance | サービスごとの保存・削除 | 各サービス仕様を公開前に確認。GA4の2か月を流用しない |

法令上の同意が必要な場合は、対象の収集を同意取得まで無効化する。Google Play Data Safety、プライバシーポリシーには実装した収集・送信の事実を反映する。

## 8. 実装に渡す安全なデータ型の考え方

```kotlin
@JvmInline value class OriginalArticleUrl(val value: String)

// 概念例。実際の生成子は非公開とし、検証済み値だけを生成する。
@JvmInline value class TelemetryHost private constructor(val value: String)

data class SummaryResult(
    val bullets: List<String>, // 非空1～3項、生成時に検証
    val title: String?,
    val site: String?,
    val isPartial: Boolean
)
```

このコードは設計スケッチであり、コンパイル可能な実装の約束ではない。高リスクの境界では、入力型と診断型を分け、意図しない生データ送信をコンパイル時・Test Double・RC検査で防ぐ。
