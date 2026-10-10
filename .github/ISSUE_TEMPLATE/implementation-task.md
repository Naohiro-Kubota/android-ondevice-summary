---
name: 実装・PoCタスク
description: GitHub IssuesをTask管理の正本として運用するためのIssueテンプレート
title: '[TASK-XXX] '
labels: ['task', 'status:todo']
assignees: []
---

## Task情報
- **Task ID:** TASK-XXX
- **PLAN:** PLAN-00X
- **種別:** 基盤 / PoC / ADR / 本実装 / 統合 / Release
- **状態:** TODO  <!-- GitHub Project等の状態が正本。ここは作成時の初期値 -->
- **優先度:** P0 / P1 / P2
- **並列稼働数:** 同時最大2Task

## 目的・Scope
- 実施すること:
- 実施しないこと:

## 要求と受入条件
- FR / NFR / ARCH / DATA / SCR / PF:
- AC / NAC:
- TV / ADR:

## 着手条件 / Dependencies
- 先行Issue:
- P0 PoC全部の合格（MG-02a）: 未確認 / 承認済 / 本実装前の例外
- ADR-001〜007全部の承認（MG-02b）: 未確認 / 承認済 / 本実装前の例外
- 該当ADRのStatus:
- Worktree管理Skill・Trusted・適用rules:
- 並列Taskとの競合確認:

## 実施計画
- 実装/PoC手順:
- 正常・異常・キャンセルのテスト:
- ドキュメント更新:

## 成果物と検証結果
- Branch / Worktree:
- PR:
- コード/検証レポート:
- `build/lint`:
- JVM Unit/Component:
- Emulator Smoke/全件:
- Pixel実機（実施 or NOT_RUN）:
- Firebase Privacy（適用 or NOT_RUN）:
- 人間AI品質レビュー（適用 or NOT_RUN）:
- CIリンク:

## Definition of Done
- [ ] 依存・PoC・ADRの前提を満たした
- [ ] スコープと実装が一致する
- [ ] 正常・異常・キャンセル試験を実施した
- [ ] Security/Privacy規則に違反しない
- [ ] PR必須CIが合格した
- [ ] ADR/設計/AC/テスト文書を必要に応じ更新した
- [ ] 人間のMG承認が必要なら証跡がある
- [ ] 残課題・NOT_RUNを明記した
- [ ] 統合後のWorktreeを安全に整理した

## Blocker / Risk / Human Decision
- BLOCKED理由:
- 既知リスク:
- 人間の承認待ち:

> 注意: Task状態の唯一の正本はGitHub Issues。別途Markdownで独立管理しない。PoC成功やCI成功を人間のMG承認と見なさない。
