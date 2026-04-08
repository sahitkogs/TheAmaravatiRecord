#!/usr/bin/env python3
"""Build an HTML explorer for the surname ground truth corpus."""
import csv
import json
import os
import re
from collections import defaultdict, Counter

# ─── Load ground truth ──────────────────────────────────────────────────────
surnames_data = defaultdict(lambda: {'castes': {}, 'total_sources': 0, 'examples': defaultdict(list)})

with open('data/surname_ground_truth.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        s = row['surname'].strip().upper()
        c = row['caste'].strip()
        url = row['source_url'].strip()

        if len(s) <= 2 or re.search(r'[^A-Z]', s):
            continue

        if c not in surnames_data[s]['castes']:
            surnames_data[s]['castes'][c] = []
        surnames_data[s]['castes'][c].append(url)
        surnames_data[s]['total_sources'] += 1

# ─── Load Gemini classification for example full names ───────────────────────
gemini_examples = defaultdict(lambda: defaultdict(list))  # surname -> caste -> [full names]
gemini_path = 'data/gemini_name_caste_map.json'
if os.path.exists(gemini_path):
    with open(gemini_path, encoding='utf-8') as f:
        gemini_map = json.load(f)
    for full_name, info in gemini_map.items():
        parts = full_name.replace('.', ' ').split()
        if not parts:
            continue
        surname = parts[0].upper().strip('.-')
        if len(surname) <= 2:
            continue
        caste = info.get('caste', 'Unknown')
        if surname in surnames_data and len(gemini_examples[surname][caste]) < 5:
            gemini_examples[surname][caste].append(full_name)

# ─── Load MyNeta SC examples ────────────────────────────────────────────────
myneta_path = 'data/raw/myneta_sc_candidates.json'
if os.path.exists(myneta_path):
    with open(myneta_path, encoding='utf-8') as f:
        myneta_records = json.load(f)
    for rec in myneta_records:
        s = rec['surname']
        if s in surnames_data and len(gemini_examples[s]['SC']) < 5:
            gemini_examples[s]['SC'].append(rec['full_name'])

# ─── Load detected first names for flagging ─────────────────────────────────
detected_first_names = set()
detected_path = 'data/detected_first_names.json'
if os.path.exists(detected_path):
    with open(detected_path, encoding='utf-8') as f:
        detected_data = json.load(f)
    detected_first_names = set(detected_data.get('first_names', []))

# ─── Build JSON for HTML ────────────────────────────────────────────────────
all_castes = sorted(set(c for d in surnames_data.values() for c in d['castes']))
entries = []
for surname, data in sorted(surnames_data.items()):
    caste_list = []
    for c in all_castes:
        if c in data['castes']:
            urls = list(set(data['castes'][c]))
            examples = gemini_examples.get(surname, {}).get(c, [])
            caste_list.append({'caste': c, 'sources': len(urls), 'urls': urls, 'examples': examples[:3]})
    # Also add Gemini-only castes (person classified as a caste not in ground truth)
    for c, names in gemini_examples.get(surname, {}).items():
        if c not in data['castes'] and c not in ('Unknown', 'Other'):
            caste_list.append({'caste': c, 'sources': 0, 'urls': [], 'examples': names[:3], 'gemini_only': True})
    # Skip detected first names entirely
    if surname in detected_first_names:
        continue

    entries.append({
        'surname': surname,
        'castes': caste_list,
        'num_castes': len(data['castes']),
        'total_sources': data['total_sources'],
    })

# Stats for overview
stats = {
    'total_surnames': len(entries),
    'castes': {},
    'overlap': {
        'exclusive': sum(1 for e in entries if e['num_castes'] == 1),
        'shared_2': sum(1 for e in entries if e['num_castes'] == 2),
        'shared_3': sum(1 for e in entries if e['num_castes'] == 3),
        'shared_4plus': sum(1 for e in entries if e['num_castes'] >= 4),
    }
}
for c in all_castes:
    total = sum(1 for e in entries if any(x['caste'] == c for x in e['castes']))
    exclusive = sum(1 for e in entries if e['num_castes'] == 1 and e['castes'][0]['caste'] == c)
    shared = total - exclusive
    stats['castes'][c] = {'total': total, 'exclusive': exclusive, 'shared': shared}

# Overlap matrix
overlap_matrix = {}
for c1 in all_castes:
    overlap_matrix[c1] = {}
    s1 = set(e['surname'] for e in entries if any(x['caste'] == c1 for x in e['castes']))
    for c2 in all_castes:
        s2 = set(e['surname'] for e in entries if any(x['caste'] == c2 for x in e['castes']))
        overlap_matrix[c1][c2] = len(s1 & s2)

caste_colors = {
    'Kamma': '#8b1a1a', 'Kapu': '#1a3a5f', 'Reddy': '#2d5f2d',
    'Brahmin': '#8b6914', 'Vysya': '#5f1a5f', 'Muslim': '#1a5f5f',
    'SC': '#8b5e14', 'ST': '#3a3a3a', 'Velama': '#6b3a1a',
    'Kshatriya': '#5f2d2d', 'Yadava': '#2d5f3a',
}

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Surname Ground Truth Explorer</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
:root {{
  --paper: #faf8f4; --paper-tinted: #f0ece4;
  --ink: #1a1715; --ink-mid: #4a4540; --ink-light: #8a8580;
  --rule: #1a1715; --rule-light: #d4cfc8;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --paper: #1a1815; --paper-tinted: #242018;
    --ink: #e8e4dd; --ink-mid: #a8a49d; --ink-light: #706c65;
    --rule: #706c65; --rule-light: #3a3630;
  }}
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: 'Source Serif 4', Georgia, serif; font-size: 15px; color: var(--ink); background: var(--paper); }}
.container {{ max-width: 1000px; margin: 0 auto; padding: 20px; }}
.header {{ text-align: center; border-top: 3px solid var(--rule); border-bottom: 3px solid var(--rule); padding: 16px 0; margin-bottom: 20px; }}
.header h1 {{ font-family: 'Playfair Display', serif; font-size: 32px; font-weight: 900; }}
.header p {{ font-family: sans-serif; font-size: 12px; color: var(--ink-mid); margin-top: 4px; }}

.stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 20px; }}
.stat {{ border: 1px solid var(--rule-light); padding: 12px; text-align: center; }}
.stat__num {{ font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 900; }}
.stat__label {{ font-family: sans-serif; font-size: 9px; text-transform: uppercase; letter-spacing: 1px; color: var(--ink-mid); }}

.section {{ margin-bottom: 24px; }}
.section h2 {{ font-family: 'Playfair Display', serif; font-size: 20px; margin-bottom: 10px; border-bottom: 1.5px solid var(--rule); padding-bottom: 6px; }}

.chart-box {{ border: 1px solid var(--rule-light); padding: 12px; margin-bottom: 16px; }}

.controls {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; align-items: center; }}
.controls input, .controls select {{ padding: 8px 12px; border: 1px solid var(--rule-light); background: var(--paper-tinted); color: var(--ink); font-size: 14px; }}
.controls input {{ flex: 1; min-width: 200px; }}
.controls .count {{ font-family: sans-serif; font-size: 11px; color: var(--ink-light); }}

.caste-filters {{ display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }}
.caste-btn {{ padding: 6px 14px; border: 1px solid var(--rule-light); background: var(--paper-tinted); color: var(--ink); cursor: pointer; font-family: sans-serif; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; transition: all 0.15s; }}
.caste-btn:hover {{ opacity: 0.8; }}
.caste-btn.active {{ color: #fff; }}

table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th {{ background: var(--paper-tinted); font-family: sans-serif; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: var(--ink-mid); padding: 8px; text-align: left; position: sticky; top: 0; cursor: pointer; }}
td {{ padding: 6px 8px; border-bottom: 1px solid var(--rule-light); }}
tr:hover td {{ background: var(--paper-tinted); }}
.table-wrap {{ max-height: 500px; overflow-y: auto; border: 1px solid var(--rule-light); }}

.tag {{ display: inline-block; padding: 2px 6px; font-family: sans-serif; font-size: 9px; font-weight: 700; color: #fff; margin: 1px; border-radius: 2px; cursor: pointer; }}
.tag:hover {{ opacity: 0.8; }}
.overlap-badge {{ background: var(--paper-tinted); border: 1px solid var(--rule-light); color: var(--ink); padding: 1px 5px; font-family: sans-serif; font-size: 9px; font-weight: 700; }}

.quality {{ border: 1px solid #d4a44a; background: #3a3020; padding: 14px; margin-bottom: 16px; color: #d4a44a; font-size: 13px; }}
.quality h3 {{ margin-bottom: 8px; }}
.quality ul {{ padding-left: 20px; }}

.pagination {{ display: flex; gap: 5px; align-items: center; justify-content: center; margin-top: 10px; }}
.pagination button {{ padding: 6px 12px; border: 1px solid var(--rule-light); background: var(--paper-tinted); color: var(--ink); cursor: pointer; font-size: 12px; }}
.pagination span {{ font-family: sans-serif; font-size: 11px; color: var(--ink-mid); }}

.footer {{ font-family: sans-serif; font-size: 9px; text-transform: uppercase; letter-spacing: 1px; color: var(--ink-light); border-top: 3px solid var(--rule); padding-top: 10px; text-align: center; margin-top: 24px; }}

@media (max-width: 600px) {{
  body {{ font-size: 16px; }}
  .header h1 {{ font-size: 24px; }}
  table {{ font-size: 14px; }}
}}
</style>
</head>
<body>
<div class="container">

<div class="header">
  <h1>Surname Ground Truth Explorer</h1>
  <p>{stats['total_surnames']:,} surnames &middot; {len(all_castes)} castes &middot; {len([e for e in entries if e['num_castes'] > 1])} shared across castes</p>
</div>

<div class="stats">
  <div class="stat"><div class="stat__num">{stats['total_surnames']:,}</div><div class="stat__label">Total Surnames</div></div>
  <div class="stat"><div class="stat__num">{stats['overlap']['exclusive']:,}</div><div class="stat__label">Exclusive (1 caste)</div></div>
  <div class="stat"><div class="stat__num">{stats['overlap']['shared_2']:,}</div><div class="stat__label">Shared (2 castes)</div></div>
  <div class="stat"><div class="stat__num">{stats['overlap']['shared_3']:,}</div><div class="stat__label">Shared (3 castes)</div></div>
  <div class="stat"><div class="stat__num">{stats['overlap']['shared_4plus']:,}</div><div class="stat__label">Shared (4+ castes)</div></div>
</div>

<div class="section">
  <h2>Caste Distribution</h2>
  <div class="chart-box"><div id="chart-dist"></div></div>
</div>

<div class="section">
  <h2>Overlap Matrix</h2>
  <p style="font-family:sans-serif;font-size:11px;color:var(--ink-mid);margin-bottom:8px;">Number of surnames shared between each pair of castes</p>
  <div class="chart-box"><div id="chart-matrix"></div></div>
</div>

<div class="section">
  <h2>Browse Surnames</h2>
  <div class="controls">
    <input type="text" id="search" placeholder="Search surname..." oninput="filterData()">
    <select id="overlap-filter" onchange="filterData()">
      <option value="">All</option>
      <option value="1">Exclusive (1 caste only)</option>
      <option value="2">Shared by 2+ castes</option>
      <option value="3">Shared by 3+ castes</option>
      <option value="4">Shared by 4+ castes</option>
    </select>
    <span class="count" id="count"></span>
  </div>
  <div class="caste-filters" id="caste-filters"></div>
  <div class="table-wrap">
    <table>
      <thead><tr>
        <th onclick="sortBy('surname')">Surname</th>
        <th onclick="sortBy('num_castes')">Castes</th>
        <th>Caste Tags</th>
        <th onclick="sortBy('total_sources')">Sources</th>
      </tr></thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>
  <div class="pagination" id="pagination"></div>
</div>

<div class="footer">
  Surname Ground Truth Corpus &middot; {stats['total_surnames']:,} surnames from 19 sources &middot; Data for research purposes only
</div>

</div>

<script>
const DATA = {json.dumps(entries)};
const CASTES = {json.dumps(all_castes)};
const STATS = {json.dumps(stats)};
const MATRIX = {json.dumps(overlap_matrix)};
const COLORS = {json.dumps(caste_colors)};

let filtered = DATA;
let activeCaste = '';
let sortKey = 'num_castes';
let sortAsc = false;
let page = 0;
const PS = 50;

// Caste filter buttons
const filtersEl = document.getElementById('caste-filters');
let btnsHtml = '<button class="caste-btn active" onclick="setCaste(\\'\\')" style="background:var(--ink);color:var(--paper)">All</button>';
CASTES.forEach(c => {{
  const color = COLORS[c] || '#666';
  btnsHtml += '<button class="caste-btn" onclick="setCaste(\\'' + c + '\\')" data-caste="' + c + '" style="border-color:' + color + '">' + c + ' (' + STATS.castes[c].total + ')</button>';
}});
filtersEl.innerHTML = btnsHtml;

function setCaste(c) {{
  activeCaste = c;
  document.querySelectorAll('.caste-btn').forEach(b => {{
    b.classList.remove('active');
    if (c && b.dataset.caste === c) {{
      b.classList.add('active');
      b.style.background = COLORS[c] || '#666';
      b.style.color = '#fff';
    }} else if (!c && !b.dataset.caste) {{
      b.classList.add('active');
    }} else {{
      b.style.background = 'var(--paper-tinted)';
      b.style.color = 'var(--ink)';
    }}
  }});
  filterData();
}}

function filterData() {{
  const q = document.getElementById('search').value.toLowerCase();
  const overlap = document.getElementById('overlap-filter').value;

  filtered = DATA.filter(e => {{
    if (q && !e.surname.toLowerCase().includes(q)) return false;
    if (overlap && e.num_castes < parseInt(overlap)) return false;
    if (activeCaste && !e.castes.some(c => c.caste === activeCaste)) return false;
    return true;
  }});

  document.getElementById('count').textContent = filtered.length + ' surnames';
  page = 0;
  render();
}}

function sortBy(key) {{
  if (sortKey === key) sortAsc = !sortAsc;
  else {{ sortKey = key; sortAsc = key === 'surname'; }}
  filtered.sort((a, b) => {{
    const va = a[key], vb = b[key];
    return sortAsc ? (va < vb ? -1 : 1) : (va > vb ? -1 : 1);
  }});
  page = 0;
  render();
}}

function render() {{
  const start = page * PS;
  const end = Math.min(start + PS, filtered.length);
  let html = '';
  for (let i = start; i < end; i++) {{
    const e = filtered[i];
    const tags = e.castes.map(c => {{
      const geminiFlag = c.gemini_only ? ' *' : '';
      return '<span class="tag" style="background:' + (COLORS[c.caste]||'#666') + '" title="' + c.sources + ' source(s)">' + c.caste + geminiFlag + '</span>';
    }}).join('');
    const badge = e.num_castes > 1 ? ' <span class="overlap-badge">' + e.num_castes + ' castes</span>' : '';
    const rowId = 'detail-' + i;

    html += '<tr onclick="toggleDetail(\\'' + rowId + '\\')" style="cursor:pointer"><td><strong>' + e.surname + '</strong>' + badge + '</td><td>' + e.num_castes + '</td><td>' + tags + '</td><td>' + e.total_sources + '</td></tr>';

    // Expandable detail row
    let detailHtml = '<tr id="' + rowId + '" style="display:none"><td colspan="4" style="padding:12px;background:var(--paper-tinted);border:1px solid var(--rule-light)">';
    e.castes.forEach(c => {{
      const color = COLORS[c.caste] || '#666';
      detailHtml += '<div style="margin-bottom:10px;padding:8px;border-left:3px solid ' + color + '">';
      detailHtml += '<div style="font-family:sans-serif;font-size:11px;font-weight:700;color:' + color + ';text-transform:uppercase;letter-spacing:1px">' + c.caste;
      if (c.gemini_only) detailHtml += ' <span style="font-size:9px;color:var(--ink-light)">(Gemini classification only, not in ground truth)</span>';
      detailHtml += '</div>';

      // Sources
      if (c.urls && c.urls.length > 0) {{
        detailHtml += '<div style="font-family:sans-serif;font-size:11px;color:var(--ink-mid);margin-top:4px"><strong>Sources (' + c.sources + '):</strong></div>';
        c.urls.forEach(url => {{
          const short = url.length > 60 ? url.substring(0, 57) + '...' : url;
          detailHtml += '<div style="font-family:sans-serif;font-size:10px;margin-left:8px"><a href="' + url + '" target="_blank" style="color:var(--ink-light)">' + short + '</a></div>';
        }});
      }}

      // Example full names
      if (c.examples && c.examples.length > 0) {{
        detailHtml += '<div style="font-family:sans-serif;font-size:11px;color:var(--ink-mid);margin-top:4px"><strong>Example names:</strong></div>';
        c.examples.forEach(name => {{
          detailHtml += '<div style="font-family:sans-serif;font-size:12px;margin-left:8px;color:var(--ink)">' + name + '</div>';
        }});
      }}
      detailHtml += '</div>';
    }});
    detailHtml += '</td></tr>';
    html += detailHtml;
  }}
  document.getElementById('tbody').innerHTML = html;

  const tp = Math.ceil(filtered.length / PS);
  const pg = document.getElementById('pagination');
  if (tp <= 1) {{ pg.innerHTML = ''; return; }}
  pg.innerHTML = '<button onclick="gp(0)">&laquo;</button><button onclick="gp(' + Math.max(0,page-1) + ')">&lsaquo;</button><span>Page ' + (page+1) + ' / ' + tp + '</span><button onclick="gp(' + Math.min(tp-1,page+1) + ')">&rsaquo;</button><button onclick="gp(' + (tp-1) + ')">&raquo;</button>';
}}
function gp(p) {{ page = p; render(); window.scrollTo(0, document.querySelector('.table-wrap').offsetTop - 100); }}

function toggleDetail(id) {{
  const el = document.getElementById(id);
  if (el) el.style.display = el.style.display === 'none' ? '' : 'none';
}}

// Charts
function renderCharts() {{
  const castes = CASTES;
  const colors = castes.map(c => COLORS[c] || '#666');

  // Distribution bar
  Plotly.newPlot('chart-dist', [
    {{
      type: 'bar', orientation: 'h', name: 'Exclusive',
      y: castes, x: castes.map(c => STATS.castes[c].exclusive),
      marker: {{ color: colors }},
      hovertemplate: '%{{y}}: %{{x}} exclusive<extra></extra>',
    }},
    {{
      type: 'bar', orientation: 'h', name: 'Shared',
      y: castes, x: castes.map(c => STATS.castes[c].shared),
      marker: {{ color: colors.map(c => c + '88') }},
      hovertemplate: '%{{y}}: %{{x}} shared<extra></extra>',
    }}
  ], {{
    barmode: 'stack',
    paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
    font: {{ color: getComputedStyle(document.documentElement).getPropertyValue('--ink').trim() || '#1a1715', size: 12 }},
    margin: {{ t: 10, b: 30, l: 80, r: 20 }},
    height: 300,
    legend: {{ orientation: 'h', y: -0.1, font: {{ size: 10 }} }},
    xaxis: {{ title: 'Number of surnames' }},
  }}, {{ responsive: true, displayModeBar: false }});

  // Overlap heatmap
  const z = castes.map(c1 => castes.map(c2 => c1 === c2 ? 0 : MATRIX[c1][c2]));
  Plotly.newPlot('chart-matrix', [{{
    z: z, x: castes, y: castes, type: 'heatmap',
    colorscale: [[0,'#faf8f4'],[0.1,'#fcbba1'],[0.3,'#fb6a4a'],[0.6,'#cb181d'],[1,'#67000d']],
    hovertemplate: '%{{y}} & %{{x}}: %{{z}} shared<extra></extra>',
    text: z.map(row => row.map(v => v > 0 ? v.toString() : '')),
    texttemplate: '%{{text}}',
  }}], {{
    paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
    font: {{ color: getComputedStyle(document.documentElement).getPropertyValue('--ink').trim() || '#1a1715', size: 11 }},
    margin: {{ t: 10, b: 80, l: 80, r: 20 }},
    height: 400,
    xaxis: {{ tickangle: -45 }},
  }}, {{ responsive: true, displayModeBar: false }});
}}

// Init
sortBy('num_castes');
filterData();
renderCharts();
</script>
</body>
</html>"""

with open('reports/surname_explorer.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Created reports/surname_explorer.html")
print(f"  {len(entries)} surnames, {len(all_castes)} castes")
print(f"  Quality filtered: removed {len(surnames_data) - len(entries)} bad entries")
