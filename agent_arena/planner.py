from __future__ import annotations

import json
import re
from pydantic import ValidationError

from .llm import call_llm_async, _run_coroutine_in_new_thread
from .schemas import (
    BusinessContext,
    ClarificationRequest,
    DEFAULT_BUSINESS_CONTEXT,
    PlannerOutput,
    RetrievalQueries,
)


def build_requirement_extractor_prompt(
    user_idea: str,
    business_context: BusinessContext = DEFAULT_BUSINESS_CONTEXT,
) -> str:
    return f"""
You are a cloud architecture requirement extraction agent.

Your task is to analyze the user's project idea and extract structured architectural requirements.

BUSINESS CONTEXT:
{business_context.model_dump_json(indent=2)}

CRITICAL RULES:
1. Return only a JSON object.
2. Do not return a JSON Schema.
3. Do not include "$defs", "properties", "required", "title", or "type".
4. Do not include Markdown.
5. Do not include explanations outside JSON.
6. Do not propose a final architecture.
7. Do not choose specific cloud services unless the user explicitly mentions them.
8. Do not invent requirements that are not reasonably implied by the user idea.
9. Do not add cost constraints unless the user explicitly mentions cost, budget, free tier, avoiding payment, or local-only execution.
10. Do not add local-first constraints unless the user explicitly says the MVP must run locally or without cloud.
11. If the user says the solution must be hosted in Azure, AWS, or GCP from the beginning, do not include local_first or avoid_paid_cloud_resources.
12. Separate explicit constraints from inferred constraints.
13. Retrieval queries will be used to search a local knowledge base. Generate queries for Azure, AWS, GCP, and neutral.

USER PROJECT IDEA:
{user_idea}

Return exactly this JSON structure:

{{
  "project_summary": "short summary of the project",
  "project_type": "short project type label",
  "required_capabilities": [
    "capability_1",
    "capability_2"
  ],
  "non_functional_requirements": [
    "requirement_1",
    "requirement_2"
  ],
  "explicit_constraints": [
    "constraints explicitly stated by the user"
  ],
  "inferred_constraints": [
    "constraints reasonably inferred from the user idea"
  ],
  "assumptions": [
    "assumptions made because the user did not provide enough detail"
  ],
  "explicit_cloud_preferences": [
    "azure",
    "aws",
    "gcp"
  ],
  "missing_information": [
    "missing information needed to design a stronger architecture"
  ],
  "retrieval_focus": [
    "focus area 1",
    "focus area 2"
  ],
  "retrieval_queries": {{
    "azure": [
      "query for Azure knowledge base retrieval"
    ],
    "aws": [
      "query for AWS knowledge base retrieval"
    ],
    "gcp": [
      "query for GCP knowledge base retrieval"
    ],
    "neutral": [
      "query for neutral architecture patterns and project cases"
    ]
  }}
}}

Allowed capability labels include:
- document_storage
- document_upload
- document_ingestion
- text_extraction
- document_intelligence
- chunking
- semantic_retrieval
- vector_search
- hybrid_search
- metadata_filtering
- llm_answer_generation
- multi_agent_reasoning
- architecture_comparison
- judge_agent
- final_architecture_synthesis
- cloud_deployment
- event_driven_processing
- async_processing
- observability
- authentication
- cost_control
- dashboarding
- data_extraction
- data_validation
- bi_reporting
- api_layer
- containerized_deployment
- serverless_processing
- workflow_orchestration
- real_time_streaming
- batch_processing
- multi_tenant_isolation
- caching
- search_engine
- notification_system

Examples of explicit constraints:
- must be deployed in Azure
- must be deployed in AWS
- must be deployed in GCP
- must run locally
- must avoid paid cloud resources
- must use retrieved context only
- must compare Azure, AWS and GCP

Important:
Only include a constraint if it is explicitly stated or strongly implied.
Do not add avoid_paid_cloud_resources unless cost avoidance is clearly present.
Do not add local_first unless local execution is clearly present.
Return the filled JSON object itself.
"""


def extract_json_string_from_text(text: str) -> str:
    text = text.strip()

    if text.startswith("{") and text.endswith("}"):
        return text

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in LLM output:\n{text}")

    return match.group(0)


def repair_schema_like_output(data: dict) -> dict:
    if "properties" in data and isinstance(data["properties"], dict):
        properties = data["properties"]

        expected_keys = {
            "project_summary",
            "project_type",
            "required_capabilities",
            "non_functional_requirements",
            "explicit_constraints",
            "inferred_constraints",
            "assumptions",
            "explicit_cloud_preferences",
            "missing_information",
            "retrieval_focus",
            "retrieval_queries",
        }

        if any(key in properties for key in expected_keys):
            return properties

    return data


def parse_planner_output(raw_llm_output: str) -> PlannerOutput:
    json_text = extract_json_string_from_text(raw_llm_output)

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON returned by planner:\n{json_text}"
        ) from e

    data = repair_schema_like_output(data)

    try:
        return PlannerOutput.model_validate(data)
    except ValidationError as e:
        raise ValueError(
            f"Planner output does not match PlannerOutput schema:\n{e}\n\nRepaired data:\n{json.dumps(data, indent=2, ensure_ascii=False)}\n\nRaw output:\n{raw_llm_output}"
        ) from e


def build_clarification_check(planner_output: PlannerOutput) -> ClarificationRequest:
    questions = []
    critical_assumptions = []

    for item in planner_output.missing_information:
        questions.append(item)

    for assumption in planner_output.assumptions:
        lower = assumption.lower()
        if any(kw in lower for kw in ["authentication", "security", "compliance", "scale", "budget", "users", "data volume", "region"]):
            critical_assumptions.append(assumption)

    proceed_anyway = len(questions) <= 2 and len(critical_assumptions) == 0

    return ClarificationRequest(
        questions=questions,
        critical_assumptions=critical_assumptions,
        proceed_anyway=proceed_anyway,
    )


async def extract_requirements_with_llm_async(
    user_idea: str,
    business_context: BusinessContext = DEFAULT_BUSINESS_CONTEXT,
    debug: bool = False,
) -> PlannerOutput:
    prompt = build_requirement_extractor_prompt(
        user_idea=user_idea,
        business_context=business_context,
    )
    raw_output = await call_llm_async(prompt)

    if debug:
        print("RAW LLM OUTPUT")
        print("=" * 120)
        print(raw_output)

    planner_output = parse_planner_output(raw_output)
    return planner_output


def extract_requirements_with_llm(
    user_idea: str,
    business_context: BusinessContext = DEFAULT_BUSINESS_CONTEXT,
    debug: bool = False,
) -> PlannerOutput:
    return _run_coroutine_in_new_thread(
        extract_requirements_with_llm_async(
            user_idea=user_idea,
            business_context=business_context,
            debug=debug,
        )
    )


def ensure_non_empty_queries(
    planner_output: PlannerOutput,
) -> RetrievalQueries:
    queries = planner_output.retrieval_queries

    azure = queries.azure or [
        "Azure architecture for document extraction, BI reporting, multi-agent decisions and service selection rationale"
    ]

    aws = queries.aws or [
        "AWS architecture for document extraction, BI reporting, multi-agent decisions and service selection rationale"
    ]

    gcp = queries.gcp or [
        "GCP architecture for document processing, AI agents, serverless compute and managed services"
    ]

    neutral = queries.neutral or [
        "architecture patterns, project cases, and decision rationale for document to BI pipelines"
    ]

    return RetrievalQueries(
        azure=azure,
        aws=aws,
        gcp=gcp,
        neutral=neutral,
    )


def build_final_retrieval_queries(
    user_idea: str,
    planner_output: PlannerOutput,
    business_context: BusinessContext = DEFAULT_BUSINESS_CONTEXT,
) -> RetrievalQueries:
    raw_queries = ensure_non_empty_queries(planner_output)

    capabilities_text = ", ".join(planner_output.required_capabilities)
    explicit_constraints_text = ", ".join(planner_output.explicit_constraints)
    inferred_constraints_text = ", ".join(planner_output.inferred_constraints)
    assumptions_text = ", ".join(planner_output.assumptions)
    retrieval_focus_text = ", ".join(planner_output.retrieval_focus)

    business_context_text = business_context.model_dump_json(indent=2)

    common_block = f"""
User project idea:
{user_idea}

Business context:
{business_context_text}

Extracted capabilities:
{capabilities_text}

Explicit constraints:
{explicit_constraints_text}

Inferred constraints:
{inferred_constraints_text}

Assumptions:
{assumptions_text}

Retrieval focus:
{retrieval_focus_text}
"""

    azure_query = f"""{common_block}
Azure retrieval queries:
{chr(10).join("- " + q for q in raw_queries.azure)}

Retrieve Azure service references, Azure decision records, Azure project cases and Azure architecture patterns that are explicitly relevant.
"""

    aws_query = f"""{common_block}
AWS retrieval queries:
{chr(10).join("- " + q for q in raw_queries.aws)}

Retrieve AWS service references, AWS decision records, AWS project cases and AWS architecture patterns that are explicitly relevant.
"""

    gcp_query = f"""{common_block}
GCP retrieval queries:
{chr(10).join("- " + q for q in raw_queries.gcp)}

Retrieve GCP service references, GCP decision records, GCP project cases and GCP architecture patterns that are explicitly relevant.
"""

    neutral_query = f"""{common_block}
Neutral retrieval queries:
{chr(10).join("- " + q for q in raw_queries.neutral)}

Retrieve neutral architecture patterns, prior project cases, decision records, cost references and reusable implementation patterns.
"""

    return RetrievalQueries(
        azure=[azure_query],
        aws=[aws_query],
        gcp=[gcp_query],
        neutral=[neutral_query],
    )
