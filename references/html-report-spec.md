# HTML report specification

Use the bundled script to generate a polished literature screening report from JSON.

## Required JSON fields

```json
{
  "title": "report title",
  "subtitle": "optional subtitle",
  "generated_date": "yyyy-mm-dd",
  "research_brief": {
    "broad_direction": "...",
    "equipment": "...",
    "advisor_focus": "...",
    "constraints": "..."
  },
  "records": [
    {
      "title": "paper title",
      "year": 2025,
      "authors": "first author et al.",
      "venue": "journal or conference",
      "doi": "optional",
      "url": "optional",
      "object": "research object",
      "task": "task or output",
      "input_device": "data or equipment",
      "method": "method or model",
      "key_contribution": "main contribution",
      "limitation": "gap or weakness",
      "category": "core retained | important reference | peripheral or excluded"
    }
  ],
  "candidate_topics": [
    {
      "name": "topic name",
      "academic_story": "one-sentence story",
      "score": 88,
      "label": "recommended",
      "supporting_evidence": "paper clusters or evidence",
      "innovation_point": "specific innovation route",
      "minimum_plan": "minimum experiment/data/model plan",
      "risk": "main risk",
      "mitigation": "mitigation"
    }
  ],
  "recommendations": ["..."],
  "search_limitations": ["..."]
}
```

## Required HTML sections

1. conclusion first.
2. user's input and research boundary.
3. screening criteria.
4. year distribution.
5. research object/problem distribution.
6. task distribution.
7. equipment/data distribution.
8. method distribution.
9. key research gaps.
10. candidate research topic ranking.
11. detailed paper screening table.
12. recommended search strings and next steps.
13. search limitations and source notes.

## Style guidance

Use a clean report-like style: dark blue header, white cards, compact tables, colored status pills, and bar indicators. The report should read like a strategic literature-screening memo, not a raw bibliography.
