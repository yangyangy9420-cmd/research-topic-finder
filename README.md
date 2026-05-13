# Skill流程

以后你可以这样调用它：

* 帮我寻找研究课题。
* 大概方向：低成本 RGB 图像用于果蔬新鲜度检测。
* 仪器设备：手机、RGB 相机、光照箱、普通 GPU 工作站。
* 导师侧重点：轻量化模型、端侧部署、采后品质评价。
* 请生成 HTML 文献筛选统计分析报告。

## Skill 会按这个流程做：

1. 先把你的输入整理成“研究边界”；
2. 检索近三年高质量论文；
3. 筛选核心文献、重要参考、外围/剔除文献；
4. 按 Why / What / How / Ideas 分析论文；
5. 统计年份、对象、任务、设备、方法；
6. 找研究空白；
7. 给出 3 到 8 个候选研究方向；
8. 对每个方向打分；
9. 给出创新点建议；
10. 生成 HTML 报告。
    
## Skill 包里包含：

`SKILL.md`
- [ ] 主 Skill 文件，定义什么时候调用、怎么做选题分析、怎么生成结果。 :tada:

`references/methodology.md`
- [ ] 把你 PDF 里的“借鉴论文思维、选课题、读文献、找创新点”改造成可执行的方法论。 :tada:

`references/search-protocol.md`
- [ ] 定义怎么检索近三年论文、怎么扩展关键词、怎么筛选高质量文献。 :tada:

`references/scoring-rubric.md`
- [ ] 定义候选研究方向的评分标准。 :tada:

`references/html-report-spec.md`
- [ ] 定义 HTML 报告结构和 JSON 输入格式。 :tada:

`scripts/generate_research_topic_report.py`
- [ ] HTML 报告生成脚本，用来生成类似你示例文件那种统计分析页面。 :tada:
