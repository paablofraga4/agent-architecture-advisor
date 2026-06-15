from __future__ import annotations

from typing import Awaitable, Callable, Optional, Any
import asyncio

from .schemas import (
    AgentArenaResult,
    BusinessContext,
    ContextPack,
    DEFAULT_BUSINESS_CONTEXT,
)
from .config import (
    AZURE_AGENT_MODEL,
    AWS_AGENT_MODEL,
    GCP_AGENT_MODEL,
    JUDGE_MODEL,
    FINAL_MODEL,
    COST_MODEL,
    DIAGRAM_MODEL,
    GCP_ENABLED,
    INTERACTIVE_PLANNER,
    MAX_REWRITE_RETRIES,
)
from .planner import (
    build_clarification_check,
    build_final_retrieval_queries,
    extract_requirements_with_llm_async,
)
from .retrieval import (
    build_contexts_summary,
    format_context_block_typed,
    retrieve_typed_contexts,
)
from .prompts import (
    build_aws_agent_prompt_typed,
    build_azure_agent_prompt_typed,
    build_gcp_agent_prompt_typed,
    build_final_architecture_prompt_typed,
    build_final_rewrite_prompt_typed,
    build_judge_prompt_typed,
    build_rewrite_prompt_typed,
    build_followup_prompt,
)
from .validators import get_valid_context_ids_typed, validate_citations_typed
from .cost_estimator import estimate_costs_async
from .diagram import generate_diagram_async
from .llm import (
    call_llm_async,
    _lf_end,
    _lf_flush,
    _lf_start_span,
    _lf_start_trace,
    _lf_update,
    _run_coroutine_in_new_thread,
)

ProgressCallback = Callable[[str, dict], Awaitable[None]]
ClarificationCallback = Callable[[list[str], list[str]], Awaitable[Optional[str]]]


async def _emit(progress_callback: Optional[ProgressCallback], event: str, payload: Optional[dict] = None):
    if progress_callback is not None:
        await progress_callback(event, payload or {})


async def build_dynamic_context_pack_with_llm_planner_async(
    user_idea: str,
    business_context: BusinessContext = DEFAULT_BUSINESS_CONTEXT,
    top_k_provider: int = 8,
    top_k_neutral: int = 6,
    progress_callback: Optional[ProgressCallback] = None,
    clarification_callback: Optional[ClarificationCallback] = None,
) -> ContextPack:
    await _emit(progress_callback, "planner_started", {"user_idea": user_idea})
    planner_output = await extract_requirements_with_llm_async(
        user_idea=user_idea,
        business_context=business_context,
    )
    await _emit(
        progress_callback,
        "planner_finished",
        {"planner_json": planner_output.model_dump_json(indent=2)},
    )

    # Interactive clarification: ask user about missing info / critical assumptions
    if INTERACTIVE_PLANNER and clarification_callback:
        clarification = build_clarification_check(planner_output)
        if not clarification.proceed_anyway and (clarification.questions or clarification.critical_assumptions):
            await _emit(progress_callback, "clarification_needed", {
                "questions": clarification.questions,
                "critical_assumptions": clarification.critical_assumptions,
            })
            user_response = await clarification_callback(
                clarification.questions,
                clarification.critical_assumptions,
            )
            if user_response:
                # Re-run planner with enriched idea
                enriched_idea = f"{user_idea}\n\nAdditional context from user:\n{user_response}"
                await _emit(progress_callback, "planner_rerun_started", {})
                planner_output = await extract_requirements_with_llm_async(
                    user_idea=enriched_idea,
                    business_context=business_context,
                )
                user_idea = enriched_idea
                await _emit(progress_callback, "planner_rerun_finished", {
                    "planner_json": planner_output.model_dump_json(indent=2),
                })

    final_queries = build_final_retrieval_queries(
        user_idea=user_idea,
        planner_output=planner_output,
        business_context=business_context,
    )

    await _emit(
        progress_callback,
        "retrieval_started",
        {"query_summary": final_queries.model_dump_json(indent=2)},
    )

    azure_contexts = retrieve_typed_contexts(
        query=final_queries.azure[0],
        provider="azure",
        top_k=top_k_provider,
    )

    aws_contexts = retrieve_typed_contexts(
        query=final_queries.aws[0],
        provider="aws",
        top_k=top_k_provider,
    )

    gcp_contexts = []
    if GCP_ENABLED and final_queries.gcp:
        try:
            gcp_contexts = retrieve_typed_contexts(
                query=final_queries.gcp[0],
                provider="gcp",
                top_k=top_k_provider,
            )
        except Exception:
            gcp_contexts = []

    neutral_contexts = retrieve_typed_contexts(
        query=final_queries.neutral[0],
        provider="neutral",
        top_k=top_k_neutral,
    )

    azure_context_block = format_context_block_typed(
        azure_contexts + neutral_contexts
    )

    aws_context_block = format_context_block_typed(
        aws_contexts + neutral_contexts
    )

    # GCP uses its own contexts + neutral. If no GCP-specific docs are indexed,
    # still build a context block from neutral contexts so the GCP agent can
    # produce a proposal based on patterns and project cases.
    gcp_context_block = ""
    if GCP_ENABLED:
        gcp_block_contexts = gcp_contexts + neutral_contexts if gcp_contexts else neutral_contexts
        if gcp_block_contexts:
            gcp_context_block = format_context_block_typed(gcp_block_contexts)
            if not gcp_contexts:
                await _emit(progress_callback, "gcp_no_specific_contexts", {
                    "message": "No se encontraron documentos GCP especificos en Qdrant. "
                               "El agente GCP usara solo contextos neutrales (patrones, casos). "
                               "Reindexe la knowledge base para incluir documentos GCP.",
                })

    context_pack = ContextPack(
        user_idea=user_idea,
        business_context=business_context,
        planner_output=planner_output,
        final_queries=final_queries,
        azure_contexts=azure_contexts,
        aws_contexts=aws_contexts,
        gcp_contexts=gcp_contexts,
        neutral_contexts=neutral_contexts,
        azure_context_block=azure_context_block,
        aws_context_block=aws_context_block,
        gcp_context_block=gcp_context_block,
    )

    await _emit(
        progress_callback,
        "retrieval_finished",
        {
            "azure_contexts": len(azure_contexts),
            "aws_contexts": len(aws_contexts),
            "gcp_contexts": len(gcp_contexts),
            "neutral_contexts": len(neutral_contexts),
            "contexts_summary": build_contexts_summary(context_pack),
        },
    )

    return context_pack


def build_dynamic_context_pack_with_llm_planner(
    user_idea: str,
    business_context: BusinessContext = DEFAULT_BUSINESS_CONTEXT,
    top_k_provider: int = 8,
    top_k_neutral: int = 6,
) -> ContextPack:
    return _run_coroutine_in_new_thread(
        build_dynamic_context_pack_with_llm_planner_async(
            user_idea=user_idea,
            business_context=business_context,
            top_k_provider=top_k_provider,
            top_k_neutral=top_k_neutral,
        )
    )


async def _rewrite_with_retries(
    proposal: str,
    valid_ids: set[str],
    context_block: str,
    agent_name: str,
    model: str,
    trace: Any,
    progress_callback: Optional[ProgressCallback],
    event_prefix: str,
) -> tuple[str, int]:
    """Rewrite a proposal up to MAX_REWRITE_RETRIES times. Returns (proposal, rewrite_count)."""
    validation = validate_citations_typed(proposal=proposal, valid_context_ids=valid_ids)
    rewrites = 0

    while not validation.valid and rewrites < MAX_REWRITE_RETRIES:
        rewrites += 1
        await _emit(progress_callback, f"{event_prefix}_rewrite_started", {"attempt": rewrites})
        rewrite_prompt = build_rewrite_prompt_typed(
            original_proposal=proposal,
            valid_context_ids=valid_ids,
            context_block=context_block,
            agent_name=agent_name,
        )
        proposal = await call_llm_async(
            prompt=rewrite_prompt,
            model=model,
            trace=trace,
            span_name=f"{event_prefix}_rewrite_{rewrites}",
            metadata={"agent": event_prefix, "rewrite": True, "attempt": rewrites},
            agent_name=f"{event_prefix}_rewrite_agent",
        )
        validation = validate_citations_typed(proposal=proposal, valid_context_ids=valid_ids)
        await _emit(progress_callback, f"{event_prefix}_rewrite_finished", {
            "proposal": proposal,
            "valid": validation.valid,
            "attempt": rewrites,
        })

    if not validation.valid:
        await _emit(progress_callback, f"{event_prefix}_rewrite_exhausted", {
            "invalid_ids": validation.invalid_ids,
            "attempts": rewrites,
        })

    return proposal, rewrites


async def run_agent_arena_with_llm_planner_pydantic_async(
    user_idea: str,
    model: str = "gpt-4o-mini",
    business_context: BusinessContext = DEFAULT_BUSINESS_CONTEXT,
    progress_callback: Optional[ProgressCallback] = None,
    clarification_callback: Optional[ClarificationCallback] = None,
) -> AgentArenaResult:
    """
    Full Agent Arena pipeline with Azure, AWS, and optionally GCP agents.
    Includes interactive planner, cost estimation, diagram generation, and retry limits.
    """
    rewrite_counts = {}

    run_trace = _lf_start_trace(
        name="agent_arena_run",
        input_data={"user_idea": user_idea, "model": model},
        metadata={
            "pipeline": "dynamic_llm_planner_pydantic",
            "runtime": "microsoft_agent_framework",
            "tracing": "langfuse_optional",
            "gcp_enabled": GCP_ENABLED,
        },
    )

    try:
        context_pack_span = _lf_start_span(
            parent=run_trace,
            name="build_context_pack",
            input_data={"user_idea": user_idea},
        )
        context_pack = await build_dynamic_context_pack_with_llm_planner_async(
            user_idea=user_idea,
            business_context=business_context,
            progress_callback=progress_callback,
            clarification_callback=clarification_callback,
        )
        _lf_end(
            context_pack_span,
            output_data={
                "azure_contexts": len(context_pack.azure_contexts),
                "aws_contexts": len(context_pack.aws_contexts),
                "gcp_contexts": len(context_pack.gcp_contexts),
                "neutral_contexts": len(context_pack.neutral_contexts),
            },
        )

        planner = context_pack.planner_output
        cloud_prefs = planner.explicit_cloud_preferences or []
        merged_constraints = set(
            planner.explicit_constraints + planner.inferred_constraints
        )
        business_tags = [
            "pipeline:agent_arena",
            f"project_type:{planner.project_type or 'unknown'}",
            f"azure_pref:{'azure' in cloud_prefs}",
            f"aws_pref:{'aws' in cloud_prefs}",
            f"gcp_pref:{'gcp' in cloud_prefs}",
            f"local_first:{'local_first' in merged_constraints}",
        ]
        for cap in planner.required_capabilities[:3]:
            business_tags.append(f"cap:{cap}")

        _lf_update(
            run_trace,
            metadata={
                "project_summary": planner.project_summary,
                "project_type": planner.project_type,
                "required_capabilities": planner.required_capabilities,
                "explicit_constraints": planner.explicit_constraints,
                "inferred_constraints": planner.inferred_constraints,
                "assumptions": planner.assumptions,
                "explicit_cloud_preferences": planner.explicit_cloud_preferences,
            },
            tags=business_tags,
        )

        prompt_span = _lf_start_span(
            parent=run_trace,
            name="build_agent_prompts",
            input_data={"user_idea": user_idea},
        )
        azure_prompt = build_azure_agent_prompt_typed(context_pack)
        aws_prompt = build_aws_agent_prompt_typed(context_pack)
        gcp_prompt = build_gcp_agent_prompt_typed(context_pack) if GCP_ENABLED and context_pack.gcp_context_block else None
        _lf_end(
            prompt_span,
            output_data={
                "azure_prompt_chars": len(azure_prompt),
                "aws_prompt_chars": len(aws_prompt),
                "gcp_prompt_chars": len(gcp_prompt) if gcp_prompt else 0,
            },
        )

        # Generate proposals concurrently
        proposal_span = _lf_start_span(
            parent=run_trace,
            name="generate_cloud_proposals",
            metadata={"execution": "concurrent"},
        )
        await _emit(progress_callback, "azure_agent_started", {})
        await _emit(progress_callback, "aws_agent_started", {})
        if gcp_prompt:
            await _emit(progress_callback, "gcp_agent_started", {})

        azure_model = AZURE_AGENT_MODEL if AZURE_AGENT_MODEL != model else model
        aws_model = AWS_AGENT_MODEL if AWS_AGENT_MODEL != model else model
        gcp_model = GCP_AGENT_MODEL if GCP_AGENT_MODEL != model else model

        tasks = [
            call_llm_async(
                prompt=azure_prompt, model=azure_model, trace=run_trace,
                span_name="azure_agent_generation", metadata={"agent": "azure"},
                agent_name="azure_architecture_agent",
            ),
            call_llm_async(
                prompt=aws_prompt, model=aws_model, trace=run_trace,
                span_name="aws_agent_generation", metadata={"agent": "aws"},
                agent_name="aws_architecture_agent",
            ),
        ]
        if gcp_prompt:
            tasks.append(
                call_llm_async(
                    prompt=gcp_prompt, model=gcp_model, trace=run_trace,
                    span_name="gcp_agent_generation", metadata={"agent": "gcp"},
                    agent_name="gcp_architecture_agent",
                )
            )

        results = await asyncio.gather(*tasks)
        azure_proposal = results[0]
        aws_proposal = results[1]
        gcp_proposal = results[2] if gcp_prompt else ""

        await _emit(progress_callback, "azure_agent_finished", {"proposal": azure_proposal})
        await _emit(progress_callback, "aws_agent_finished", {"proposal": aws_proposal})
        if gcp_proposal:
            await _emit(progress_callback, "gcp_agent_finished", {"proposal": gcp_proposal})
        _lf_end(proposal_span, output_data={
            "azure_chars": len(azure_proposal),
            "aws_chars": len(aws_proposal),
            "gcp_chars": len(gcp_proposal),
        })

        # Collect valid context IDs
        azure_valid_ids = get_valid_context_ids_typed(context_pack=context_pack, agent="azure")
        aws_valid_ids = get_valid_context_ids_typed(context_pack=context_pack, agent="aws")
        gcp_valid_ids = get_valid_context_ids_typed(context_pack=context_pack, agent="gcp") if gcp_proposal else set()
        all_valid_ids = get_valid_context_ids_typed(context_pack=context_pack, agent="all")

        # Citation validation with retry limits
        await _emit(progress_callback, "citation_validation_started", {})
        azure_validation = validate_citations_typed(proposal=azure_proposal, valid_context_ids=azure_valid_ids)
        aws_validation = validate_citations_typed(proposal=aws_proposal, valid_context_ids=aws_valid_ids)
        gcp_validation = validate_citations_typed(proposal=gcp_proposal, valid_context_ids=gcp_valid_ids) if gcp_proposal else None

        await _emit(progress_callback, "citation_validation_finished", {
            "azure_valid": azure_validation.valid,
            "aws_valid": aws_validation.valid,
            "gcp_valid": gcp_validation.valid if gcp_validation else None,
        })

        # Rewrite with retry limits
        if not azure_validation.valid:
            azure_proposal, azure_rewrites = await _rewrite_with_retries(
                azure_proposal, azure_valid_ids, context_pack.azure_context_block,
                "Azure Architecture Agent", azure_model, run_trace, progress_callback, "azure",
            )
            azure_validation = validate_citations_typed(azure_proposal, azure_valid_ids)
            rewrite_counts["azure"] = azure_rewrites

        if not aws_validation.valid:
            aws_proposal, aws_rewrites = await _rewrite_with_retries(
                aws_proposal, aws_valid_ids, context_pack.aws_context_block,
                "AWS Architecture Agent", aws_model, run_trace, progress_callback, "aws",
            )
            aws_validation = validate_citations_typed(aws_proposal, aws_valid_ids)
            rewrite_counts["aws"] = aws_rewrites

        if gcp_validation and not gcp_validation.valid:
            gcp_proposal, gcp_rewrites = await _rewrite_with_retries(
                gcp_proposal, gcp_valid_ids, context_pack.gcp_context_block,
                "GCP Architecture Agent", gcp_model, run_trace, progress_callback, "gcp",
            )
            gcp_validation = validate_citations_typed(gcp_proposal, gcp_valid_ids)
            rewrite_counts["gcp"] = gcp_rewrites

        # Judge comparison
        await _emit(progress_callback, "judge_started", {})
        judge_model = JUDGE_MODEL if JUDGE_MODEL != model else model
        judge_prompt = build_judge_prompt_typed(
            context_pack=context_pack,
            azure_proposal=azure_proposal,
            aws_proposal=aws_proposal,
            gcp_proposal=gcp_proposal,
        )
        final_comparison = await call_llm_async(
            prompt=judge_prompt, model=judge_model, trace=run_trace,
            span_name="judge_generation", metadata={"agent": "judge"},
            agent_name="architecture_judge_agent",
        )
        await _emit(progress_callback, "judge_finished", {"final_comparison": final_comparison})

        # Final architecture
        await _emit(progress_callback, "final_architecture_started", {})
        final_model = FINAL_MODEL if FINAL_MODEL != model else model
        final_architecture_prompt = build_final_architecture_prompt_typed(
            context_pack=context_pack,
            azure_proposal=azure_proposal,
            aws_proposal=aws_proposal,
            final_comparison=final_comparison,
            gcp_proposal=gcp_proposal,
        )
        final_architecture_proposal = await call_llm_async(
            prompt=final_architecture_prompt, model=final_model, trace=run_trace,
            span_name="final_architecture_generation", metadata={"agent": "final_architecture"},
            agent_name="final_architecture_agent",
        )

        final_validation = validate_citations_typed(
            proposal=final_architecture_proposal, valid_context_ids=all_valid_ids,
        )

        if not final_validation.valid:
            all_context_block = format_context_block_typed(
                context_pack.azure_contexts
                + context_pack.aws_contexts
                + context_pack.gcp_contexts
                + context_pack.neutral_contexts
            )
            final_architecture_proposal, final_rewrites = await _rewrite_with_retries(
                final_architecture_proposal, all_valid_ids, all_context_block,
                "Final Architecture Agent", final_model, run_trace, progress_callback, "final_architecture",
            )
            final_validation = validate_citations_typed(
                proposal=final_architecture_proposal, valid_context_ids=all_valid_ids,
            )
            rewrite_counts["final"] = final_rewrites

        await _emit(progress_callback, "final_architecture_finished", {
            "proposal": final_architecture_proposal,
        })

        # Cost estimation (concurrent with diagram generation)
        await _emit(progress_callback, "cost_estimation_started", {})
        await _emit(progress_callback, "diagram_generation_started", {})

        cost_model = COST_MODEL if COST_MODEL != model else model
        diagram_model = DIAGRAM_MODEL if DIAGRAM_MODEL != model else model

        cost_task = estimate_costs_async(
            context_pack=context_pack,
            azure_proposal=azure_proposal,
            aws_proposal=aws_proposal,
            gcp_proposal=gcp_proposal,
            model=cost_model,
            trace=run_trace,
        )
        diagram_task = generate_diagram_async(
            final_proposal=final_architecture_proposal,
            user_idea=context_pack.user_idea,
            model=diagram_model,
            trace=run_trace,
        )

        cost_result, diagram_result = await asyncio.gather(
            cost_task, diagram_task, return_exceptions=True
        )

        # Handle cost estimation failure gracefully
        if isinstance(cost_result, Exception):
            print(f"  [WARN] Cost estimation failed: {cost_result}")
            await _emit(progress_callback, "cost_estimation_error", {"error": str(cost_result)})
            cost_comparison = None
        else:
            cost_comparison = cost_result
            await _emit(progress_callback, "cost_estimation_finished", {
                "cost_comparison": cost_comparison.model_dump_json(indent=2),
            })

        # Handle diagram generation failure gracefully
        if isinstance(diagram_result, Exception):
            print(f"  [WARN] Diagram generation failed: {diagram_result}")
            await _emit(progress_callback, "diagram_generation_error", {"error": str(diagram_result)})
            mermaid_diagram = ""
        else:
            mermaid_diagram = diagram_result
            await _emit(progress_callback, "diagram_generation_finished", {
                "mermaid_diagram": mermaid_diagram,
            })

        full_report = final_architecture_proposal

        result = AgentArenaResult(
            context_pack=context_pack,
            azure_proposal=azure_proposal,
            aws_proposal=aws_proposal,
            gcp_proposal=gcp_proposal,
            azure_validation=azure_validation,
            aws_validation=aws_validation,
            gcp_validation=gcp_validation,
            final_comparison=final_comparison,
            final_architecture_proposal=final_architecture_proposal,
            full_report=full_report,
            cost_comparison=cost_comparison,
            mermaid_diagram=mermaid_diagram,
            rewrite_counts=rewrite_counts,
        )

        _lf_update(
            run_trace,
            metadata={
                "azure_valid": result.azure_validation.valid,
                "aws_valid": result.aws_validation.valid,
                "gcp_valid": result.gcp_validation.valid if result.gcp_validation else None,
                "final_valid": final_validation.valid,
                "rewrite_counts": rewrite_counts,
            },
            tags=[
                f"azure_valid:{result.azure_validation.valid}",
                f"aws_valid:{result.aws_validation.valid}",
                f"gcp_enabled:{GCP_ENABLED}",
                f"final_valid:{final_validation.valid}",
            ],
        )

        _lf_end(run_trace, output_data={"status": "success"})
        _lf_flush()
        return result

    except Exception as exc:
        await _emit(progress_callback, "error", {"error": str(exc)})
        _lf_end(run_trace, error=exc)
        _lf_flush()
        raise


async def handle_followup_async(
    user_question: str,
    previous_result: AgentArenaResult,
    model: str = "gpt-4o-mini",
) -> str:
    """Handle a follow-up question using the previous result's context."""
    summary = (
        f"Azure proposal:\n{previous_result.azure_proposal[:500]}...\n\n"
        f"AWS proposal:\n{previous_result.aws_proposal[:500]}...\n\n"
    )
    if previous_result.gcp_proposal:
        summary += f"GCP proposal:\n{previous_result.gcp_proposal[:500]}...\n\n"
    summary += f"Final proposal:\n{previous_result.final_architecture_proposal}"

    prompt = build_followup_prompt(
        context_pack=previous_result.context_pack,
        previous_result_summary=summary,
        user_question=user_question,
    )
    return await call_llm_async(
        prompt=prompt,
        model=model,
        agent_name="followup_agent",
    )


def run_agent_arena_with_llm_planner_pydantic(
    user_idea: str,
    model: str = "gpt-4o-mini",
    business_context: BusinessContext = DEFAULT_BUSINESS_CONTEXT,
) -> AgentArenaResult:
    """Sync wrapper to keep existing notebook cells compatible."""
    return _run_coroutine_in_new_thread(
        run_agent_arena_with_llm_planner_pydantic_async(
            user_idea=user_idea,
            model=model,
            business_context=business_context,
        )
    )
