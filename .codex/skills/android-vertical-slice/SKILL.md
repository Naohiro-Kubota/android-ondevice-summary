---
name: android-vertical-slice
description: Android記事要約アプリのVertical SliceをKotlin・Jetpack Composeで実装する。共有Intent、記事取得・抽出、ML Kit要約・翻訳、結果・ERR画面などのTASKを画面からPort/Adapter・テストまで一体で実装するときに使用する。
---

# Android Vertical Slice実装

## 着手ゲート

- `github-task-workflow`でIssueがREADYであることを確認する。
- **PLAN-004以降の本実装では**全P0 PoCとADR-001〜007、MG-02a/02bの人間承認を必ず確認する。未達なら本実装には着手しない。
- 開発前に`AGENTS.md`、`docs/03-functional-requirements.md`、`docs/05-screens-and-flows.md`、`docs/06-architecture.md`、該当AC/NACを読む。
- `worktree-management`で専用Worktreeを用意する。最大2並列。

## 実装の基本手順

1. Issue内に対象のFR/NFR/ARCH/SCR/PF/AC/NACと正常・異常・キャンセルを列挙する。
2. UI（Compose）→ViewModel→SessionCoordinator→UseCase→Domain Port→Data Adapterの順に責務を確認する。レイヤのみ完成させてタスク完了にしない。
3. Single Activity、単一`:app`、手動DI、StateFlow、Coroutinesを基本とする。未承認ライブラリを勝手に追加しない。
4. Test Doubleをコンストラクタ注入してまず状態遷移・失敗・競合をJVMで検証する。
5. 関連Sliceの本番Adapter・画面・テストを統合する。ML Kit実機動作が必要な部分はPixel 9 Pro XLの証跡を区別する。
6. 部分的に成功した場合でも未実施テストをPASSにしない。Issue/PRへ実施状況を記録する。

## 特に壊しやすい設計不変条件

- 別の**共有操作**であれば同じURLでも新しいSessionを開始する。Activity再生成/Compose再描画は再受信扱いしない。
- 新共有が旧セッションを即時無効化。旧AI処理のリソースが未解放なら新AI処理は待機。要約と翻訳で共通排他。
- モデル取得はセッション終了後もSDK管理下で継続可能。記事本文・URLはモデル管理側へ保持しない。
- ユーザーが最前面を離れたらセッション取消。回転では継続し、プロセス死から復元しない。
- 本文400文字境界、部分要約の表示、1〜3項目、手動再試行とERR分類を守る。
- 記事データは永続化しない。診断送信は安全なホスト名のみ。独自Session/Execution IDはFirebase送信禁止。

`docs/06-architecture.md`の責務・状態、`docs/07-data-design.md`の所有権、`docs/08-test-strategy.md`のDoDに従い、必要に応じて文書も更新する。
