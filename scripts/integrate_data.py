#!/usr/bin/env python3
"""
LLM 时间线数据整合脚本
- 整合 awesome-ai-models (42条) 和 frontier (64条)
- 补充缺失的早期模型
- 输出统一的 JSON 格式
"""

import json
from pathlib import Path

# 读取两个数据源
awesome_path = Path("/www/wwwroot/projects/awesome-ai-models/docs/models.json")
frontier_path = Path("/www/wwwroot/projects/frontier/src/data/models.json")

with open(awesome_path, "r", encoding="utf-8") as f:
    awesome_data = json.load(f)

with open(frontier_path, "r", encoding="utf-8") as f:
    frontier_data = json.load(f)

print(f"awesome-ai-models: {len(awesome_data)} 条")
print(f"frontier: {len(frontier_data)} 条")

# 整理 frontier 数据为 dict，方便匹配
frontier_by_name = {}
for item in frontier_data:
    name_lower = item.get("name", "").lower()
    frontier_by_name[name_lower] = item

# 已有公司列表
companies_in_awesome = set(m.get("org", "") for m in awesome_data)
print(f"\nawesome 中已有公司: {companies_in_awesome}")

# 检查 awesome 中是否有 OpenAI GPT-1, GPT-2 等早期模型
has_gpt1 = any("gpt-1" in m.get("name", "").lower() or m.get("name", "") == "GPT" for m in awesome_data)
has_gpt2 = any("gpt-2" in m.get("name", "").lower() for m in awesome_data)
has_bert = any("bert" in m.get("name", "").lower() for m in awesome_data)
print(f"GPT-1: {'有' if has_gpt1 else '缺'}")
print(f"GPT-2: {'有' if has_gpt2 else '缺'}")
print(f"BERT:  {'有' if has_bert else '缺'}")

# frontier 中的 provider 列表
providers_frontier = set(m.get("provider", "") for m in frontier_data)
print(f"\nfrontier 中的 providers: {providers_frontier}")
