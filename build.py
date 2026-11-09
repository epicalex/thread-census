#!/usr/bin/env python3
"""Regenerate static HTML from reviewed derived data. No raw transcripts are published."""
import json,html,pathlib,datetime,collections
from hero_yarn import render as render_hero_yarn, render_ball
base=pathlib.Path(__file__).resolve().parent
r=json.loads((base/'data/thread-results.json').read_text())
assert not r['stats']['pending_review'] and not r['stats']['parse_errors'] and not r['stats']['missing_files'], 'Finish reviewing the archive before publishing.'
esc=lambda s:html.escape(str(s or ''))
def name(e):return 'Noam Segal (AI sentiment survey)' if e['file']=='noam-segal.md' else e['guest']
def date(s):return datetime.date.fromisoformat(s).strftime('%d %b %Y') if s else 'Undated'
def link(text,url):return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(text)} <span aria-hidden="true">↗</span></a>' if url else esc(text)
leaders=[]
for e in sorted(r['episodes'],key=lambda e:(-e['thread_events'],name(e))):
 if e['thread_events']<2:continue
 leaders.append(f'<tr><td>{link(name(e),e.get("youtube_url"))}</td><td><time datetime="{esc(e["date"])}">{date(e["date"])}</time></td><td class="score"><span class="bar" style="--amount:{e["thread_events"]/4*100}%"></span><b>{e["thread_events"]}</b></td></tr>')
events=[]
for e in sorted(sorted(r['events'],key=lambda e:(name(e),e['seconds'] or 0)),key=lambda e:e['date'] or '',reverse=True):
 events.append(f'<tr data-kind="{e["decision"]}"><td><strong>{esc(name(e))}</strong><time class="guest-date" datetime="{esc(e["date"])}">{date(e["date"])}</time></td><td>{link(e["timestamp"],e["source_url"])}</td><td><span class="tag {e["decision"]}">{e["decision"]}</span></td><td>{esc(e["summary"])}</td></tr>')
last_pull=max((e for e in r['events'] if e['decision']=='pull' and e['date']),key=lambda e:(e['date'],e['seconds'] or 0))
since_pull=sum(bool(e['date'] and e['date']>last_pull['date']) for e in r['episodes'])
last_follow=max((e for e in r['events'] if e['decision']=='follow' and e['date']),key=lambda e:(e['date'],e['seconds'] or 0))
since_follow=sum(bool(e['date'] and e['date']>last_follow['date']) for e in r['episodes'])
theme_review=json.loads((base/'data/thread-themes-review.json').read_text())
assert set(theme_review['assignments'])=={e['id'] for e in r['events']}, 'Update the topic review before building.'
theme_counts=collections.Counter()
for event in r['events']:
 assignment=theme_review['assignments'][event['id']]
 assert assignment['text_sha256']==event['text_sha256'] and assignment['summary']==event['summary'], 'Update changed topic review.'
 theme_counts[assignment['theme']]+=1
theme_rows=''
for key,count in theme_counts.most_common():
 label=theme_review['themes'][key]['label']
 theme_rows+=f'<li><div><span>{esc(label)}</span><b>{count} <small>({count/len(r["events"]):.0%})</small></b></div><span class="theme-track" aria-hidden="true"><span style="width:{100*count/len(r["events"]):.2f}%"></span></span></li>'
s=r['stats'];template=(base/'template.html').read_text()
for key,value in {'HERO_BALL':render_ball(),'HERO_YARN':render_hero_yarn(),'FLIP_DIGITS':''.join(f'<span class="flip-digit" aria-hidden="true">{digit}</span>' for digit in str(since_pull).zfill(2)),'CHANCE':f"{100*s['episodes_with_events']/s['episodes_scanned']:.1f}",'THEME_ROWS':theme_rows,'SINCE_PULL_TEXT':since_pull,'SINCE_PULL':str(since_pull).zfill(2),'SINCE_FOLLOW':since_follow,'LAST_PULL':link(name(last_pull)+' · '+last_pull['timestamp'],last_pull['source_url']),'LAST_PULL_DATE':date(last_pull['date']),'LAST_PULL_TOPIC':esc(last_pull['summary']),'LEADERS':'\n'.join(leaders),'EVENTS':'\n'.join(events),'TOTAL':s['reviewed_events'],'PULL':s['literal_pull_events'],'FOLLOW':s['follow_events'],'EPISODES':s['episodes_with_events'],'SCANNED':s['episodes_scanned']}.items():template=template.replace('{{'+key+'}}',str(value))
(base/'index.html').write_text(template)
print(f'Built index.html: {len(leaders)} leaderboard rows, {len(events)} moments')
