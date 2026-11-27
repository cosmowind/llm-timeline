#!/usr/bin/env python3
"""生成 LLM Intelligence Index 动态时间轴 HTML 动画"""
import json, csv
from pathlib import Path
from collections import defaultdict

# ====== 读取 AA API 数据 ======
aa_api = json.load(open('/www/wwwroot/projects/frontier/src/data/aa-models-api.json'))

# 过滤有完整数据的
have = [m for m in aa_api
        if m.get('aaIntelligenceIndex')
        and m.get('price1mBlended3to1')
        and m.get('releaseDate')
        and m['releaseDate'].startswith('20')]

# 去重：每个模型名取最新日期
seen = {}
for m in sorted(have, key=lambda x: x['releaseDate'], reverse=True):
    if m['name'] not in seen:
        seen[m['name']] = m
have = list(seen.values())
print(f"去重后: {len(have)} 条")

# ====== 公司颜色 ======
COLORS = {
    'OpenAI': '#ef4444', 'Google': '#3b82f6', 'Anthropic': '#f97316',
    'DeepSeek': '#06b6d4', 'Meta': '#8b5cf6', 'xAI': '#a855f7',
    'Mistral': '#6366f1', 'Alibaba': '#f59e0b', 'ByteDance': '#ec4899',
    'ByteDance Seed': '#ec4899', 'MiniMax': '#14b8a6', 'Kimi': '#f43f5e',
    'Z AI': '#64748b', 'Amazon': '#f97316', 'Microsoft': '#0078d4',
    'NVIDIA': '#22c55e', 'default': '#94a3b8',
}

# ====== 按月份分组 ======
monthly = defaultdict(list)
for m in have:
    key = m['releaseDate'][:7]  # 'YYYY-MM'
    monthly[key].append(m)

all_months = sorted(monthly.keys())
print(f"时间跨度: {all_months[0]} ~ {all_months[-1]} ({len(all_months)}个月)")

# ====== 构建 JS 模型列表 ======
js_models = []
for m in have:
    idx = m['aaIntelligenceIndex']
    cost = m['price1mBlended3to1']
    value = round(idx / cost, 2) if cost else 0
    color = COLORS.get(m['provider'], COLORS['default'])
    js_models.append({
        'name': m['name'],
        'provider': m['provider'],
        'date': m['releaseDate'],
        'month': m['releaseDate'][:7],
        'index': idx,
        'cost': cost,
        'value': value,
        'color': color,
    })

js_models.sort(key=lambda x: x['index'], reverse=True)

# ====== 构建 HTML ======
# 序列化 JS 数据（用 % formatting 而非 f-string）
models_json = json.dumps(js_models, ensure_ascii=False)
monthly_json = json.dumps({k: [mm['name'] for mm in v] for k, v in monthly.items()}, ensure_ascii=False)
all_months_json = json.dumps(all_months)
index_max = max(m['index'] for m in js_models) + 2

MAINSTREAM = {'OpenAI','Anthropic','Google','Meta','Microsoft','DeepSeek','xAI','Amazon','Alibaba','Baidu','Tencent','ByteDance','Cohere','Mistral','NVIDIA','Samsung','Apple','Kimi','MiniMax','01.AI'}
providers = sorted(set(m['provider'] for m in js_models))
mainstream = [p for p in providers if p in MAINSTREAM]
niche = [p for p in providers if p not in MAINSTREAM]

def make_legend_item(p, models):
    for m in models:
        if m['provider'] == p:
            c = m['color']; break
    else: c = '#94a3b8'
    return ('<span class="legend-item flex items-center gap-1 text-xs cursor-pointer px-2 py-1 rounded-full border border-transparent hover:border-gray-500 transition" '
        'style="color:%s;" data-provider="%s" onclick="toggleProvider(\'%s\')" title="点击切换显示">'
        '<span style="width:10px;height:10px;border-radius:50%%;background:%s;display:inline-block;"></span>'
        '<span class="provider-label">%s</span></span>') % (c, p, p, c, p)

legend_html = ''
if mainstream:
    legend_html += '<div class="mb-2"><span class="text-xs text-gray-500 mr-2">⭐主流</span>'
    legend_html += '<button onclick="toggleGroup(\'mainstream\')" class="text-xs px-1.5 py-0.5 bg-gray-700 hover:bg-gray-600 rounded-full mr-1">显/隐</button>'
    for p in mainstream:
        legend_html += make_legend_item(p, js_models)
    legend_html += '</div>'
if niche:
    legend_html += '<div><span class="text-xs text-gray-500 mr-2">🌐其他</span>'
    legend_html += '<button onclick="toggleGroup(\'niche\')" class="text-xs px-1.5 py-0.5 bg-gray-700 hover:bg-gray-600 rounded-full mr-1">显/隐</button>'
    for p in niche:
        legend_html += make_legend_item(p, js_models)
    legend_html += '</div>'

# 颜色映射表供 JS 用
color_map_js = json.dumps(COLORS, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 LLM Intelligence Race - 大模型指数进化史</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
        .bubble {
            position: absolute;
            border-radius: 50%%;
            display: flex; align-items: center; justify-content: center;
            font-size: 9px; color: white; font-weight: 600;
            cursor: pointer; transition: all 0.4s ease;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5);
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            overflow: hidden; white-space: nowrap;
        }
        .bubble:hover { z-index: 100; transform: scale(1.2); box-shadow: 0 6px 24px rgba(0,0,0,0.5); }
        .bubble.hidden { display: none; }
        .legend-item.dimmed { opacity: 0.3; }
        .legend-item.dimmed .provider-label { text-decoration: line-through; }
    </style>
</head>
<body class="bg-gray-900 text-white min-h-screen">

    <!-- Header -->
    <div class="bg-gray-800 border-b border-gray-700 px-4 py-3">
        <div class="max-w-6xl mx-auto flex items-center justify-between flex-wrap gap-3">
            <div>
                <h1 class="text-xl font-bold">🏆 LLM Intelligence Race</h1>
                <p class="text-xs text-gray-400">大模型 Intelligence Index 进化史 · 数据来源: Artificial Analysis</p>
            </div>
            <div class="flex items-center gap-4 text-sm">
                <span>📅 <span id="curDate" class="font-mono">--</span></span>
                <span>🤖 <span id="curCount">0</span> 个模型</span>
                <span>📊 最高: <span id="curTop" class="text-yellow-400 font-bold">--</span></span>
            </div>
        </div>
    </div>

    <!-- Controls -->
    <div class="bg-gray-800/90 border-b border-gray-700 px-4 py-2 sticky top-0 z-50" style="backdrop-filter:blur(10px)">
        <div class="max-w-6xl mx-auto flex items-center gap-3 flex-wrap">
            <button id="playBtn" class="px-4 py-1 bg-indigo-600 hover:bg-indigo-500 rounded-full text-sm font-bold transition">▶ 播放</button>
            <button id="resetBtn" class="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded-full text-sm">⏮ 重置</button>
            <input type="range" id="slider" min="0" max="%d" value="0" class="flex-1 min-w-[200px]" style="accent-color:#6366f1;">
            <select id="speedSel" class="bg-gray-700 text-sm px-2 py-1 rounded">
                <option value="1000">0.5x</option>
                <option value="500">1x</option>
                <option value="250" selected>2x</option>
                <option value="125">4x</option>
            </select>
            <span class="text-xs text-gray-500">播放速度</span>
        </div>
    </div>

    <!-- Chart -->
    <div class="max-w-6xl mx-auto px-4 py-6">
        <div class="relative bg-gray-800/50 rounded-xl" style="height:480px;">
            <!-- Y-axis -->
            <div id="yAxis" class="absolute left-0 top-0 h-full flex flex-col justify-between py-4 text-xs text-gray-500" style="width:36px;"></div>
            <!-- Bubbles -->
            <div id="bubbles" class="absolute inset-0" style="left:40px;right:20px;top:0;bottom:24px;"></div>
            <!-- X-axis -->
            <div id="xAxis" class="absolute left-40 right-4 bottom-0 h-6 flex justify-between text-xs text-gray-500"></div>
        </div>
    </div>

    <!-- Legend -->
    <div class="max-w-6xl mx-auto px-4 pb-3">
        <div class="flex flex-wrap gap-3 justify-center" id="legend">%s</div>
    </div>

    <!-- Stats -->
    <div class="bg-gray-800/60 px-4 py-3">
        <div class="max-w-6xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-4 text-center text-sm">
            <div><span class="text-gray-400">已入场</span><br><span id="s1" class="text-xl font-bold text-indigo-400">0</span></div>
            <div><span class="text-gray-400">Intelligence总和</span><br><span id="s2" class="text-xl font-bold text-green-400">0</span></div>
            <div><span class="text-gray-400">平均Index</span><br><span id="s3" class="text-xl font-bold text-yellow-400">0</span></div>
            <div><span class="text-gray-400">性价比之王</span><br><span id="s4" class="text-xl font-bold text-pink-400">--</span></div>
        </div>
    </div>

<script>
var ALL_MODELS = %s;
var MONTHLY = %s;
var ALL_MONTHS = %s;
var INDEX_MAX = %d;
var MAINSTREAM_PROVIDERS = new Set(%s);
var NICHE_PROVIDERS = new Set(%s);

var CHART_W = 0, CHART_H = 480;
var PADDING = {top:20, bottom:20, left:0, right:20};
var curMonthIdx = 0;
var playing = false, playTimer = null;
var hiddenProviders = new Set();

function toggleProvider(p) {
    if (hiddenProviders.has(p)) {
        hiddenProviders.delete(p);
    } else {
        hiddenProviders.add(p);
    }
    updateLegend();
    render(curMonthIdx);
}

function toggleGroup(group) {
    var providers = group === 'mainstream' ? MAINSTREAM_PROVIDERS : NICHE_PROVIDERS;
    var allHidden = [...providers].every(p => hiddenProviders.has(p));
    if (allHidden) {
        providers.forEach(p => hiddenProviders.delete(p));
    } else {
        providers.forEach(p => hiddenProviders.add(p));
    }
    updateLegend();
    render(curMonthIdx);
}

function updateLegend() {
    document.querySelectorAll('.legend-item').forEach(el => {
        var p = el.dataset.provider;
        if (hiddenProviders.has(p)) {
            el.classList.add('dimmed');
        } else {
            el.classList.remove('dimmed');
        }
    });
}

function idxToY(idx) {
    var pct = idx / INDEX_MAX;
    return CHART_H - PADDING.bottom - pct * (CHART_H - PADDING.top - PADDING.bottom);
}
function idxToR(idx) {
    var minR = 5, maxR = 38;
    return minR + (idx / 60) * (maxR - minR);
}
function getMonthIndex(monthStr) {
    return ALL_MONTHS.indexOf(monthStr);
}

function buildYAxis() {
    var el = document.getElementById('yAxis');
    var html = '';
    for (var i = 0; i <= 6; i++) {
        var idx = Math.round(INDEX_MAX * i / 6);
        var y = idxToY(idx);
        html += '<div style="position:absolute;top:'+y+'px;left:0;">'+idx+'</div>';
    }
    el.innerHTML = html;
}
function buildXAxis() {
    var el = document.getElementById('xAxis');
    var html = '';
    var step = Math.ceil(ALL_MONTHS.length / 12);
    for (var i = 0; i < ALL_MONTHS.length; i += step) {
        var pct = i / (ALL_MONTHS.length - 1) * 100;
        html += '<span style="position:absolute;left:'+pct+'%%;transform:translateX(-50%%);">'+ALL_MONTHS[i]+'</span>';
    }
    el.innerHTML = html;
}

function render(monthIdx) {
    var visible = ALL_MODELS.filter(function(m) {
        return getMonthIndex(m.month) <= monthIdx && !hiddenProviders.has(m.provider);
    });
    visible.sort(function(a,b){ return b.index - a.index; });

    var count = visible.length;
    var totalIdx = visible.reduce(function(s,m){ return s+m.index; }, 0);
    var avgIdx = count ? (totalIdx/count).toFixed(1) : 0;
    var bestVal = count ? Math.max.apply(null, visible.map(function(m){ return m.value; })) : 0;
    var best = visible.find(function(m){ return m.value === bestVal; });
    var top1 = visible[0];

    document.getElementById('curCount').textContent = count;
    document.getElementById('curDate').textContent = ALL_MONTHS[monthIdx] || '';
    document.getElementById('curTop').textContent = top1 ? top1.name.slice(0,22)+' ('+top1.index+')' : '--';
    document.getElementById('s1').textContent = count;
    document.getElementById('s2').textContent = Math.round(totalIdx);
    document.getElementById('s3').textContent = avgIdx;
    document.getElementById('s4').textContent = best ? best.name.slice(0,18)+' ('+best.value+')' : '--';

    var container = document.getElementById('bubbles');
    CHART_W = container.offsetWidth || 900;
    visible.sort(function(a,b){ return a.index - b.index; });  // 升序：小在下，大在上

    var seenNames = {};
    var html = '';
    visible.forEach(function(m, i) {
        if (seenNames[m.name]) return;
        seenNames[m.name] = true;

        var xPct = getMonthIndex(m.month) / (ALL_MONTHS.length - 1);
        var x = xPct * CHART_W;
        var y = idxToY(m.index);
        var r = Math.min(idxToR(m.index), 36);
        var isTop = i >= visible.length - 3;  // 最后3个（最大的）显示名称
        var name = isTop ? m.name : '';
        var border = isTop ? 'border:2px solid white;' : '';
        var zIndex = i;  // 升序下标 → 大气泡z-index更高

        html += '<div class="bubble" style="'
            + 'left:'+x+'px;'
            + 'top:'+y+'px;'
            + 'width:'+(r*2)+'px;height:'+(r*2)+'px;'
            + 'background:'+m.color+';'
            + 'z-index:'+zIndex+';'
            + border
            + '" title="'+m.name+'&#10;Index:'+m.index+'&#10;Cost:$'+m.cost+'/1M&#10;Value:'+m.value+'">'
            + name
            + '</div>';
    });
    container.innerHTML = html;
}

function step() {
    if (!playing) return;
    if (curMonthIdx >= ALL_MONTHS.length - 1) {
        playing = false;
        document.getElementById('playBtn').textContent = '▶ 播放';
        return;
    }
    curMonthIdx++;
    document.getElementById('slider').value = curMonthIdx;
    render(curMonthIdx);
    playTimer = setTimeout(step, parseInt(document.getElementById('speedSel').value));
}

document.getElementById('playBtn').addEventListener('click', function() {
    if (playing) {
        playing = false;
        clearTimeout(playTimer);
        this.textContent = '▶ 播放';
    } else {
        if (curMonthIdx >= ALL_MONTHS.length - 1) curMonthIdx = 0;
        playing = true;
        this.textContent = '⏸ 暂停';
        render(curMonthIdx);
        step();
    }
});
document.getElementById('resetBtn').addEventListener('click', function() {
    playing = false; clearTimeout(playTimer);
    document.getElementById('playBtn').textContent = '▶ 播放';
    curMonthIdx = 0;
    document.getElementById('slider').value = 0;
    render(0);
});
document.getElementById('slider').addEventListener('input', function() {
    curMonthIdx = parseInt(this.value);
    render(curMonthIdx);
});

buildYAxis();
buildXAxis();
render(0);
window.addEventListener('resize', function(){ render(curMonthIdx); });
</script>
</body>
</html>
""" % (len(all_months)-1, legend_html, models_json, monthly_json, all_months_json, index_max,
        json.dumps(list(MAINSTREAM)), json.dumps(list(niche)))

out_path = Path("/www/wwwroot/projects/llm-timeline/show/animation.html")
with open(out_path, 'w') as f:
    f.write(html)

print(f"✅ 动画页面: {len(html)} bytes")
print(f"发布: cp {out_path} /www/wwwroot/show/projects/llm-timeline/animation.html")
