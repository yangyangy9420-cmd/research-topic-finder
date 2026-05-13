#!/usr/bin/env python3
"""Generate a Chinese HTML literature-screening report for research topic discovery.

Usage:
    python generate_research_topic_report.py input.json output.html

The script expects a JSON object described in references/html-report-spec.md.
It performs simple statistics over paper records and renders a polished HTML report.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def h(value: Any) -> str:
    """HTML-escape a value and normalize empty fields."""
    if value is None:
        return ""
    text = str(value).strip()
    return html.escape(text) if text else ""


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def split_tags(value: Any) -> List[str]:
    """Split comma/semicolon/slash separated labels while keeping short phrases."""
    if value is None:
        return []
    if isinstance(value, list):
        raw = []
        for item in value:
            raw.extend(split_tags(item))
        return raw
    text = str(value).strip()
    if not text:
        return []
    for sep in ["；", ";", "、", ",", "，", "|"]:
        text = text.replace(sep, "/")
    parts = [p.strip() for p in text.split("/") if p.strip()]
    return parts if parts else [text]


def count_field(records: Iterable[Dict[str, Any]], field: str, split: bool = True) -> Counter:
    counter: Counter = Counter()
    for record in records:
        value = record.get(field)
        if split:
            for tag in split_tags(value):
                counter[tag] += 1
        elif value not in (None, ""):
            counter[str(value).strip()] += 1
    return counter


def bar(width_pct: float) -> str:
    width = max(2, min(100, int(round(width_pct)))) if width_pct else 0
    return f"<div class='bar'><span style='width:{width}%'></span></div>"


def counter_table(counter: Counter, limit: int = 30) -> str:
    if not counter:
        return "<p class='muted'>暂无可统计记录。</p>"
    max_count = max(counter.values()) or 1
    rows = []
    for label, count in counter.most_common(limit):
        rows.append(
            "<tr>"
            f"<td>{h(label)}</td>"
            f"<td>{count}</td>"
            f"<td>{bar(count / max_count * 100)}</td>"
            "</tr>"
        )
    return (
        "<table class='compact'><thead><tr><th>类别</th><th>数量</th><th>相对强度</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def category_class(category: str) -> str:
    c = (category or "").lower()
    if "core" in c or "核心" in c:
        return "ok"
    if "important" in c or "重要" in c:
        return "mid"
    return "low"


def score_label(score: Any) -> Tuple[str, str]:
    try:
        n = float(score)
    except Exception:
        return "未评分", "low"
    if n >= 85:
        return "强烈推荐", "ok"
    if n >= 75:
        return "推荐", "mid"
    if n >= 60:
        return "备选", "mid"
    return "谨慎", "low"


def render_records(records: List[Dict[str, Any]]) -> str:
    if not records:
        return "<p class='muted'>暂无论文记录。请先完成检索与筛选。</p>"
    rows = []
    for idx, r in enumerate(records, 1):
        title = h(r.get("title", "未命名文献"))
        meta_parts = [h(r.get("authors")), h(r.get("venue")), h(r.get("doi"))]
        meta = "；".join([p for p in meta_parts if p])
        url = h(r.get("url"))
        link = f"<div class='meta'>{meta}</div>" if meta else ""
        if url:
            link += f"<div class='meta'>source: {url}</div>"
        cat = h(r.get("category", "未分类"))
        rows.append(
            "<tr>"
            f"<td><strong>{idx}. {title}</strong>{link}</td>"
            f"<td>{h(r.get('year'))}</td>"
            f"<td>{h(r.get('object'))}</td>"
            f"<td>{h(r.get('task'))}</td>"
            f"<td>{h(r.get('input_device'))}</td>"
            f"<td>{h(r.get('method'))}</td>"
            f"<td>{h(r.get('key_contribution'))}</td>"
            f"<td>{h(r.get('limitation'))}</td>"
            f"<td><span class='pill {category_class(cat)}'>{cat}</span></td>"
            "</tr>"
        )
    return (
        "<table class='records'><thead><tr>"
        "<th>序号/题名</th><th>年份</th><th>对象/问题</th><th>任务/输出</th>"
        "<th>输入/设备</th><th>方法</th><th>关键贡献</th><th>局限/缺口</th><th>分类</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
    )


def render_topics(topics: List[Dict[str, Any]]) -> str:
    if not topics:
        return "<p class='muted'>暂无候选研究方向。请先完成证据综合。</p>"
    rows = []
    for t in sorted(topics, key=lambda x: float(x.get("score", 0) or 0), reverse=True):
        label, cls = score_label(t.get("score"))
        custom_label = h(t.get("label")) or label
        rows.append(
            "<tr>"
            f"<td><strong>{h(t.get('name'))}</strong><div class='meta'>{h(t.get('academic_story'))}</div></td>"
            f"<td><span class='score'>{h(t.get('score'))}</span>/100<br><span class='pill {cls}'>{custom_label}</span></td>"
            f"<td>{h(t.get('supporting_evidence'))}</td>"
            f"<td>{h(t.get('innovation_point'))}</td>"
            f"<td>{h(t.get('minimum_plan'))}</td>"
            f"<td>{h(t.get('risk'))}<br><span class='meta'>缓解：{h(t.get('mitigation'))}</span></td>"
            "</tr>"
        )
    return (
        "<table><thead><tr><th>候选方向</th><th>评分</th><th>证据基础</th><th>创新点</th>"
        "<th>最低实施方案</th><th>风险与缓解</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table>"
    )


def render_list(items: List[Any], class_name: str = "note") -> str:
    if not items:
        return "<p class='muted'>暂无。</p>"
    lis = "".join(f"<li>{h(item)}</li>" for item in items)
    return f"<div class='{class_name}'><ol>{lis}</ol></div>"


def css() -> str:
    return """
:root{--bg:#f5f7fb;--paper:#fff;--ink:#172033;--muted:#5c667a;--line:#d9e0ea;--accent:#1967d2;--accent2:#0f8b6b;--warn:#b45309;--bad:#8b1e3f;--soft:#edf4ff;--green:#e9f8f2;--yellow:#fff7e6;--red:#fff1f3}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Microsoft YaHei","PingFang SC",Arial,sans-serif;line-height:1.72}header{background:#10233f;color:#fff;padding:42px 44px 34px}header h1{margin:0 0 10px;font-size:30px;line-height:1.28}header p{max-width:1160px;margin:8px 0;color:#d7e4f7}.wrap{max-width:1280px;margin:0 auto;padding:28px 24px 56px}section{background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:24px 26px;margin:18px 0;box-shadow:0 1px 2px rgba(15,23,42,.04);overflow-x:auto}h2{font-size:23px;margin:0 0 14px;color:#10233f}h3{font-size:18px;margin:22px 0 10px;color:#172033}p{margin:10px 0}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.card{border:1px solid var(--line);border-radius:8px;padding:16px;background:#fbfdff}.num{font-size:30px;font-weight:700;color:var(--accent);line-height:1.1}.label{font-size:13px;color:var(--muted)}table{border-collapse:collapse;width:100%;margin:12px 0 4px;background:#fff}th,td{border:1px solid var(--line);padding:9px 10px;vertical-align:top}th{background:#eef4fb;text-align:left;color:#172033}.compact td,.compact th{font-size:14px}.records{font-size:12.5px;min-width:1320px}.bar{height:12px;background:#edf2f7;border-radius:999px;overflow:hidden}.bar span{display:block;height:100%;background:linear-gradient(90deg,#1967d2,#0f8b6b)}.pill{display:inline-block;border-radius:999px;padding:3px 8px;font-size:12px;font-weight:600}.pill.ok{background:var(--green);color:#08704f}.pill.mid{background:var(--yellow);color:#915a00}.pill.low{background:var(--red);color:#8b1e3f}.note{background:#f6f9ff;border-left:4px solid var(--accent);padding:12px 14px;border-radius:6px}.warn{background:#fff8ed;border-left:4px solid var(--warn);padding:12px 14px;border-radius:6px}.okbox{background:#f0fbf7;border-left:4px solid var(--accent2);padding:12px 14px;border-radius:6px}.meta,.muted{font-size:12px;color:var(--muted);margin-top:5px}.score{font-weight:700;color:#0f8b6b}ol,ul{padding-left:22px}code{background:#f1f5f9;padding:2px 5px;border-radius:4px}@media(max-width:900px){header{padding:30px 22px}.wrap{padding:18px 12px}.grid{grid-template-columns:1fr 1fr}section{padding:18px 14px}}
""".strip()


def generate(data: Dict[str, Any]) -> str:
    records = as_list(data.get("records"))
    records = [r for r in records if isinstance(r, dict)]
    topics = [t for t in as_list(data.get("candidate_topics")) if isinstance(t, dict)]
    brief = data.get("research_brief") or {}
    if not isinstance(brief, dict):
        brief = {}

    title = h(data.get("title") or "寻找研究课题：文献筛选统计分析报告")
    subtitle = h(data.get("subtitle") or "基于近期高质量文献、实验条件与导师侧重点生成的选题建议")
    generated_date = h(data.get("generated_date") or _dt.date.today().isoformat())

    core_count = sum(1 for r in records if category_class(str(r.get("category", ""))) == "ok")
    recent_years = [int(r.get("year")) for r in records if str(r.get("year", "")).isdigit()]
    latest_count = sum(1 for y in recent_years if y >= _dt.date.today().year - 2)
    best_topic = max(topics, key=lambda x: float(x.get("score", 0) or 0), default={})
    best_topic_name = h(best_topic.get("name") or "待定")

    year_counter = count_field(records, "year", split=False)
    object_counter = count_field(records, "object", split=True)
    task_counter = count_field(records, "task", split=True)
    equipment_counter = count_field(records, "input_device", split=True)
    method_counter = count_field(records, "method", split=True)
    category_counter = count_field(records, "category", split=False)

    brief_rows = "".join(
        f"<tr><th>{h(k)}</th><td>{h(v)}</td></tr>"
        for k, v in {
            "大概研究方向": brief.get("broad_direction", ""),
            "仪器设备/数据资源": brief.get("equipment", ""),
            "导师指导侧重点": brief.get("advisor_focus", ""),
            "约束条件": brief.get("constraints", ""),
        }.items()
    )

    html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css()}</style>
</head>
<body>
<header>
<h1>{title}</h1>
<p>{subtitle}</p>
<p>生成日期：{generated_date}</p>
</header>
<main class="wrap">
<section>
<h2>一、结论先行</h2>
<div class="grid">
<div class="card"><div class="num">{len(records)}</div><div class="label">纳入文献记录</div></div>
<div class="card"><div class="num">{core_count}</div><div class="label">核心保留记录</div></div>
<div class="card"><div class="num">{latest_count}</div><div class="label">近三年强相关记录</div></div>
<div class="card"><div class="num">{len(topics)}</div><div class="label">候选研究方向</div></div>
</div>
<p class="note">综合当前证据、设备条件和导师侧重点，优先建议推进：<strong>{best_topic_name}</strong>。该建议来自文献趋势、资源匹配和创新可落地性的综合判断，仍需结合导师意见和真实数据可获得性做最终确认。</p>
</section>

<section>
<h2>二、用户输入与研究边界</h2>
<table><tbody>{brief_rows}</tbody></table>
</section>

<section>
<h2>三、筛选口径与分类标准</h2>
<table><thead><tr><th>类别</th><th>纳入标准</th><th>对选题的作用</th></tr></thead><tbody>
<tr><td>核心保留</td><td>与研究方向、关键任务、设备/数据条件和潜在创新点高度相关。</td><td>构成候选课题的主要证据。</td></tr>
<tr><td>重要参考</td><td>不完全匹配，但对方法、设备、验证、数据集、评价指标或学术故事有借鉴价值。</td><td>支撑方法设计和论文叙事。</td></tr>
<tr><td>外围/剔除</td><td>主题、场景、设备或任务偏离较大，或质量/可验证性不足。</td><td>仅作为背景或排除依据。</td></tr>
</tbody></table>
</section>

<section><h2>四、年份分布</h2>{counter_table(year_counter, limit=12)}</section>
<section><h2>五、研究对象/问题分布</h2>{counter_table(object_counter, limit=35)}</section>
<section><h2>六、任务类型统计</h2>{counter_table(task_counter, limit=35)}</section>
<section><h2>七、设备与数据统计</h2>{counter_table(equipment_counter, limit=35)}</section>
<section><h2>八、方法与模型统计</h2>{counter_table(method_counter, limit=35)}</section>
<section><h2>九、筛选分类统计</h2>{counter_table(category_counter, limit=10)}</section>

<section>
<h2>十、候选研究方向与创新点建议</h2>
{render_topics(topics)}
</section>

<section>
<h2>十一、研究方向建议</h2>
{render_list(as_list(data.get('recommendations')), 'okbox')}
</section>

<section>
<h2>十二、详细文献筛选清单</h2>
{render_records(records)}
</section>

<section>
<h2>十三、检索限制与下一步</h2>
{render_list(as_list(data.get('search_limitations')), 'warn')}
</section>
</main>
</body>
</html>"""
    return html_doc


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an HTML research topic report from JSON.")
    parser.add_argument("input_json", help="path to JSON input")
    parser.add_argument("output_html", help="path to output HTML")
    args = parser.parse_args()

    input_path = Path(args.input_json)
    output_path = Path(args.output_html)
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit("input JSON must be an object")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generate(data), encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
