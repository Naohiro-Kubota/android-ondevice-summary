# worktree-management Skillの事前準備

本成果物にはSkill本体を同梱していません。以前のプロジェクトで作成したSkillを、実際のCodexワークスペースの適切な位置（例：`.codex/skills/worktree-management/`）へ設置し、実行権限と依存ライブラリを検査してください。

**TASK-036（MG-01前の必須項目）:**

1. Skillの`SKILL.md`および必要なスクリプトが実在することを確認。
2. Worktree作成・Trusted状態確認・`.codex/rules`適用・削除の一連をテスト。
3. Trustedの設定は**ユーザーが事前承認したワークスペース**だけに限定する。
4. Worktree削除時には未コミット・未統合成果物がないことを確認。
5. コマンド、権限、依存関係が不明な場合は直接gitコマンドに回避せずTaskをBLOCKEDとして人間へ報告。

Codexの設定におけるProject Trustの記述（2026-10-10参照）：https://developers.openai.com/ja-JP/docs/config-file/config-reference
