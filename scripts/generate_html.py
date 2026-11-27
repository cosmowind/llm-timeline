#!/usr/bin/env python3
"""生成 LLM 时间线 HTML 页面"""
import json, csv
from pathlib import Path

csv_path = Path("/www/wwwroot/projects/llm-timeline/data/llm_timeline.csv")
out_path = Path("/www/wwwroot/projects/llm-timeline/show/index.html")

# Read from CSV (already sorted by date in CSV)
models = []
with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # description is a plain string
        row['description'] = row.get('description', '')
        # Parse params as int or None (may have B/T suffix)
        raw_params = row['params'].strip()
        if raw_params:
            # Remove B/T suffix and convert
            num = raw_params.upper().rstrip('BT')
            try:
                val = float(num)
                row['params'] = int(val) if val == int(val) else val
            except:
                row['params'] = raw_params  # keep as string if non-numeric
        else:
            row['params'] = None
        # Parse open_weights
        if row['open_weights'] == 'True':
            row['open_weights'] = True
        elif row['open_weights'] == 'False':
            row['open_weights'] = False
        else:
            row['open_weights'] = None
        # Parse tags
        if row['tags']:
            row['tags'] = row['tags'].split(',')
        else:
            row['tags'] = []
        models.append(row)

# CSV is already sorted by date+name, no resort needed
models_js = json.dumps(models, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 LLM 模型时间线 - 大模型演进史</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        primary: '#6366f1',
                        secondary: '#8b5cf6',
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
        .timeline-item:hover .model-card {{ transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.12); }}
        .timeline-item:hover .year-badge {{ transform: scale(1.1); }}
        .model-card {{ transition: all 0.2s ease; }}
        .year-badge {{ transition: transform 0.2s ease; }}
        .company-tag {{ transition: all 0.15s; }}
        .company-tag:hover {{ transform: scale(1.05); }}
        .dot {{ position: absolute; left: 50%; transform: translateX(-50%); width: 12px; height: 12px; border-radius: 50%; background: #6366f1; border: 3px solid white; box-shadow: 0 0 0 2px #6366f1; }}
    </style>
</head>
<body class="bg-gray-50 dark:bg-gray-900 min-h-screen">
    <header class="bg-white dark:bg-gray-800 shadow-sm sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-4">
            <div class="flex items-center justify-between flex-wrap gap-3">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">🤖 LLM 模型时间线</h1>
                    <p class="text-sm text-gray-500 dark:text-gray-400">大模型发布历史 · 2018-2026 · 共 {len(models)} 个模型</p>
                </div>
                <div class="flex items-center gap-3 flex-wrap">
                    <select id="orgFilter" class="px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm">
                        <option value="">全部公司</option>
                    </select>
                    <select id="catFilter" class="px-3 py-1.5 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm">
                        <option value="">全部类别</option>
                    </select>
                    <span id="stats" class="text-sm text-gray-500 dark:text-gray-400"></span>
                </div>
            </div>
        </div>
    </header>

    <div class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white py-3">
        <div class="max-w-7xl mx-auto px-4 flex items-center justify-center gap-6 text-sm font-medium">
            <span>📊 <span id="totalModels">0</span> 个模型</span>
            <span>🏢 <span id="totalOrgs">0</span> 家公司</span>
            <span>📅 <span id="yearRange">0</span> 年跨度</span>
        </div>
    </div>

    <main class="max-w-7xl mx-auto px-4 py-8">
        <div id="timeline" class="relative"></div>
    </main>

    <footer class="text-center py-8 text-sm text-gray-400">
        <p>数据来源: awesome-ai-models + frontier + 公开资料整理 | 更新于 2025-05-12</p>
    </footer>

    <script>
    const MODELS = {models_js};

    const COLORS = {{
        'OpenAI': 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-200',
        'Google': 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200',
        'Meta': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
        'Anthropic': 'bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-200',
        'DeepSeek': 'bg-cyan-100 text-cyan-700 dark:bg-cyan-900 dark:text-cyan-200',
        'Alibaba': 'bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-200',
        'xAI': 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-200',
        'Mistral AI': 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-200',
        'Mistral': 'bg-indigo-50 text-indigo-600 dark:bg-indigo-950 dark:text-indigo-300',
        'ByteDance': 'bg-pink-100 text-pink-700 dark:bg-pink-900 dark:text-pink-200',
        'Baidu': 'bg-red-50 text-red-600 dark:bg-red-950 dark:text-red-300',
        'iFlytek': 'bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-300',
        'Moonshot AI': 'bg-purple-50 text-purple-600 dark:bg-purple-950 dark:text-purple-300',
        'MiniMax': 'bg-teal-100 text-teal-700 dark:bg-teal-900 dark:text-teal-200',
        'StepFun': 'bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-200',
        'Stability AI': 'bg-pink-50 text-pink-600 dark:bg-pink-950 dark:text-pink-300',
        'Kuaishou': 'bg-orange-50 text-orange-600 dark:bg-orange-950 dark:text-orange-300',
        'Pika': 'bg-violet-50 text-violet-600 dark:bg-violet-950 dark:text-violet-300',
        'Runway': 'bg-rose-50 text-rose-600 dark:bg-rose-950 dark:text-rose-300',
        'default': 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-200'
    }};

    const CAT_COLORS = {{
        'text': 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-200',
        'multimodal': 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-200',
        'video': 'bg-pink-100 text-pink-700 dark:bg-pink-900 dark:text-pink-200',
        'image': 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-200',
        'agent': 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200',
        'code': 'bg-cyan-100 text-cyan-700 dark:bg-cyan-900 dark:text-cyan-200',
    }};

    const ORGS = [...new Set(MODELS.map(m => m.org))].sort();
    const CATS = [...new Set(MODELS.map(m => m.category || 'text'))].sort();

    ORGS.forEach(org => {{
        document.getElementById('orgFilter').innerHTML += `<option value="${{org}}">${{org}}</option>`;
    }});
    CATS.forEach(cat => {{
        const labels = {{'text':'📝 文本','multimodal':'🔮 多模态','video':'🎬 视频','image':'🎨 图片','agent':'🤖 Agent','code':'💻 代码'}};
        document.getElementById('catFilter').innerHTML += `<option value="${{cat}}">${{labels[cat] || cat}}</option>`;
    }});

    document.getElementById('totalModels').textContent = MODELS.length;
    document.getElementById('totalOrgs').textContent = ORGS.length;
    const years = MODELS.map(m => parseInt(m.date.split('-')[0]));
    document.getElementById('yearRange').textContent = Math.max(...years) - Math.min(...years) + 1;

    function getColor(org) {{ return COLORS[org] || COLORS['default']; }}
    function getCatColor(cat) {{ return CAT_COLORS[cat] || CAT_COLORS['text']; }}
    function getOpenIcon(openWeights) {{
        if (openWeights === true) return '🔓';
        if (openWeights === false) return '🔒';
        return '';
    }}
    function formatParams(params) {{
        if (!params && params !== 0) return '';
        if (typeof params === 'string') return params;
        if (params >= 1000) return `${{(params/1000).toFixed(0)}}T`;
        return `${{params}}B`;
    }}

    function renderTimeline(models) {{
        const container = document.getElementById('timeline');
        document.getElementById('stats').textContent = `${{models.length}} 个模型`;

        if (models.length === 0) {{
            container.innerHTML = '<div class="text-center py-20 text-gray-400">暂无数据</div>';
            return;
        }}

        let html = '';
        let currentYear = null;

        models.forEach((m, i) => {{
            const year = m.date.split('-')[0];
            if (year !== currentYear) {{
                currentYear = year;
                html += `
                <div class="relative mb-8">
                    <div class="flex items-center justify-center">
                        <div class="bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-6 py-2 rounded-full text-lg font-bold shadow-lg">
                            ${{year}}
                        </div>
                    </div>
                </div>`;
            }}

            const isLeft = i % 2 === 0;
            const catColor = getCatColor(m.category);
            const orgColor = getColor(m.org);

            html += `
            <div class="timeline-item relative mb-6">
                <div class="dot" style="top: ${{20 + (i % 10) * 5}}px"></div>
                <div class="w-5/12 ${{isLeft ? 'pr-8 text-right' : 'pl-8 ml-auto'}}" style="${{isLeft ? '' : 'text-align:left'}}">
                    <div class="model-card bg-white dark:bg-gray-800 rounded-xl shadow-md p-4" style="max-width: 400px; ${{isLeft ? '' : 'margin-left:auto'}}">
                        <div class="flex items-start justify-between gap-2 mb-2">
                            <h3 class="font-semibold text-gray-900 dark:text-white text-sm">${{getOpenIcon(m.open_weights)}} ${{m.name}}</h3>
                            <span class="${{catColor}} text-xs px-2 py-0.5 rounded-full shrink-0">${{m.category || 'text'}}</span>
                        </div>
                        <div class="flex items-center gap-2 mb-2 flex-wrap" style="${{isLeft ? 'justify-content:flex-end' : ''}}">
                            <span class="${{orgColor}} text-xs px-2 py-0.5 rounded-full company-tag">${{m.org}}</span>
                            ${{m.params ? `<span class="bg-gray-100 dark:bg-gray-700 text-xs px-2 py-0.5 rounded-full">${{formatParams(m.params)}}</span>` : ''}}
                        </div>
                        <div class="text-xs text-gray-400">${{m.date}}</div>
                        ${{m.description ? `<p class="text-xs text-gray-500 dark:text-gray-400 mt-2">${{m.description}}</p>` : ''}}
                    </div>
                </div>
            </div>`;
        }});

        container.innerHTML = html;
    }}

    let allModels = MODELS;
    let filteredModels = allModels;

    function applyFilters() {{
        const org = document.getElementById('orgFilter').value;
        const cat = document.getElementById('catFilter').value;
        filteredModels = allModels.filter(m => {{
            if (org && m.org !== org) return false;
            if (cat && (m.category || 'text') !== cat) return false;
            return true;
        }});
        renderTimeline(filteredModels);
    }}

    document.getElementById('orgFilter').addEventListener('change', applyFilters);
    document.getElementById('catFilter').addEventListener('change', applyFilters);

    renderTimeline(allModels);
    </script>
</body>
</html>
"""

with open(out_path, 'w') as f:
    f.write(html)

print(f"✅ 生成完成: {len(html)} bytes, {len(models)} 条模型")
