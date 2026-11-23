#!/usr/bin/env python3
"""Merge reviewed results for previously unseen filenames; never rescan old transcripts."""
import argparse, collections, datetime, json, pathlib

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--results', required=True, type=pathlib.Path)
p.add_argument('--manifest', required=True, type=pathlib.Path)
a = p.parse_args()
base = pathlib.Path(__file__).resolve().parent
path = base / 'data/thread-results.json'
saved = json.loads(path.read_text())
new = json.loads(a.results.read_text())
manifest = json.loads(a.manifest.read_text())
entries = manifest.get('results', manifest.get('podcasts', []))
assert len(entries) == manifest.get('total', len(entries)), 'Incomplete manifest'
old_files = {e['file'] for e in saved['episodes']}
all_files = {pathlib.Path(e['filename']).name for e in entries}
new_files = {e['file'] for e in new['episodes']}
assert len(all_files) == len(entries), 'Duplicate manifest filenames'
assert old_files <= all_files, 'Archive entries removed; investigate separately'
assert new_files and new_files == all_files - old_files, 'Provide results for every new filename only'
assert len(new_files) == len(new['episodes']), 'Duplicate new episode filenames'
for result in (saved, new):
    s = result['stats']
    assert not s['pending_review'] and not s['parse_errors'] and not s['missing_files'], 'Finish review first'
assert all(e['file'] in new_files for e in new['events'])
saved['episodes'].extend(new['episodes'])
saved['episodes'].sort(key=lambda e: (-e['thread_events'], e['guest'], e['file']))
saved['events'].extend(new['events'])
assert len({e['id'] for e in saved['events']}) == len(saved['events'])
s = saved['stats']
s['previous_run_at'] = s['run_at']
s['run_at'] = new['stats']['run_at']
s['refresh_mode'] = 'new_transcripts_only'
s['new_transcripts_scanned'] = len(new_files)
s['previous_transcripts_reused'] = len(old_files)
s['episodes_scanned'] = len(saved['episodes'])
s['manifest_count'] = len(all_files)
s['date_min'] = min(e['date'] for e in saved['episodes'] if e['date'])
s['date_max'] = max(e['date'] for e in saved['episodes'] if e['date'])
s['reviewed_events'] = len(saved['events'])
s['literal_pull_events'] = sum(e['decision'] == 'pull' for e in saved['events'])
s['follow_events'] = sum(e['decision'] == 'follow' for e in saved['events'])
s['episodes_with_events'] = len({e['file'] for e in saved['events']})
for key in ('qualifying_speaking_turns', 'lenny_thread_turns'):
    s[key] += new['stats'][key]
path.write_text(json.dumps(saved, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(s, indent=2))
