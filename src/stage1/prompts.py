"""Prompt templates for Stage 1: deep research and hypothesis parsing."""

RESEARCH_PROMPT_TEMPLATE = """\
You are a research assistant helping the Yale Environmental Performance Index (EPI) team \
find alternative data sources ("proxies") for hard-to-measure environmental indicators.

## Target Indicator
- **Abbreviation**: {tla}
- **Full Name**: {indicator_name}
- **Units**: {units}
- **Source Organization**: {source_org}
- **Issue Category**: {issue_category}
- **Polarity**: {polarity} ({polarity_description})
- **Country Coverage**: ~{n_countries} countries
- **Year Range**: {year_range}

{domain_knowledge_section}\
## Your Task

Conduct a thorough literature review and data discovery exercise to find literature and datasets that could \
indicate or serve as **statistical proxies** for this indicator. A good proxy is a variable that:
1. Correlates strongly with the target indicator across countries
2. Has broader geographic coverage, more frequent updates, or easier access than the original
3. Has a plausible causal or mechanistic explanation for the correlation

## Required Sections

### 1. Causal Map
Identify the **upstream causes** and **downstream effects** of {tla}. What drives variation in \
this indicator across countries? What are its consequences? Draw a conceptual causal diagram \
in text form.

### 2. Literature-Validated Proxies
For each proxy found in published research:
- Variable name and description
- Source dataset (organization, URL, format, coverage)
- Reported correlation strength and sample
- Expected functional form (linear, log-linear, quadratic, or threshold) and reasoning
- Key caveats or limitations
- Full citation

### 3. Speculative Proxies
Based on the causal map, brainstorm **novel proxy candidates** — datasets not yet studied in \
relation to {tla} but plausibly correlated. For each:
- Variable name and description
- Why you expect a correlation (mechanistic reasoning)
- Likely data source and accessibility
- Expected direction and strength of correlation
- Expected functional form (linear is default for cross-country comparisons unless theory suggests otherwise)

### 4. Data Availability Assessment
For each candidate proxy (both literature-validated and speculative), rate:
- Geographic coverage (global/regional/sparse)
- Temporal granularity (annual/multi-year/single snapshot)
- Accessibility (open/free account/paid/restricted)
- Format (CSV/API/Excel/PDF)

### 5. Confounder Analysis
What confounders could create **spurious correlations** between {tla} and the candidate proxies? \
Especially consider GDP per capita, urbanization, population, and regional effects.

### 6. Ranked Candidates
Provide a **ranked list of your top 5-8 proxy candidates**, ordered by a combination of:
- Expected correlation strength
- Data availability and accessibility
- Geographic and temporal coverage
- Mechanistic plausibility

For each, give a one-line summary of the proxy, expected relationship direction, and data source.
"""

PARSE_PROMPT_TEMPLATE = """\
You are a structured data extraction assistant. Given a research report about proxy data sources \
for the EPI indicator **{tla}** ({indicator_name}), extract every proxy candidate mentioned \
into a structured JSON format.

## Research Report
{report_markdown}

## Citations from the report
The research report uses numbered markers like [1], [2], etc. Below is the mapping \
from marker number to source URL. Use these to populate the `references` field with \
actual URLs, and to populate `literature_evidence` with proper citations.
{citations}

## Indicator Metadata
- TLA: {tla}
- Full Name: {indicator_name}
- Units: {units}
- Source: {source_org}
- Issue Category: {issue_category}
- Polarity: {polarity}

## Instructions

Extract ALL proxy candidates mentioned in the report (both literature-validated and speculative) \
into a JSON array. Each element must conform to this schema:

```json
{{
  "id": "{tla}-H01",
  "context": {{
    "geographic_scope": "string (e.g. 'global', 'OECD countries')",
    "time_period": "string (e.g. '2010-2020')",
    "subpopulations": "string or null"
  }},
  "target_variable": "{tla}",
  "proxy_variable": "string (short name)",
  "proxy_description": "string (what this measures and why it relates)",
  "relationship": {{
    "direction": "positive|negative|nonlinear|unknown",
    "functional_form": "linear|log-linear|quadratic|threshold|unknown",
    "strength_estimate": "string or null (e.g. 'r=0.72')"
  }},
  "mechanism": "string (causal explanation)",
  "data_source": {{
    "name": "string (dataset name)",
    "organization": "string or null",
    "url": "string or null",
    "format": "string or null (CSV, API, etc.)",
    "accessibility": "open|free_account|paid|restricted|unknown",
    "coverage": "string or null (e.g. '150 countries, 2000-2022')"
  }},
  "confidence": "literature_backed|speculative|expert_opinion",
  "evidence_type": "literature_attested|programmatic_verify|manual_data_needed",
  "literature_evidence": "string or null (reported statistic + citation)",
  "caveats": ["string", ...],
  "references": ["string", ...]
}}
```

## Rules
1. Number hypotheses sequentially: {tla}-H01, {tla}-H02, etc.
2. Literature-backed hypotheses come first, then speculative ones.
3. If the report mentions a correlation coefficient, include it in `strength_estimate`.
4. If a data source URL is mentioned, include it. Otherwise set to null.
5. Set `confidence` to "literature_backed" only if a specific paper/study is cited.
6. Extract the causal/mechanistic explanation into `mechanism`.
7. Include relevant caveats from the report.
8. NEVER set direction to "unknown" if any evidence exists — infer from the mechanism. \
If the mechanism describes a positive causal link, set direction to "positive". \
If it describes a negative/inverse link, set "negative".
9. Default functional_form to "linear" unless the report explicitly mentions a non-linear \
relationship or the mechanism implies one (e.g., diminishing returns → "log-linear", \
U-shaped → "quadratic").
10. For strength_estimate, extract any quantitative mention (r-value, R², "strong", \
"moderate", "weak"). If the report says "strongly correlated", write "strong (estimated)".
11. Set `evidence_type` to classify HOW the proxy was identified:
    - "literature_attested": A specific paper/study reports a DIRECT statistical relationship \
(correlation, odds ratio, R², regression coefficient) between THIS proxy and the target \
indicator (or a very close variant of it). The key test: does the paper report a number \
you could cite as evidence of the relationship?
    - "programmatic_verify": The proxy data is available from a large public database that \
provides API or bulk CSV access (World Bank, WHO GHO, FAOSTAT, OECD, UN-Water SDG \
indicators, World Development Indicators). The verification agent can download and \
analyze this data programmatically.
    - "manual_data_needed": The proxy data exists but requires manual steps to obtain — \
registration portals (UNICEF MICS microdata), website scraping (washdata.org), \
restricted-access databases, data from paper supplementary materials, or niche \
portals without APIs.
    When a hypothesis is BOTH literature_attested AND programmatic_verify, set \
evidence_type to "literature_attested" (the literature evidence is the primary value; \
programmatic corroboration can still happen).
12. When evidence_type is "literature_attested", ALWAYS populate `literature_evidence` \
with the specific reported statistic AND citation, e.g.: \
"CPI explains 53.8% of variation in self-reported water harm (Cheng et al. 2024, Lancet Planet Health)" \
or "Odds ratios 0.42 to 0.84 for diarrheal disease (meta-analysis of 21 LMICs, JMP 2024)".
13. When evidence_type is "manual_data_needed", describe in `data_source.coverage` what \
specific steps would be needed to obtain the data (e.g. "Requires UNICEF MICS microdata \
application", "Must scrape country profiles from washdata.org").
14. For the `references` field, use the actual citation URLs from the mapping above. \
When the report cites [N], look up the URL for [N] and include it. Prefer full \
URLs over abbreviated site names.

Also extract a brief causal map summary (2-3 sentences) from the "Causal Map" section.

## Output Format
Return a JSON object with exactly this structure:
```json
{{
  "causal_map_summary": "string",
  "hypotheses": [...]
}}
```

Return ONLY valid JSON, no markdown fences or other text.
"""
