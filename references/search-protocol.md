# Search protocol for recent research-topic discovery

## Default search window

Use the latest 3 years by default. Include older papers only when they are foundational, define a benchmark, describe the lab's inherited method, or are heavily reused by recent work.

## Query expansion pattern

Build queries from four axes:

1. object/problem: material, crop, disease, device, structure, process, population, phenomenon.
2. task/output: classification, prediction, detection, segmentation, regression, mechanism, optimization, shelf life, durability, safety, performance, diagnosis, monitoring.
3. method/equipment: instrument names, sensor type, model family, software, experiment platform, simulation method.
4. constraints: low cost, lightweight, field deployable, real time, explainable, robust, small sample, multimodal, time series.

Example query set:

- `[object] [task] [method] 2024 2025 2026 review`
- `[object] [task] [equipment] "machine learning"`
- `[object] "shelf life" RGB image deep learning`
- `[method] [domain] limitation future work`
- `[advisor focus keyword] [domain] top journal`

## Source priority

1. Publisher/DOI pages and official journal pages.
2. Bibliographic indexes: PubMed, Crossref, OpenAlex, Semantic Scholar, IEEE, ACM, arXiv, Europe PMC, SSRN when relevant.
3. Academic search engines: Google Scholar when accessible; otherwise use public snippets cautiously.
4. Database exports from the user: Web of Science, Scopus, CNKI, EndNote, Zotero, BibTeX, CSV, RIS.
5. Lab/homepage evidence: principal investigator pages, project pages, GitHub repositories, datasets.

## Screening categories

- core retained: directly matches direction, task, data/equipment, and innovation route.
- important reference: not a direct match, but strongly informs method, equipment, validation, benchmark, or field trend.
- peripheral or excluded: weak match, outdated without foundational value, pure background, not feasible, not peer-reviewed unless preprint is specifically useful.

## High-quality signals

Use multiple signals; do not rely on one alone:

- recent top or mainstream journal/conference in the field.
- strong publisher or society venue.
- review article in reputable journal.
- repeatedly cited benchmark or dataset.
- active leading group or author.
- direct method/equipment match to the user.
- clear data, validation, metrics, and reproducibility.

## Search limitations to disclose

Disclose when:

- Google Scholar, Web of Science, Scopus, ScienceDirect, or full text is not accessible.
- ranking metrics or citation counts cannot be verified.
- only abstracts/snippets were available.
- preprints are used.
- the last-3-year window yields too few direct papers and older evidence is added.
