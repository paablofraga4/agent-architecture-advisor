import os
import sys

# Python 3.14 compatibility shim for AnyIO backend detection inside
# Starlette/Chainlit static responses.
if sys.version_info >= (3, 14):
    try:
        from anyio._backends._asyncio import AsyncIOBackend
        from anyio._core import _eventloop as _anyio_eventloop
        from anyio._core import _tasks as _anyio_tasks
        from anyio import to_thread as _anyio_to_thread
        from anyio import lowlevel as _anyio_lowlevel

        _orig_get_async_backend = _anyio_eventloop.get_async_backend
        _NoCurrentAsyncBackend = _anyio_eventloop.NoCurrentAsyncBackend

        def _patched_get_async_backend(asynclib_name: str | None = None):
            try:
                return _orig_get_async_backend(asynclib_name)
            except _NoCurrentAsyncBackend:
                if asynclib_name in (None, "asyncio"):
                    return AsyncIOBackend
                raise

        _anyio_eventloop.get_async_backend = _patched_get_async_backend
        _anyio_tasks.get_async_backend = _patched_get_async_backend
        _anyio_to_thread.get_async_backend = _patched_get_async_backend
        _anyio_lowlevel.get_async_backend = _patched_get_async_backend
    except Exception:
        pass

import chainlit as cl

from agent_arena.flow_visualizer import FlowState
from agent_arena.flow_svg import render_markdown as render_flow_markdown
from agent_arena.report_renderer import render_report_header, fetch_architecture_png, render_architecture_section


WELCOME = (
    "# Agent Arena\n\n"
    "Describe una idea de proyecto. Verás el pipeline de agentes en vivo (nodos), "
    "el informe final con la arquitectura recomendada y un diagrama por capas.\n\n"
    "Tras la propuesta, cualquier mensaje se trata como **pregunta de seguimiento**. "
    "Para empezar de cero escribe: *\"nuevo proyecto: [tu idea]\"*\n\n"
    "**Ideas de ejemplo para la demo:**\n"
    "- Asistente RAG sobre normativa interna de un banco con auditoría regulatoria\n"
    "- Pipeline de detección de fraude en tiempo real sobre transacciones\n"
    "- Copiloto de PMO que resuma estado de proyectos desde Jira y SharePoint\n"
    "- Extracción de PDFs farmacéuticos a BI con human-in-the-loop\n"
)


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("arena_result", None)
    await cl.Message(content=WELCOME).send()


@cl.on_message
async def on_message(message: cl.Message):
    from agent_arena.arena import (
        run_agent_arena_with_llm_planner_pydantic_async,
        handle_followup_async,
    )
    from agent_arena.config import DEFAULT_MODEL
    from agent_arena.validators import format_evidence_trace
    from agent_arena.cost_estimator import format_cost_comparison

    user_input = message.content.strip()
    model = os.getenv("AGENT_ARENA_MODEL", DEFAULT_MODEL)

    previous_result = cl.user_session.get("arena_result")
    if previous_result is not None:
        lower = user_input.lower().strip()
        is_new_project = any(kw in lower for kw in [
            "nuevo proyecto", "new project", "nueva idea", "empezar de nuevo",
            "start over", "reset", "otra idea",
        ])
        if not is_new_project:
            thinking_msg = cl.Message(content="Procesando pregunta de seguimiento...")
            await thinking_msg.send()
            try:
                response = await handle_followup_async(
                    user_question=user_input,
                    previous_result=previous_result,
                    model=model,
                )
                await thinking_msg.remove()
                await cl.Message(content=response).send()
                return
            except Exception as e:
                await thinking_msg.remove()
                await cl.Message(content=f"Error en follow-up: {e}").send()
                return
        else:
            cl.user_session.set("arena_result", None)

    # ---- Live pipeline flow as a single updating message ----
    flow_state = FlowState()
    flow_msg = cl.Message(content=render_flow_markdown(flow_state))
    await flow_msg.send()

    async def clarification_callback(questions, critical_assumptions):
        text = ""
        if questions:
            text += "**Información faltante:**\n" + "\n".join(f"- {q}" for q in questions) + "\n"
        if critical_assumptions:
            text += "\n**Suposiciones críticas:**\n" + "\n".join(f"- {a}" for a in critical_assumptions) + "\n"
        text += "\nResponde con más detalles o escribe **continuar**."
        response = await cl.AskUserMessage(content=text, timeout=120).send()
        if response and response.get("output", "").strip().lower() not in ["continuar", "continue", ""]:
            return response["output"]
        return None

    async def progress_callback(event: str, payload: dict):
        # 1) Update the live flow message
        if flow_state.apply_event(event):
            flow_msg.content = render_flow_markdown(flow_state)
            await flow_msg.update()

        # 2) Detail steps for transparency (collapsible by Chainlit)
        label_map = {
            "planner_finished":             ("Requisitos extraídos", "llm", "json", payload.get("planner_json", "")),
            "retrieval_finished":           ("Contexto recuperado", "retrieval", None, payload.get("contexts_summary", "")),
            "azure_agent_finished":         ("Propuesta Azure", "llm", "markdown", payload.get("proposal", "")),
            "aws_agent_finished":           ("Propuesta AWS", "llm", "markdown", payload.get("proposal", "")),
            "gcp_agent_finished":           ("Propuesta GCP", "llm", "markdown", payload.get("proposal", "")),
            "judge_finished":               ("Comparativa del juez", "llm", "markdown", payload.get("final_comparison", "")),
        }
        if event in label_map:
            name, type_, lang, output = label_map[event]
            kwargs = {"name": name, "type": type_}
            if lang:
                kwargs["language"] = lang
            async with cl.Step(**kwargs) as step:
                step.output = output

    try:
        result = await run_agent_arena_with_llm_planner_pydantic_async(
            user_idea=user_input,
            model=model,
            progress_callback=progress_callback,
            clarification_callback=clarification_callback,
        )
    except Exception as exc:
        flow_state.apply_event("error")
        flow_msg.content = render_flow_markdown(flow_state) + f"\n\n**Error:** {exc}"
        await flow_msg.update()
        raise

    cl.user_session.set("arena_result", result)

    # ---- Structured report ----
    await cl.Message(content=render_report_header(result)).send()

    if result.mermaid_diagram:
        png_bytes = fetch_architecture_png(result.mermaid_diagram)
        if png_bytes:
            arch_img = cl.Image(
                content=png_bytes,
                name="arquitectura",
                display="inline",
                size="large",
            )
            await cl.Message(
                content="## Arquitectura propuesta",
                elements=[arch_img],
            ).send()
        else:
            await cl.Message(content=render_architecture_section(result)).send()

    await cl.Message(
        content="## Propuesta detallada\n\n" + result.final_architecture_proposal
    ).send()

    if result.cost_comparison:
        await cl.Message(content=format_cost_comparison(result.cost_comparison)).send()

    trace = format_evidence_trace(result)
    await cl.Message(content="## Trazabilidad de evidencia\n\n" + trace).send()

    if result.rewrite_counts:
        rewrite_text = "## Reescrituras por validación\n\n" + "\n".join(
            f"- **{a.upper()}**: {c}" for a, c in result.rewrite_counts.items()
        )
        await cl.Message(content=rewrite_text).send()

    actions = [
        cl.Action(name="show_azure", payload={"type": "azure"}, label="Propuesta Azure"),
        cl.Action(name="show_aws", payload={"type": "aws"}, label="Propuesta AWS"),
    ]
    if result.gcp_proposal:
        actions.append(cl.Action(name="show_gcp", payload={"type": "gcp"}, label="Propuesta GCP"))
    actions.append(cl.Action(name="show_comparison", payload={"type": "comparison"}, label="Comparativa"))
    actions.append(cl.Action(name="new_project", payload={"type": "new"}, label="Nuevo proyecto"))

    await cl.Message(
        content=(
            "Puedes ver propuestas individuales o **preguntar sobre la propuesta**. "
            "Para empezar otra idea: *\"nuevo proyecto: [idea]\"*."
        ),
        actions=actions,
    ).send()


@cl.action_callback("show_azure")
async def show_azure(action: cl.Action):
    r = cl.user_session.get("arena_result")
    if r:
        await cl.Message(content=r.azure_proposal).send()


@cl.action_callback("show_aws")
async def show_aws(action: cl.Action):
    r = cl.user_session.get("arena_result")
    if r:
        await cl.Message(content=r.aws_proposal).send()


@cl.action_callback("show_gcp")
async def show_gcp(action: cl.Action):
    r = cl.user_session.get("arena_result")
    if r and r.gcp_proposal:
        await cl.Message(content=r.gcp_proposal).send()


@cl.action_callback("show_comparison")
async def show_comparison(action: cl.Action):
    r = cl.user_session.get("arena_result")
    if r:
        await cl.Message(content=r.final_comparison).send()


@cl.action_callback("new_project")
async def new_project(action: cl.Action):
    cl.user_session.set("arena_result", None)
    await cl.Message(content="Sesión reiniciada. Describe tu nueva idea.").send()
