# LLM 时间线探索日志

## 2025-05-12 探索过程

### 已验证可用资源

#### 1. awesome-ai-models ✅ 已Clone
- **来源**: https://github.com/sav7ng/awesome-ai-models
- **Clone 位置**: /www/wwwroot/projects/awesome-ai-models
- **数据**: 42个模型，docs/models.json
- **字段**: name, org, date, repo, tags, description（中英双语）
- **覆盖**: 2018-10 (BERT) 到 2025-12

#### 2. frontier ✅ 已Clone
- **来源**: https://github.com/LoggeL/frontier
- **Clone 位置**: /www/wwwroot/projects/frontier
- **数据**: src/data/models.json（64条）
- **字段**: id, name, provider, releaseDate, knowledgeCutoff, openWeights, contextWindow, hfLink, totalParams, activeParams, architecture, aaBenchmark数据, 价格等

### 数据整合结果

**整合后数据**: /www/wwwroot/projects/llm-timeline/data/llm_timeline.json
- **总计**: 101 条记录
- **公司覆盖**: 26 家

**按公司统计**:
- OpenAI: 15个
- Google: 11个
- Meta: 11个
- Alibaba: 11个
- Anthropic: 9个
- DeepSeek: 8个
- Zhipu AI: 4个
- xAI: 4个
- Mistral AI: 3个
- Kimi: 3个
- MiniMax: 2个
- ... 其他

**主要系列**:
- GPT: 12个 (2018-06 ~ 2026-04)
- LLaMA: 10个 (2023-02 ~ 2025-07)
- Qwen: 11个 (2024-06 ~ 2026-04)
- Gemini: 5个 (2025-05 ~ 2026-02)
- Grok: 4个 (2024-03 ~ 2026-04)
- Claude: 9个 (2025-05 ~ 2026-04)

### 补充的早期模型
- GPT-1 (2018-06-11)
- GPT-2 (2019-02-14)
- BERT-Base/Large (2018-10-11)
- T5 (2019-10-24)
- GPT-3 (2020-06-11)

### 已知数据缺口
- [ ] 豆包（字节跳动）系列
- [ ] 文心一言（百度）系列
- [ ] 讯飞星火系列
- [ ] 阶跃星辰系列
- [ ] Stability AI 更多图片模型
- [ ] 视频生成模型（Sora、Veo、Pika 等）

### 下一步
- [ ] 确认数据准确度（特别是 2025-2026 新模型日期）
- [ ] 补充缺失的公司系列
- [ ] 考虑视频制作方案（Manim 时间轴 / HTML 交互页面）
- [ ] 确认参数字段完整性

### 脚本工具
- scripts/integrate_data_v2.py - 数据整合脚本

## 2025-05-12 探索过程（第二轮）

### 数据补充结果
- **补充前**: 101 条
- **补充后**: 137 条
- **新增**: 36 条

**新增覆盖**:
- 字节跳动（豆包/Doubao）: 3条
- 百度（文心/ERNIE）: 3条
- 讯飞（星火/Spark）: 4条
- 阶跃星辰（Step）: 2条
- Moonshot（Kimi）: 2条
- 视频生成: Sora, Veo, Gen-3, Pika, Kling, 海螺 - 6条
- 图片生成补充: DALL-E 2/3, SD3, Imagen 2/3 - 5条
- 语音/多模态补充: GPT-4o, Gemini 1.0/1.5, Claude 3/3.5系列 - 11条

**按类别统计**:
- text: 117个
- multimodal: 8个
- video: 6个
- image: 5个

**按公司 Top10**:
- OpenAI: 20个
- Google: 17个
- Anthropic: 14个
- Meta: 11个
- Alibaba: 11个
- DeepSeek: 8个

### 补充的现成 GitHub 项目

1. **awesome-ai-models** (https://github.com/sav7ng/awesome-ai-models) - 42条模型数据，中英双语
2. **frontier** (https://github.com/LoggeL/frontier) - 64条，含参数量/价格/Benchmark

## 2026-05-29 更新

### 数据增长
- **更新前**: 664 条记录
- **更新后**: 675 条记录
- **新增**: 11 条

### 新增模型列表

#### 2026年4月
1. GPT-6 (2026-04-14) - OpenAI，代号Spud，200万Token上下文
2. Qwen 3.6-35B-A3B (2026-04-16) - 阿里开源，Apache 2.0
3. Qwen 3.6 Max (2026-04-16) - 阿里旗舰

#### 2026年5月
4. Gemini 3.5 Flash (2026-05) - Google，极速高并发
5. Qwen 3.7 (2026-05) - 阿里最新版
6. 文心 ERNIE 5.1 (2026-05) - 百度，搜索增强
7. 星火 V4 (2026-05) - 讯飞，语音+教育
8. 混元 3 Preview (2026-05) - 腾讯，社交场景
9. 豆包 Seed 2.0 Pro (2026-05) - 字节跳动
10. GPT-5.6 曝光 (2026-05-26) - 150万Token上下文
11. Claude Opus 4.8 (2026-05-29) - Anthropic，今天发布

### 验证结果
✅ 使用 mmx search 联网功能验证
✅ 确认 GPT-5.5、DeepSeek V4、Claude Opus 4.7 发布日期准确
✅ 发现并添加 Claude Opus 4.8（今日最新发布）

### 当前数据统计
- **总模型数**: 675 条
- **覆盖时间**: 2018-2026
- **主要公司分布**:
  - 阿里: 94
  - OpenAI: 67
  - Google: 55
  - Anthropic: 30
  - Mistral: 28
  - DeepSeek: 27
  - Meta: 22
