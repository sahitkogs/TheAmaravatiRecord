#!/usr/bin/env python3
"""Build an HTML conflict reviewer for manual validation."""
import csv
import json
from collections import defaultdict

# ─── Load conflicts ──────────────────────────────────────────────────────────
with open('data/llm_conflicts.csv', encoding='utf-8') as f:
    conflicts = list(csv.DictReader(f))

# ─── Categorize ──────────────────────────────────────────────────────────────
CASTE_SUFFIXES = {'REDDY','NAIDU','CHOWDARY','CHOUDHARY','CHOWDARI','SETTY',
                  'SETTI','GOUD','VARMA','RAJU','NAYUDU'}
CHRISTIAN_NAMES = {'ISRAEL','JOHN','JOSEPH','DAVID','SAMUEL','MARY','DANIEL',
                   'PETER','SOLOMON','SALOMAN','MARIYADASU','PAUL','JAMES',
                   'THOMAS','MICHAEL','SELVARAJ','DANIYELU','YESU','ABRAHAM',
                   'SALOMANU','JACOB','MOSES','JERUSALEM','ELISAMMA','GLORY',
                   'YESUPADAM','HRUDAYAMARY','JAKKARAIAH','VICTOR','GABRIEL'}
MUSLIM_NAMES = {'AHMED','AHAMMAD','MOHAMMAD','MOHAMMED','BASHA','NOOR',
                'KHADAR','HUSSAIN','RAHAMAN','SUBHANI','MABU','FAKRUDDIN',
                'ISSAQ','CHAND'}

# Build unique entries
surname_data = {}
for c in conflicts:
    key = (c['surname'], c['directory_caste'], c['llm_caste'])
    if key not in surname_data:
        surname_data[key] = {
            'count': 0, 'conf': c['llm_confidence'],
            'examples': [], 'reasoning': c['reasoning']
        }
    surname_data[key]['count'] += 1
    if len(surname_data[key]['examples']) < 5:
        surname_data[key]['examples'].append(c['name'])

def categorize(surname, dir_c, llm_c, info):
    parts = set()
    for ex in info['examples']:
        parts.update(ex.upper().split())

    if any(s in parts for s in CASTE_SUFFIXES) and llm_c in ('Reddy','Kamma','Vysya','Kshatriya','Kapu'):
        return ('1', 'Caste Suffix Override', 'Name contains a caste suffix (Reddy, Naidu, etc.) that overrides the surname classification')
    if any(n in parts for n in CHRISTIAN_NAMES):
        return ('2', 'Christian Given Name', 'Given name suggests the person may be Christian regardless of surname caste')
    if any(n in parts for n in MUSLIM_NAMES):
        return ('3', 'Muslim Given Name', 'Given name suggests the person may be Muslim regardless of surname caste')
    if {dir_c, llm_c} == {'Kamma', 'Kapu'}:
        return ('4', 'Kamma vs Kapu', 'Surname is used by both communities - genuinely ambiguous')
    if llm_c == 'Other':
        return ('5', 'LLM Says Other', 'LLM could not confidently assign a caste - directory likely more reliable')
    if dir_c in ('Other', 'Unknown'):
        return ('6', 'Directory Was Other', 'Directory had no specific caste - LLM suggestion may help')
    if info['conf'] == 'high':
        return ('7', 'High Confidence Disagreement', 'LLM is highly confident the directory is wrong - needs review')
    if {dir_c, llm_c} & {'SC', 'ST'}:
        return ('8', 'SC/ST Dispute', 'Disagreement involving Scheduled Caste or Scheduled Tribe classification')
    if 'Brahmin' in (dir_c, llm_c):
        return ('9', 'Brahmin Dispute', 'Disagreement involving Brahmin classification')
    if 'Vysya' in (dir_c, llm_c):
        return ('10', 'Vysya Dispute', 'Disagreement involving Vysya classification')
    return ('11', 'Other', 'Other disagreements')

# Build categorized list
entries = []
for (surname, dir_c, llm_c), info in surname_data.items():
    cat_id, cat_name, cat_desc = categorize(surname, dir_c, llm_c, info)
    entries.append({
        'surname': surname,
        'directory_caste': dir_c,
        'llm_caste': llm_c,
        'confidence': info['conf'],
        'count': info['count'],
        'examples': info['examples'],
        'reasoning': info['reasoning'],
        'category_id': cat_id,
        'category': cat_name,
        'category_desc': cat_desc,
    })

# Sort: by category, then by count descending
entries.sort(key=lambda e: (e['category_id'], -e['count']))

data_json = json.dumps(entries)

# ─── Category summary ────────────────────────────────────────────────────────
cat_summary = defaultdict(lambda: {'count': 0, 'rows': 0})
for e in entries:
    cat_summary[e['category']]['count'] += 1
    cat_summary[e['category']]['rows'] += e['count']

cat_summary_json = json.dumps(dict(cat_summary))

# ─── Build HTML ──────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Conflict Reviewer — Amaravati Caste Analysis</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<style>
:root {{
  --paper: #faf8f4; --paper-tinted: #f0ece4;
  --ink: #1a1715; --ink-mid: #4a4540; --ink-light: #8a8580;
  --rule: #1a1715; --rule-light: #d4cfc8;
  --red: #8b1a1a; --green: #2d5f2d; --blue: #1a3a5f; --amber: #8b6914;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --paper: #1a1815; --paper-tinted: #242018;
    --ink: #e8e4dd; --ink-mid: #a8a49d; --ink-light: #706c65;
    --rule: #706c65; --rule-light: #3a3630;
    --red: #d4605a; --green: #6aaa6a; --blue: #6a9ad4; --amber: #d4a44a;
  }}
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: 'Source Serif 4', Georgia, serif; font-size: 15px; line-height: 1.6; color: var(--ink); background: var(--paper); }}
.container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
.header {{ text-align: center; border-top: 3px solid var(--rule); border-bottom: 3px solid var(--rule); padding: 16px 0; margin-bottom: 20px; }}
.header h1 {{ font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 900; }}
.header p {{ font-family: sans-serif; font-size: 12px; color: var(--ink-mid); margin-top: 4px; }}

/* Controls */
.controls {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; align-items: center; }}
.controls select, .controls input {{ padding: 8px 12px; border: 1px solid var(--rule-light); background: var(--paper-tinted); color: var(--ink); font-size: 14px; }}
.controls input {{ flex: 1; min-width: 200px; }}
.controls .count {{ font-family: sans-serif; font-size: 12px; color: var(--ink-light); }}

/* Category summary */
.cat-summary {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 8px; margin-bottom: 20px; }}
.cat-card {{ border: 1px solid var(--rule-light); padding: 10px; cursor: pointer; transition: background 0.15s; }}
.cat-card:hover {{ background: var(--paper-tinted); }}
.cat-card.active {{ border-color: var(--ink); background: var(--paper-tinted); }}
.cat-card__name {{ font-family: sans-serif; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--ink-mid); }}
.cat-card__num {{ font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 900; }}
.cat-card__sub {{ font-family: sans-serif; font-size: 10px; color: var(--ink-light); }}

/* Conflict cards */
.conflict {{ border: 1px solid var(--rule-light); padding: 14px; margin-bottom: 10px; }}
.conflict__header {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; flex-wrap: wrap; }}
.conflict__surname {{ font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; }}
.conflict__badge {{ font-family: sans-serif; font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; padding: 2px 8px; color: #fff; }}
.conflict__meta {{ font-family: sans-serif; font-size: 11px; color: var(--ink-mid); margin-top: 6px; }}
.conflict__arrow {{ display: flex; align-items: center; gap: 8px; margin: 8px 0; font-family: sans-serif; font-size: 13px; }}
.conflict__tag {{ padding: 3px 10px; font-weight: 700; font-size: 12px; }}
.dir-tag {{ background: var(--paper-tinted); border: 1px solid var(--rule-light); color: var(--ink); }}
.llm-tag {{ background: var(--blue); color: #fff; }}
.conflict__reasoning {{ font-size: 13px; color: var(--ink-mid); margin-top: 6px; font-style: italic; }}
.conflict__examples {{ font-family: sans-serif; font-size: 12px; color: var(--ink-light); margin-top: 6px; }}
.conflict__examples span {{ display: inline-block; background: var(--paper-tinted); padding: 1px 6px; margin: 2px 2px; border: 1px solid var(--rule-light); }}

/* Decision buttons */
.conflict__actions {{ display: flex; gap: 6px; margin-top: 10px; flex-wrap: wrap; }}
.conflict__actions button {{ padding: 6px 14px; border: 1px solid var(--rule-light); background: var(--paper-tinted); color: var(--ink); cursor: pointer; font-family: sans-serif; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; transition: all 0.15s; }}
.conflict__actions button:hover {{ background: var(--rule-light); }}
.conflict__actions button.chosen {{ background: var(--green); color: #fff; border-color: var(--green); }}

.pagination {{ display: flex; gap: 5px; align-items: center; justify-content: center; margin: 16px 0; }}
.pagination button {{ padding: 6px 14px; border: 1px solid var(--rule-light); background: var(--paper-tinted); color: var(--ink); cursor: pointer; font-family: sans-serif; font-size: 12px; }}
.pagination span {{ font-family: sans-serif; font-size: 12px; color: var(--ink-mid); }}

.footer {{ border-top: 3px solid var(--rule); padding-top: 10px; margin-top: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }}
.footer button {{ padding: 8px 16px; border: 1px solid var(--rule-light); background: var(--paper-tinted); color: var(--ink); cursor: pointer; font-family: sans-serif; font-size: 12px; }}
.footer .export {{ background: var(--blue); color: #fff; border-color: var(--blue); }}
.footer .info {{ font-family: sans-serif; font-size: 11px; color: var(--ink-light); }}

@media (max-width: 600px) {{
  .conflict__surname {{ font-size: 17px; }}
  .cat-summary {{ grid-template-columns: repeat(2, 1fr); }}
  body {{ font-size: 16px; }}
}}
</style>
</head>
<body>
<div class="container">

<div class="header">
  <h1>Conflict Reviewer</h1>
  <p>{len(entries)} unique conflicts across {len(cat_summary)} categories &mdash; review and decide which classification is correct</p>
</div>

<div class="cat-summary" id="cat-summary"></div>

<div class="controls">
  <select id="filter-cat" onchange="applyFilter()">
    <option value="">All Categories</option>
  </select>
  <select id="filter-conf" onchange="applyFilter()">
    <option value="">All Confidence</option>
    <option value="high">High</option>
    <option value="medium">Medium</option>
    <option value="low">Low</option>
  </select>
  <input type="text" id="search" placeholder="Search surname..." oninput="applyFilter()">
  <span class="count" id="count"></span>
</div>

<div id="cards"></div>
<div class="pagination" id="pagination"></div>

<div class="footer">
  <div class="info" id="decided-count">Decisions: 0 / {len(entries)}</div>
  <div style="display:flex;gap:8px;">
    <button class="export" onclick="exportCSV()">Export Decisions CSV</button>
    <button onclick="if(confirm('Clear all decisions?')){{decisions={{}};save();render();}}">Reset</button>
  </div>
</div>

</div>

<script>
const DATA = {data_json};
const CAT_SUMMARY = {cat_summary_json};
const STORAGE_KEY = 'amaravati_conflict_decisions';

let decisions = {{}};
try {{ decisions = JSON.parse(localStorage.getItem(STORAGE_KEY)) || {{}}; }} catch(e) {{ decisions = {{}}; }}

let filtered = DATA;
let page = 0;
const PS = 30;

function save() {{ localStorage.setItem(STORAGE_KEY, JSON.stringify(decisions)); }}

// Category summary cards
function renderCatSummary() {{
  const el = document.getElementById('cat-summary');
  const sel = document.getElementById('filter-cat');
  let html = '';
  let opts = '<option value="">All Categories</option>';
  const cats = [...new Set(DATA.map(d => d.category))];
  cats.forEach(cat => {{
    const items = DATA.filter(d => d.category === cat);
    const rows = items.reduce((s,d) => s + d.count, 0);
    html += '<div class="cat-card" onclick="filterByCat(\\'' + cat + '\\')" id="cat-' + cat.replace(/\\s/g,'_') + '">' +
      '<div class="cat-card__name">' + cat + '</div>' +
      '<div class="cat-card__num">' + items.length + '</div>' +
      '<div class="cat-card__sub">' + rows + ' rows</div></div>';
    opts += '<option value="' + cat + '">' + cat + ' (' + items.length + ')</option>';
  }});
  el.innerHTML = html;
  sel.innerHTML = opts;
}}

function filterByCat(cat) {{
  document.getElementById('filter-cat').value = cat;
  applyFilter();
}}

function applyFilter() {{
  const cat = document.getElementById('filter-cat').value;
  const conf = document.getElementById('filter-conf').value;
  const q = document.getElementById('search').value.toLowerCase();

  filtered = DATA.filter(d => {{
    if (cat && d.category !== cat) return false;
    if (conf && d.confidence !== conf) return false;
    if (q && !d.surname.toLowerCase().includes(q)) return false;
    return true;
  }});

  // Highlight active category
  document.querySelectorAll('.cat-card').forEach(c => c.classList.remove('active'));
  if (cat) {{
    const el = document.getElementById('cat-' + cat.replace(/\\s/g,'_'));
    if (el) el.classList.add('active');
  }}

  document.getElementById('count').textContent = filtered.length + ' conflicts';
  page = 0;
  render();
}}

function render() {{
  const start = page * PS;
  const end = Math.min(start + PS, filtered.length);
  let html = '';

  for (let i = start; i < end; i++) {{
    const d = filtered[i];
    const key = d.surname + '|' + d.directory_caste + '|' + d.llm_caste;
    const decision = decisions[key] || '';
    const confColor = d.confidence === 'high' ? 'var(--red)' : d.confidence === 'medium' ? 'var(--amber)' : 'var(--ink-light)';

    html += '<div class="conflict">';
    html += '<div class="conflict__header">';
    html += '<div class="conflict__surname">' + d.surname + '</div>';
    html += '<span class="conflict__badge" style="background:' + confColor + '">' + d.confidence + ' &middot; ' + d.count + ' plots</span>';
    html += '</div>';
    html += '<div class="conflict__meta">' + d.category + '</div>';
    html += '<div class="conflict__arrow">';
    html += '<span class="conflict__tag dir-tag">Directory: ' + d.directory_caste + '</span>';
    html += '<span style="color:var(--ink-light)">&rarr;</span>';
    html += '<span class="conflict__tag llm-tag">LLM: ' + d.llm_caste + '</span>';
    html += '</div>';
    html += '<div class="conflict__reasoning">"' + d.reasoning + '"</div>';
    html += '<div class="conflict__examples">Example names: ' + d.examples.map(e => '<span>' + e + '</span>').join('') + '</div>';
    html += '<div class="conflict__actions">';
    html += '<button class="' + (decision === 'keep_directory' ? 'chosen' : '') + '" onclick="decide(\\'' + key + '\\',\\'keep_directory\\')">Keep Directory (' + d.directory_caste + ')</button>';
    html += '<button class="' + (decision === 'accept_llm' ? 'chosen' : '') + '" onclick="decide(\\'' + key + '\\',\\'accept_llm\\')">Accept LLM (' + d.llm_caste + ')</button>';
    html += '<button class="' + (decision === 'skip' ? 'chosen' : '') + '" onclick="decide(\\'' + key + '\\',\\'skip\\')">Skip</button>';
    html += '</div>';
    html += '</div>';
  }}

  document.getElementById('cards').innerHTML = html;
  updateDecidedCount();
  renderPagination();
}}

function decide(key, value) {{
  decisions[key] = value;
  save();
  render();
}}

function updateDecidedCount() {{
  const total = DATA.length;
  const done = Object.keys(decisions).length;
  document.getElementById('decided-count').textContent = 'Decisions: ' + done + ' / ' + total;
}}

function renderPagination() {{
  const tp = Math.ceil(filtered.length / PS);
  const el = document.getElementById('pagination');
  if (tp <= 1) {{ el.innerHTML = ''; return; }}
  el.innerHTML = '<button onclick="gp(0)">&laquo;</button>' +
    '<button onclick="gp(' + Math.max(0,page-1) + ')">&lsaquo;</button>' +
    '<span>Page ' + (page+1) + ' / ' + tp + '</span>' +
    '<button onclick="gp(' + Math.min(tp-1,page+1) + ')">&rsaquo;</button>' +
    '<button onclick="gp(' + (tp-1) + ')">&raquo;</button>';
}}
function gp(p) {{ page = p; render(); window.scrollTo(0, 0); }}

function exportCSV() {{
  let csv = 'surname,directory_caste,llm_caste,confidence,count,decision\\n';
  DATA.forEach(d => {{
    const key = d.surname + '|' + d.directory_caste + '|' + d.llm_caste;
    csv += d.surname + ',' + d.directory_caste + ',' + d.llm_caste + ',' + d.confidence + ',' + d.count + ',' + (decisions[key]||'') + '\\n';
  }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([csv], {{type:'text/csv'}}));
  a.download = 'conflict_decisions.csv';
  a.click();
}}

renderCatSummary();
applyFilter();
</script>
</body>
</html>"""

with open('reports/conflict_reviewer.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Created reports/conflict_reviewer.html ({len(entries)} conflicts)")
