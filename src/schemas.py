"""Pydantic v2 models for hypotheses, research outputs, and verification results."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Direction(str, Enum):
    positive = "positive"
    negative = "negative"
    nonlinear = "nonlinear"
    unknown = "unknown"


class FunctionalForm(str, Enum):
    linear = "linear"
    log_linear = "log-linear"
    quadratic = "quadratic"
    nonlinear = "nonlinear"
    threshold = "threshold"
    unknown = "unknown"


class Confidence(str, Enum):
    literature_backed = "literature_backed"
    speculative = "speculative"
    expert_opinion = "expert_opinion"


class Verdict(str, Enum):
    confirmed = "confirmed"
    partially_confirmed = "partially_confirmed"
    inconclusive = "inconclusive"
    rejected = "rejected"


class VerificationMethod(str, Enum):
    statistical_test = "statistical_test"       # ran full stats on acquired data
    literature_accepted = "literature_accepted"  # accepted on citation quality
    exploratory_test = "exploratory_test"        # found approximate data, ran stats
    pending_data = "pending_data"                # could not find any usable data


class Accessibility(str, Enum):
    open = "open"
    free_account = "free_account"
    paid = "paid"
    restricted = "restricted"
    unknown = "unknown"


class EvidenceType(str, Enum):
    literature_attested = "literature_attested"   # paper reports a relationship directly
    programmatic_verify = "programmatic_verify"   # data fetchable via WB/WHO/local
    manual_data_needed = "manual_data_needed"     # data exists but requires human acquisition


# ── Hypothesis Components ──────────────────────────────────────────────────────

class Context(BaseModel):
    geographic_scope: str = Field(description="e.g. 'global', 'OECD countries', 'Sub-Saharan Africa'")
    time_period: str = Field(description="e.g. '2010-2020', '1990-2021'")
    subpopulations: Optional[str] = Field(default=None, description="e.g. 'countries with GDP > $5000'")


class Relationship(BaseModel):
    direction: Direction = Direction.unknown
    functional_form: FunctionalForm = FunctionalForm.unknown
    strength_estimate: Optional[str] = Field(default=None, description="e.g. 'r=0.72', 'moderate'")


class DataSource(BaseModel):
    name: str
    organization: Optional[str] = None
    url: Optional[str] = None
    format: Optional[str] = Field(default=None, description="e.g. 'CSV', 'API', 'Excel'")
    accessibility: Accessibility = Accessibility.unknown
    coverage: Optional[str] = Field(default=None, description="e.g. '150 countries, 2000-2022'")


class ProxyHypothesis(BaseModel):
    id: str = Field(description="e.g. 'UWD-H01'")
    context: Context
    target_variable: str = Field(description="EPI indicator TLA, e.g. 'UWD'")
    proxy_variable: str = Field(description="Short name for the proxy variable")
    proxy_description: str = Field(description="What this proxy measures and why it relates to the target")
    relationship: Relationship
    mechanism: str = Field(description="Causal/mechanistic explanation for the proxy relationship")
    data_source: DataSource
    confidence: Confidence = Confidence.speculative
    evidence_type: EvidenceType = EvidenceType.programmatic_verify
    literature_evidence: Optional[str] = Field(default=None, description="Reported statistic + citation when evidence_type is literature_attested")
    caveats: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)


# ── Stage 1 Output ─────────────────────────────────────────────────────────────

class ResearchOutput(BaseModel):
    indicator_tla: str
    hypotheses: list[ProxyHypothesis]
    causal_map_summary: str = ""
    raw_report_path: Optional[str] = None


# ── Validation Annotation ─────────────────────────────────────────────────────

class ValidationAnnotation(BaseModel):
    no_synthetic_data: bool = True
    year_alignment_ok: bool = True
    hypothesis_interpretation_ok: bool = True
    data_source_authentic: bool = True
    country_coverage_adequate: bool = True
    outlier_concerns: bool = False
    mechanistic_explanation: str = ""
    issues: list[str] = Field(default_factory=list)
    overall_assessment: str = ""


# ── Stage 2 Results ────────────────────────────────────────────────────────────

class CorrelationResult(BaseModel):
    pearson_r: Optional[float] = None
    pearson_p: Optional[float] = None
    spearman_rho: Optional[float] = None
    spearman_p: Optional[float] = None
    n_observations: Optional[int] = None
    n_countries: Optional[int] = None


class PartialCorrelationResult(BaseModel):
    partial_r: Optional[float] = None
    partial_p: Optional[float] = None
    control_variables: list[str] = Field(default_factory=list)


class FunctionalFormResult(BaseModel):
    best_form: FunctionalForm = FunctionalForm.unknown
    linear_r2: Optional[float] = None
    linear_aic: Optional[float] = None
    log_linear_r2: Optional[float] = None
    log_linear_aic: Optional[float] = None
    quadratic_r2: Optional[float] = None
    quadratic_aic: Optional[float] = None


class VerificationResult(BaseModel):
    hypothesis_id: str
    verdict: Verdict = Verdict.inconclusive
    verification_method: Optional[VerificationMethod] = None
    raw_correlation: Optional[CorrelationResult] = None
    partial_correlation: Optional[PartialCorrelationResult] = None
    functional_form: Optional[FunctionalFormResult] = None
    data_quality_notes: str = ""
    script_path: Optional[str] = None
    summary: str = ""
    validation: Optional[ValidationAnnotation] = None


# ── Pipeline Result ────────────────────────────────────────────────────────────

class PipelineResult(BaseModel):
    indicator_tla: str
    research_output: Optional[ResearchOutput] = None
    verification_results: list[VerificationResult] = Field(default_factory=list)
    summary: str = ""
