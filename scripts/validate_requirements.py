#!/usr/bin/env python3
"""要件レジストリの連番・重複・参照・重大な決定の一致を標準ライブラリだけで検証。"""
from __future__ import annotations
import re
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parents[1]
DOCS = BASE / 'docs'
SOURCE = {
    'D': ('01-product-overview.md', 13, 3),
    'US': ('02-user-requirements.md', 9, 3),
    'CON': ('02-user-requirements.md', 20, 3),
    'INV': ('02-user-requirements.md', 20, 3),
    'FR': ('03-functional-requirements.md', 62, 3),
    'ERR': ('03-functional-requirements.md', 17, 3),
    'AC': ('03-functional-requirements.md', 167, 3),
    'NFR': ('04-nonfunctional-requirements.md', 72, 3),
    'NAC': ('04-nonfunctional-requirements.md', 116, 3),
    'SCR': ('05-screens-and-flows.md', 6, 3),
    'PF': ('05-screens-and-flows.md', 12, 3),
    'ARCH': ('06-architecture.md', 20, 3),
    'DATA': ('07-data-design.md', 12, 3),
    'DINV': ('07-data-design.md', 6, 3),
    'TEST': ('08-test-strategy.md', 14, 3),
    'TV': ('08-test-strategy.md', 16, 3),
    'GATE': ('08-test-strategy.md', 12, 2),
    'PLAN': ('09-implementation-plan.md', 7, 3),
    'TASK': ('09-implementation-plan.md', 39, 3),
    'ADR': ('09-implementation-plan.md', 7, 3),
    'COD': ('10-codex-instructions.md', 30, 3),
}
errors=[]
counts={}
all_defined=set()
for prefix,(file,count,width) in SOURCE.items():
    text=(DOCS/file).read_text(encoding='utf8')
    identifiers=re.findall(rf'^\| ({re.escape(prefix)}-\d{{{width}}}) \|',text,re.M)
    counts[prefix]=len(identifiers)
    missing=set(f'{prefix}-{i:0{width}d}' for i in range(1,count+1))-set(identifiers)
    extra=set(identifiers)-set(f'{prefix}-{i:0{width}d}' for i in range(1,count+1))
    duplicate=[a for a,c in Counter(identifiers).items() if c>1]
    if missing or extra or duplicate or len(identifiers)!=count:
        errors.append(f'{prefix} 実体数={len(identifiers)}/{count} 欠番={sorted(missing)} 余分={sorted(extra)} 重複={duplicate}')
    all_defined.update(identifiers)
# MG is alphanumeric substage
mg_text=(DOCS/'09-implementation-plan.md').read_text('utf8')
mg=re.findall(r'^\| (MG-[0-9]{2}[ab]?) \|', mg_text, re.M)
mg_expected={'MG-01','MG-02a','MG-02b','MG-03','MG-04','MG-05','MG-06'}
if set(mg)!=mg_expected or len(mg)!=7:
    errors.append(f'MG登録不正: {mg}')
all_defined.update(mg)
counts['MG']=len(mg)
# Reference verification: templates have XXX and are intentionally excluded.
all_text='\n'.join(p.read_text('utf8') for p in [BASE/'AGENTS.md', BASE/'README.md', *DOCS.glob('[0-9][0-9]-*.md')])
for ref in sorted(set(re.findall(r'(?<![A-Za-z0-9])(?:FR|NFR|AC|NAC|ERR|CON|INV|DINV|SCR|PF|ARCH|DATA|TEST|TV|GATE|PLAN|TASK|ADR|COD|US)-\d{2,3}(?!\d)',all_text))):
    if ref not in all_defined:
        errors.append(f'参照先不明: {ref}')
for ref in sorted(set(re.findall(r'(?<![A-Za-z0-9])MG-\d{2}[ab]?(?!\w)',all_text))):
    if ref not in all_defined:
        errors.append(f'マイルストーン未登録: {ref}')
# Semantic consistency checks (not a substitute for human review)
required={
  'AGENTS.md':['最大2件','GitHub Issues','MG-02a/02b','Trusted'],
  'docs/09-implementation-plan.md':['最大2件','GitHub Issues','未作成・不明','MG-02a','MG-02b'],
  'docs/10-codex-instructions.md':['最大2件','GitHub Issues','未作成・不明','MG-02a','MG-02b'],
  'docs/08-test-strategy.md':['20記事','Pixel 9 Pro XL','Emulator Smoke','Release候補'],
  'docs/07-data-design.md':['2か月','TelemetryHost','SessionId','Firebase'],
  'docs/05-screens-and-flows.md':['共通AI','旧Session','Wi-Fi'],
}
for file,markers in required.items():
    text=(BASE/file).read_text('utf8')
    for marker in markers:
        if marker not in text:errors.append(f'{file}: 決定事項のキーワード不足 {marker}')
expected_docs=[f'{i:02d}-' for i in range(1,11)]
for prefix in expected_docs:
    found=list(DOCS.glob(prefix+'*.md'))
    if len(found)!=1:errors.append(f'文書{prefix} が{len(found)}件（1件必要）')
report=['# 追跡可能性・ID整合性の検査結果','',
        '**検査対象:** 要件文書10件、ルートAGENTS.md、README。',
        '**検査方法:** `python3 scripts/validate_requirements.py`（標準ライブラリのみ）。','',
        '## レジストリの定義件数','',
        '| Prefix | 定義件数 | 期待件数 |','|---|---:|---:|']
for prefix,(_,count,_) in SOURCE.items(): report.append(f'| {prefix} | {counts[prefix]} | {count} |')
report.append(f'| MG | {counts["MG"]} | 7 |')
report += ['', '## 自動検証結果', '', '**結果：'+('PASS' if not errors else 'FAIL')+'**', '']
if errors:
    report+=['検出した問題:','']+['- '+e for e in errors]
else:
    report+=['- レジストリIDの欠番・重複なし。','- 対象形式の参照IDに未定義なし。','- 10文書が指定名で存在。','- 主要な運用決定（最大2Task・GitHub Issues・一括ゲート・Pixel1台・GA4保持2か月）のキーワード検査を実施。']
report+=['','## 検査の限界','',
         '- この検査は構文・IDの整合性を保証するものであり、実機PoC、要件の品質、全ての意味的矛盾、過去版との逐語一致は保証しない。',
         '- 初期段階の原文が完全に再掲されていない旧FR/ACについては、合意内容を基に説明文を再構成している。過去の元仕様がある場合、MG-01で照合する。',
         '- ADRはIDと採用課題だけを登録しており、個別のAccepted ADR文書は未作成。実装着手ゲートを満たさない。',
         '- Google Playアカウントは未作成・不明。公式要件に従う必要がある。',
         '']
(DOCS/'TRACEABILITY.md').write_text('\n'.join(report),encoding='utf8')
for name in sorted(counts):print(f'{name:5} {counts[name]:3}')
if errors:
    print('検査失敗:')
    for e in errors:print(' -',e)
    raise SystemExit(1)
print('PASS: 定義・連番・参照・必須決定の簡易検査が完了')
