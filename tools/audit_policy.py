#!/usr/bin/env python3
"""Check the provenance and active canonical coverage of all source rule IDs."""
from pathlib import Path
import re, csv, sys, json
root=Path(__file__).resolve().parents[1]
index=root/'docs/agent-policy/RULE_INDEX.tsv'
sources={'CORE':'AGENTS_v1.6.md','FE':'FRONTEND_GUIDELINES.md','BE':'BACKEND_GUIDELINES.md'}
original=set()
import zipfile
with zipfile.ZipFile(root/'docs/agent-policy/sources/original-rulebooks.zip') as src_archive:
 source_texts={scope:src_archive.read(fname).decode('utf-8') for scope,fname in sources.items()}
for prefix,fname in sources.items():
 txt=source_texts[prefix]
 if prefix=='CORE': rules=re.findall(r'(?m)^- ([A-Z][A-Z0-9]*\d+) ([MSO]) ',txt)
 else: rules=re.findall(r'(?m)^- \*\*([A-Z][A-Z0-9]*\d+) ([MSO])\*\*',txt)
 original.update((prefix,rid,level) for rid,level in rules)
with index.open(newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
indexed={(r['source'],r['original_id'],r['strength']) for r in rows}
errors=[]
if original!=indexed:errors.append(f'source coverage mismatch missing={original-indexed} extra={indexed-original}')
if len(indexed)!=len(rows):errors.append('duplicate source IDs in rule index')
seen_active=set()
for row in rows:
 target=root/row['target'];name=row['canonical_id'];source=row['source']
 if not target.is_file():errors.append(f'missing {target}')
 if row['status']=='active':
  if name in seen_active:errors.append(f'duplicate active {name}')
  seen_active.add(name)
  if not re.search(r'(?m)^- (?:\*\*)?'+re.escape(name)+r' [MSO]',target.read_text()):
   errors.append(f'active rule not found: {name} in {target}')
 elif row['status']=='alias-to-core':
  if not name.startswith('CORE.') or not re.search(r'(?m)^- '+re.escape(name)+r' '+re.escape(row['strength'])+r' ',target.read_text()):
   errors.append(f'alias target not found: {name} in {target}')
 else:errors.append(f'unknown status {row["status"]}')
# All source PERF sections retained in references (section content deliberately not tokenized/altered).
perf_refs=root/'.agents/skills/compute-optimization/references'
perf=list(perf_refs.glob('*.md'))
if len(perf)!=11:errors.append('expected 11 performance references')
for skill in ['frontend-engineering','backend-engineering','compute-optimization']:
 if not (root/'.agents/skills'/skill/'SKILL.md').exists():errors.append(f'missing skill {skill}')
manifest=json.loads((root/'docs/agent-policy/MANIFEST.json').read_text())
if sum(manifest['source_counts'].values())!=len(rows):errors.append('manifest count mismatch')
if errors:
 print('FAIL —',len(errors),'errors')
 for e in errors:print(' -',e)
 sys.exit(1)
print(f'OK: {len(rows)} source rules mapped; {len(seen_active)} canonical active; {len(rows)-len(seen_active)} aliases; {len(perf)} performance sections; 3 Codex skills.')
