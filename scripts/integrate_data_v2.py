#!/usr/bin/env python3
"""
LLM 时间线数据整合脚本 V2
整合 awesome-ai-models 和 frontier，补充早期模型
"""

import json
from pathlib import Path
from datetime import datetime

# ============ 读取数据 ============
awesome_path = Path("/www/wwwroot/projects/awesome-ai-models/docs/models.json")
frontier_path = Path("/www/wwwroot/projects/frontier/src/data/models.json")

with open(awesome_path, "r", encoding="utf-8") as f:
    awesome_data = json.load(f)

with open(frontier_path, "r", encoding="utf-8") as f:
    frontier_data = json.load(f)

print(f"[数据源] awesome-ai-models: {len(awesome_data)} 条")
print(f"[数据源] frontier: {len(frontier_data)} 条")

# ============ frontier 转统一格式 ============
def parse_frontier_item(item):
    """把 frontier 格式转为统一格式"""
    name = item.get("name", "")
    # 去掉日期后缀如 " (Jul '24)"
    clean_name = name
    import re
    m = re.match(r"^(.+?)\s*\(", name)
    if m:
        clean_name = m.group(1).strip()
    
    return {
        "name": clean_name,
        "original_name": item.get("name", ""),
        "org": item.get("provider", ""),
        "date": item.get("releaseDate", ""),
        "open_weights": item.get("openWeights", None),
        "params": item.get("totalParams", None),
        "active_params": item.get("activeParams", None),
        "context_window": item.get("contextWindow", None),
        "hf_link": item.get("hfLink", ""),
        "architecture": item.get("architecture", ""),
        "knowledge_cutoff": item.get("knowledgeCutoff", ""),
        "tags": [],
        "description": {"en": clean_name},
        "source": "frontier",
    }

frontier_normalized = [parse_frontier_item(i) for i in frontier_data]

# ============ awesome 转统一格式 ============
def parse_awesome_item(item):
    tags = item.get("tags", [])
    # 判断模型类别
    tag_map = {
        "LLM": "text",
        "Code": "code",
        "Agent": "agent",
        "Reasoning": "reasoning",
        "Multimodal": "multimodal",
        "MoE": "moe",
    }
    category = "text"
    for t in tags:
        if t in tag_map:
            category = tag_map[t]
            break
    
    return {
        "name": item.get("name", ""),
        "org": item.get("org", ""),
        "date": item.get("date", ""),
        "open_weights": None,  # awesome 数据没有这个字段
        "params": None,
        "active_params": None,
        "context_window": None,
        "hf_link": item.get("repo", ""),
        "architecture": "",
        "knowledge_cutoff": "",
        "tags": tags,
        "category": category,
        "description": item.get("description", {}),
        "source": "awesome",
    }

awesome_normalized = [parse_awesome_item(i) for i in awesome_data]

# ============ 补充早期模型（手动整理） ============
early_models = [
    {
        "name": "GPT-1",
        "org": "OpenAI",
        "date": "2018-06-11",
        "open_weights": False,
        "params": 110,  # 1.17亿参数
        "active_params": 110,
        "context_window": None,
        "hf_link": "",
        "architecture": "decoder-only",
        "knowledge_cutoff": "2018-06",
        "tags": ["LLM", "text"],
        "category": "text",
        "description": {"en": "OpenAI's first Generative Pre-trained Transformer, 110M parameters."},
        "source": "manual",
    },
    {
        "name": "GPT-2",
        "org": "OpenAI",
        "date": "2019-02-14",
        "open_weights": False,
        "params": 1500,  # 15亿参数
        "active_params": 1500,
        "context_window": 1024,
        "hf_link": "https://github.com/openai/gpt-2",
        "architecture": "decoder-only",
        "knowledge_cutoff": "2019-02",
        "tags": ["LLM", "text"],
        "category": "text",
        "description": {"en": "GPT-2, 1.5B parameters, famously withheld due to misuse concerns."},
        "source": "manual",
    },
    {
        "name": "BERT-Base",
        "org": "Google",
        "date": "2018-10-11",
        "open_weights": True,
        "params": 110,
        "active_params": 110,
        "context_window": 512,
        "hf_link": "https://github.com/google-research/bert",
        "architecture": "encoder-only",
        "knowledge_cutoff": "2018-10",
        "tags": ["LLM", "text"],
        "category": "text",
        "description": {"en": "BERT Base, 110M parameters, encoder-only architecture."},
        "source": "manual",
    },
    {
        "name": "BERT-Large",
        "org": "Google",
        "date": "2018-10-11",
        "open_weights": True,
        "params": 340,
        "active_params": 340,
        "context_window": 512,
        "hf_link": "https://github.com/google-research/bert",
        "architecture": "encoder-only",
        "knowledge_cutoff": "2018-10",
        "tags": ["LLM", "text"],
        "category": "text",
        "description": {"en": "BERT Large, 340M parameters, encoder-only architecture."},
        "source": "manual",
    },
    {
        "name": "T5",
        "org": "Google",
        "date": "2019-10-24",
        "open_weights": True,
        "params": 220,  # T5-Base
        "active_params": 220,
        "context_window": 512,
        "hf_link": "https://github.com/google-research/text-to-text-transfer-transformer",
        "architecture": "encoder-decoder",
        "knowledge_cutoff": "2019-10",
        "tags": ["LLM", "text"],
        "category": "text",
        "description": {"en": "T5 (Text-to-Text Transfer Transformer), encoder-decoder architecture."},
        "source": "manual",
    },
    {
        "name": "GPT-3",
        "org": "OpenAI",
        "date": "2020-06-11",
        "open_weights": False,
        "params": 175000,  # 1750亿
        "active_params": 175000,
        "context_window": 2048,
        "hf_link": "",
        "architecture": "decoder-only",
        "knowledge_cutoff": "2019-10",
        "tags": ["LLM", "text"],
        "category": "text",
        "description": {"en": "GPT-3, 175B parameters, few-shot learner."},
        "source": "manual",
    },
]

# ============ 合并所有数据 ============
all_models = early_models + awesome_normalized + frontier_normalized

# 去重（按 name + date 组合）
seen = set()
unique_models = []
for m in all_models:
    key = (m["name"].lower(), m.get("date", ""))
    if key not in seen:
        seen.add(key)
        unique_models.append(m)

# 按日期排序
unique_models.sort(key=lambda x: x.get("date", ""))

print(f"\n[合并后] 共 {len(unique_models)} 条")

# ============ 按公司统计 ============
from collections import Counter
org_count = Counter(m["org"] for m in unique_models)
print("\n[按公司统计]")
for org, cnt in org_count.most_common():
    print(f"  {org}: {cnt}个")

# ============ 输出 ============
output_path = Path("/www/wwwroot/projects/llm-timeline/data/llm_timeline.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(unique_models, f, ensure_ascii=False, indent=2)

print(f"\n✅ 已保存到: {output_path}")
print(f"   总计: {len(unique_models)} 条模型记录")
