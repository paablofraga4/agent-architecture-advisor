from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator


class RetrievalQueries(BaseModel):
    azure: List[str] = Field(default_factory=list)
    aws: List[str] = Field(default_factory=list)
    gcp: List[str] = Field(default_factory=list)
    neutral: List[str] = Field(default_factory=list)


class PlannerOutput(BaseModel):
    project_summary: str
    project_type: str

    required_capabilities: List[str] = Field(default_factory=list)
    non_functional_requirements: List[str] = Field(default_factory=list)

    explicit_constraints: List[str] = Field(default_factory=list)
    inferred_constraints: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)

    explicit_cloud_preferences: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    retrieval_focus: List[str] = Field(default_factory=list)

    retrieval_queries: RetrievalQueries

    @field_validator(
        "required_capabilities",
        "non_functional_requirements",
        "explicit_constraints",
        "inferred_constraints",
        "assumptions",
        "explicit_cloud_preferences",
        "missing_information",
        "retrieval_focus",
        mode="before",
    )
    @classmethod
    def ensure_list(cls, value):
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        return value


Provider = Literal["azure", "aws", "gcp", "neutral", "unknown"]
DocumentType = Literal[
    "cloud_reference",
    "service_reference",
    "architecture_pattern",
    "decision_record",
    "project_case",
    "cost_reference",
    "unknown",
]


class BusinessContext(BaseModel):
    organization_name: str = "Internal AI Architecture Team"
    department_or_area: str = "AI, Automation and Cloud Architecture"
    business_domain: str = (
        "Enterprise AI solutions, document processing, PMO support and cloud architecture advisory"
    )
    target_users: List[str] = Field(default_factory=list)
    current_priorities: List[str] = Field(default_factory=list)
    preferred_working_style: List[str] = Field(default_factory=list)
    architecture_principles: List[str] = Field(default_factory=list)
    known_constraints: List[str] = Field(default_factory=list)
    preferred_clouds: List[str] = Field(default_factory=list)
    notes: str = ""


DEFAULT_BUSINESS_CONTEXT = BusinessContext(
    organization_name="Internal AI Architecture Team",
    department_or_area="AI, Automation and Cloud Architecture",
    business_domain=(
        "Enterprise AI solutions focused on document processing, cloud architecture, "
        "multi-agent systems, PMO use cases, RAG systems and automation workflows."
    ),
    target_users=[
        "technical teams",
        "PMO teams",
        "business stakeholders",
        "cloud architecture teams",
    ],
    current_priorities=[
        "compare Azure, AWS and GCP architectures",
        "justify technical decisions with evidence",
        "avoid hallucinated architecture components",
        "produce proposals reusable in real projects",
        "prefer clear MVP-to-production evolution",
        "include cost estimation ranges per provider",
    ],
    preferred_working_style=[
        "structured architecture proposals",
        "explicit trade-offs",
        "grounded recommendations",
        "clear explanation of why each service is selected",
    ],
    architecture_principles=[
        "start with the simplest architecture that satisfies requirements",
        "separate MVP architecture from production architecture",
        "use managed services when operational overhead should be reduced",
        "use local or open-source components when experimentation is priority",
        "every recommended component must be justified by retrieved context",
    ],
    known_constraints=[],
    preferred_clouds=["azure", "aws", "gcp"],
    notes=(
        "The system acts as an architecture advisor. It should not only list services. "
        "It should explain why a service or pattern fits the specific project."
    ),
)


class RetrievedContext(BaseModel):
    context_id: str
    chunk_id: Optional[str] = None

    provider: Provider
    document_type: DocumentType

    source_file: str
    source_path: Optional[str] = None
    document_title: Optional[str] = None

    section_title: Optional[str] = None
    section_path: str

    chunk_text: str
    contextualized_chunk_text: Optional[str] = None

    score: Optional[float] = None
    rerank_score: Optional[float] = None


class ContextPack(BaseModel):
    user_idea: str
    business_context: BusinessContext

    planner_output: PlannerOutput
    final_queries: RetrievalQueries

    azure_contexts: List[RetrievedContext]
    aws_contexts: List[RetrievedContext]
    gcp_contexts: List[RetrievedContext] = Field(default_factory=list)
    neutral_contexts: List[RetrievedContext]

    azure_context_block: str
    aws_context_block: str
    gcp_context_block: str = ""


class CitationValidation(BaseModel):
    cited_ids: List[str] = Field(default_factory=list)
    invalid_ids: List[str] = Field(default_factory=list)
    has_citations: bool
    valid: bool


class CostEstimate(BaseModel):
    provider: str
    mvp_monthly_low: float
    mvp_monthly_high: float
    production_monthly_low: float
    production_monthly_high: float
    key_cost_drivers: List[str] = Field(default_factory=list)
    optimization_tips: List[str] = Field(default_factory=list)


class CostComparison(BaseModel):
    estimates: List[CostEstimate] = Field(default_factory=list)
    summary: str = ""
    cheapest_mvp: str = ""
    cheapest_production: str = ""


class ClarificationRequest(BaseModel):
    questions: List[str] = Field(default_factory=list)
    critical_assumptions: List[str] = Field(default_factory=list)
    proceed_anyway: bool = True


Confidence = Literal["clear", "close_tie", "tie"]


class JudgeVerdict(BaseModel):
    """Structured verdict from the judge agent.

    confidence:
      - "clear":     one provider is clearly better (>=20 pt gap on 0-100 scale).
      - "close_tie": a leader exists but runners-up are within 5-19 pts.
      - "tie":       two or more providers are functionally equivalent (<5 pt gap).
    """
    winner: Literal["azure", "aws", "gcp"]
    confidence: Confidence
    score_gap: int = Field(ge=0, le=100, description="Gap winner vs best runner-up.")
    runners_up_within_gap: List[Literal["azure", "aws", "gcp"]] = Field(default_factory=list)
    reasoning_summary: str


class AgentArenaResult(BaseModel):
    context_pack: ContextPack

    azure_proposal: str
    aws_proposal: str
    gcp_proposal: str = ""

    azure_validation: CitationValidation
    aws_validation: CitationValidation
    gcp_validation: Optional[CitationValidation] = None

    final_comparison: str
    final_architecture_proposal: str
    full_report: str

    cost_comparison: Optional[CostComparison] = None
    mermaid_diagram: str = ""
    rewrite_counts: dict = Field(default_factory=dict)
    verdict: Optional[JudgeVerdict] = None
