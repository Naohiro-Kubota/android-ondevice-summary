---
name: poc-adr-governance
description: 技術PoCの計画・実施・証跡化とADR提案・人間承認ゲートを管理する。ML Kit、OkHttp、本文抽出、Firebase、AI解放、AndroidライフサイクルのPoCや技術選定、本実装開始可否の判定に使用する。
---

# PoCとADRのガバナンス

## 原則

- P0 PoCの技術的**実行結果**と、人間による**承認**を区別する。
- 全P0 PoC合格および主要ADR-001〜007の人間によるAccepted承認、MG-02aとMG-02bの記録が揃うまで、PLAN-004以降の本実装を**BLOCKED**とする。
- 候補ライブラリはPoC専用コードで試せる。本実装への採用・流用はADR承認とレビューが必要。
- MUSTを満たさない場合にクラウドLLMへ変更したり、HTTP/Privacyの制約を緩めたりしない。代替のオンデバイス方式をADR案として提示する。

## 手順

1. `docs/08-test-strategy.md`と`docs/09-implementation-plan.md`から対象TV/ADR・Gateを特定する。
2. `docs/POC-REPORT-TEMPLATE.md`を用い、入力条件・合格条件・Pixel9 Pro XLの実機環境・否定試験を記載する。
3. PoC専用Worktreeを`worktree-management`で準備。実機が使えない場合は`NOT_RUN`/`BLOCKED`を付記し、成功扱いしない。
4. 再現用テスト、評価データ、コマンド、SDKバージョン、ログ**から禁止情報を除外した証跡**を記録する。
5. [poc-gates.md](references/poc-gates.md)のP0安全性を満たさない場合、不合格・代替案を報告する。
6. `docs/adr/ADR-TEMPLATE.md`から提案ADRを生成。Statusは`Proposed`。候補比較と選定理由、実測、ライセンス、リスクを記述する。
7. 実機PoCとADRを人間へ提示して承認記録を求める。**Codexは自分の提案ADRをAcceptedへ変更しない**。
8. 本実装のREADY判定は、文書上のStatusだけでなく人間の承認証跡、関連Issue、MG承認の一致を検査する。不明ならBLOCKED。

## 重点

- TV-007: `cancel()`/`close()`呼出しと実際のAICore資源解放は同義ではない。未確認なら次のAI実行権を与えない。
- TV-005: URL文字列/DNS事前検証だけでSSRF対策完了としない。
- TV-006/016: Firebase自動計測は`TelemetryReporter`の検査を経由しない。安全性を確認できなければ不採用。
- TV-011/012: 最前面喪失と回転、Intentの再配送と新規共有を混同しない。
- PoCコードは原則検証専用で本実装に直接混ぜない。

関連文書: `docs/POC-REPORT-TEMPLATE.md`、`docs/adr/ADR-TEMPLATE.md`、`docs/08-test-strategy.md`。
