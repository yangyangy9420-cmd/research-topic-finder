---
name: research-topic-finder
description: find, screen, and rank research topics for academic papers from a broad research direction, available instruments or equipment, lab resources, and advisor priorities. use when the user asks to choose a topic, find a research direction, identify innovation points, screen recent papers, analyze a field, or generate an html literature screening and statistical report similar to a provided benchmark. outputs topic feasibility analysis, recent high-quality paper screening tables, innovation routes, risks, and a downloadable html report.
---

# Research Topic Finder

## Overview

Use this skill to turn a vague research area into concrete, feasible paper topics. The core task is not to invent a topic from thin air, but to ethically imitate and extend strong prior work: find high-quality references, extract their research patterns, match them to the user's lab resources, and propose publishable second-order innovations.

## Required inputs

Collect or infer these inputs before producing a topic plan:

1. broad research direction or keywords.
2. available instruments, datasets, software, experimental platform, lab resources, or inherited results.
3. advisor priorities, preferred methods, target journals, funding direction, or graduation constraints.

If one of these three is missing and the user expects a concrete topic recommendation, ask one concise follow-up question. If the user asks for a reusable template or skill behavior, proceed with placeholders.

## Non-negotiable ethics rules

- Treat “imitate” as learning research structure, method choices, evidence chains, and problem framing. Never copy text, fabricate citations, invent data, misrepresent methods, or recommend plagiarism.
- Never fabricate paper metadata. If bibliographic details, DOI, journal rank, citation count, or database indexing cannot be verified, mark them as “not verified” instead of guessing.
- A topic is only recommended if it can plausibly be executed with the user's resources. Avoid attractive but unrealistic “new direction” traps unless they can be connected to the lab's existing advantages.

## Workflow

### 1. Define the research boundary

Rewrite the user's input into a compact research brief:

- field and subfield.
- target object/problem.
- likely measurable variables.
- available equipment and methods.
- advisor/lab strengths.
- constraints: time, budget, sample availability, data access, expected paper level.

Use `references/methodology.md` for the adapted topic-selection logic.

### 2. Search recent and authoritative literature

For current literature, use web search or available academic/search connectors. Default to the most recent 3 years, but include older classic papers only when they define the method, dataset, or benchmark.

Search priority:

1. primary academic sources: publisher pages, DOI pages, PubMed, IEEE, ACM, Springer, Elsevier/ScienceDirect, Wiley, Taylor & Francis, MDPI, Frontiers, Nature, Science, PNAS, Cell, arXiv when appropriate.
2. open scholarly indexes: Semantic Scholar, OpenAlex, Crossref, PubMed, Europe PMC, Google Scholar snippets if accessible.
3. field authority signals: top journals/conferences, review papers, highly active groups, recent special issues, author/lab homepages, public ResearchGate or project pages.

If Google Scholar, Web of Science, Scopus, or Elsevier full text is unavailable, state the limitation and use accessible substitutes. If the user provides WoS/Scopus/EndNote/BibTeX/CSV exports, use those files as the evidence base.

Use `references/search-protocol.md` for query expansion, source selection, and screening rules.

### 3. Screen papers into a structured evidence table

For each retained paper, extract:

- title, year, authors, venue, DOI or URL.
- research object/problem.
- input data and equipment.
- task/output variable.
- method/model/theory.
- key contribution.
- limitation or gap.
- relevance category: core retained, important reference, peripheral or excluded.
- why it matters for the user's topic.

Prefer 30-120 records for a broad HTML screening report. For an initial topic scouting answer, 8-20 strong papers is enough.

### 4. Read papers using WWH to Ideas

For each cluster of papers, summarize:

- Why: why the problem matters and what field pain point it addresses.
- What: what the paper claims, measures, predicts, or proves.
- How: how the paper implements the study, especially data, equipment, model, experiment, validation, and metrics.
- Ideas: what limitation can be turned into the user's possible innovation.

Do not over-focus on introductions. For topic finding, emphasize methods, datasets, limitations, and validation paths.

### 5. Rank candidate research topics

Generate 3-8 candidate topic directions. Score each using `references/scoring-rubric.md`:

- lab resource fit.
- equipment/data feasibility.
- advisor alignment.
- literature authority and recency.
- innovation tractability.
- publication potential.
- risk and execution cost.

Explain why the highest-scoring topic is feasible, what must be verified next, and which topic should be avoided.

### 6. Generate innovation routes

Use these five ethical innovation patterns:

1. application innovation: move a mature method to a new object, scenario, dataset, or engineering problem.
2. modification innovation: add, remove, simplify, or correct a component in an existing method or theory.
3. fusion innovation: combine complementary methods, sensors, variables, models, or stages into one validated pipeline.
4. comparison innovation: benchmark multiple methods and extract an improved or application-specific recommendation.
5. method/theory innovation: propose a genuinely new method only when the user has enough experience, data, and validation capacity.

For new researchers, prefer application, modification, and fusion innovations unless the literature clearly supports a stronger route.

### 7. Produce the output

Always start with a feasibility analysis of the user's requested skill/task or topic plan. Then provide the final deliverable in one of these modes:

- quick scouting answer: short ranked topic list with evidence and next-step search queries.
- detailed topic report: literature clusters, high-quality paper table, topic scoring, innovation suggestions, risks.
- html report: a downloadable HTML file styled like a literature screening/statistical analysis report.

For HTML reports, create a JSON input file and run:

```bash
python /home/oai/skills/research-topic-finder/scripts/generate_research_topic_report.py input.json output.html
```

Use `references/html-report-spec.md` for the JSON structure and required sections. When returning the HTML file, include a sandbox download link.

## Quality checklist

Before finalizing, verify:

- the topic recommendation is tied to the user's actual direction, instruments, and advisor priorities.
- papers are recent enough for the task and source limitations are disclosed.
- every major claim about current literature is cited when web search or uploaded files are used.
- the report distinguishes evidence from inference.
- at least one recommended topic is executable with low-to-medium risk.
- innovation suggestions are specific enough to become experiments, models, datasets, or paper sections.
