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
    except Exception:
        pass

import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("arena_result", None)

    await cl.Message(
        content=(
            "# Agent Arena\n\n"
            "Describe una idea de proyecto. El sistema extraera requisitos, "
            "recuperara contexto desde Qdrant, hara debatir a los agentes Azure/AWS/GCP, "
            "ejecutara un juez, generara una propuesta final, estimara costos y "
            "producira un diagrama de arquitectura.\n\n"
            "Despues de la propuesta, **cualquier mensaje sera tratado como pregunta de seguimiento**. "
            "Puedes preguntar lo que quieras sobre la propuesta generada.\n\n"
            "Para iniciar un **nuevo proyecto**, escribe: *\"nuevo proyecto: [tu idea]\"*"
        )
    ).send()


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

    # If there's a previous result, treat messages as follow-up by default.
    # The user must explicitly say "nuevo proyecto" or click the action to start fresh.
    previous_result = cl.user_session.get("arena_result")
    if previous_result is not None:
        lower = user_input.lower().strip()
        is_new_project = any(kw in lower for kw in [
            "nuevo proyecto", "new project", "nueva idea", "empezar de nuevo",
            "start over", "reset", "otra idea", "quiero construir", "quiero crear",
            "necesito un sistema", "diseña", "diseñar",
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
            # Clear previous result so the full pipeline runs
            cl.user_session.set("arena_result", None)

    # Full arena pipeline
    status_msg = cl.Message(content="Ejecutando Agent Arena...")
    await status_msg.send()

    # Clarification callback for interactive planner
    async def clarification_callback(questions, critical_assumptions):
        clarification_text = ""
        if questions:
            clarification_text += "**Informacion faltante:**\n"
            for q in questions:
                clarification_text += f"- {q}\n"
        if critical_assumptions:
            clarification_text += "\n**Suposiciones criticas que necesitan confirmacion:**\n"
            for a in critical_assumptions:
                clarification_text += f"- {a}\n"
        clarification_text += "\nResponde con mas detalles o escribe **continuar** para proceder con las suposiciones actuales."

        # Ask user via Chainlit
        response = await cl.AskUserMessage(
            content=clarification_text,
            timeout=120,
        ).send()

        if response and response.get("output", "").strip().lower() not in ["continuar", "continue", ""]:
            return response["output"]
        return None

    async def progress_callback(event: str, payload: dict):
        if event == "planner_started":
            async with cl.Step(name="1. Extrayendo requisitos", type="llm") as step:
                step.input = user_input
                step.output = "Planner iniciado"

        elif event == "planner_finished":
            async with cl.Step(name="1. Requisitos extraidos", type="llm", language="json") as step:
                step.input = user_input
                step.output = payload.get("planner_json", "")

        elif event == "clarification_needed":
            async with cl.Step(name="1b. Clarificacion necesaria", type="tool") as step:
                step.output = "Solicitando informacion adicional al usuario"

        elif event == "planner_rerun_started":
            async with cl.Step(name="1c. Re-ejecutando planner", type="llm") as step:
                step.output = "Planner re-ejecutado con informacion adicional"

        elif event == "retrieval_started":
            async with cl.Step(name="2. Recuperando contexto", type="retrieval", language="json") as step:
                step.input = payload.get("query_summary", "")
                step.output = "Buscando contexto Azure, AWS, GCP y neutral en Qdrant"

        elif event == "retrieval_finished":
            async with cl.Step(name="2. Contexto recuperado", type="retrieval") as step:
                step.output = payload.get("contexts_summary", "")

        elif event == "gcp_no_specific_contexts":
            async with cl.Step(name="2b. GCP sin docs especificos", type="tool") as step:
                step.output = payload.get("message", "No GCP-specific documents in Qdrant")

        elif event == "azure_agent_started":
            async with cl.Step(name="3. Azure Agent", type="llm") as step:
                step.output = "Generando propuesta Azure"

        elif event == "aws_agent_started":
            async with cl.Step(name="4. AWS Agent", type="llm") as step:
                step.output = "Generando propuesta AWS"

        elif event == "gcp_agent_started":
            async with cl.Step(name="5. GCP Agent", type="llm") as step:
                step.output = "Generando propuesta GCP"

        elif event == "citation_validation_started":
            async with cl.Step(name="6. Validando citas", type="tool") as step:
                step.output = "Comprobando CTX validos en propuestas"

        elif event == "citation_validation_finished":
            async with cl.Step(name="6. Citas validadas", type="tool") as step:
                parts = []
                for provider in ["azure", "aws", "gcp"]:
                    val = payload.get(f"{provider}_valid")
                    if val is not None:
                        parts.append(f"{provider.upper()}: {'OK' if val else 'REWRITE NEEDED'}")
                step.output = " | ".join(parts)

        elif event.endswith("_rewrite_started"):
            provider = event.replace("_rewrite_started", "").upper()
            attempt = payload.get("attempt", 1)
            async with cl.Step(name=f"6b. Reescribiendo {provider} (intento {attempt})", type="llm") as step:
                step.output = f"Reescribiendo propuesta {provider}"

        elif event.endswith("_rewrite_exhausted"):
            provider = event.replace("_rewrite_exhausted", "").upper()
            async with cl.Step(name=f"6c. {provider} rewrites agotados", type="tool") as step:
                step.output = f"Se agotaron los reintentos. IDs invalidos: {payload.get('invalid_ids', [])}"

        elif event == "judge_started":
            async with cl.Step(name="7. Judge Agent", type="llm") as step:
                step.output = "Comparando propuestas"

        elif event == "judge_finished":
            async with cl.Step(name="7. Comparacion generada", type="llm") as step:
                step.output = payload.get("final_comparison", "")

        elif event == "final_architecture_started":
            async with cl.Step(name="8. Final Architecture Agent", type="llm") as step:
                step.output = "Sintetizando la arquitectura final seleccionada"

        elif event == "cost_estimation_started":
            async with cl.Step(name="9. Estimacion de costos", type="llm") as step:
                step.output = "Estimando costos mensuales por proveedor"

        elif event == "diagram_generation_started":
            async with cl.Step(name="10. Generando diagrama", type="llm") as step:
                step.output = "Generando diagrama Mermaid de la arquitectura"

        elif event == "error":
            async with cl.Step(name="Error", type="tool") as step:
                step.output = payload.get("error", "Unknown error")

    try:
        result = await run_agent_arena_with_llm_planner_pydantic_async(
            user_idea=user_input,
            model=model,
            progress_callback=progress_callback,
            clarification_callback=clarification_callback,
        )
    finally:
        await status_msg.remove()

    # Store result for follow-up questions
    cl.user_session.set("arena_result", result)

    # Final architecture proposal
    await cl.Message(content=result.final_architecture_proposal).send()

    # Mermaid diagram
    if result.mermaid_diagram:
        await cl.Message(content=f"## Diagrama de Arquitectura\n\n```mermaid\n{result.mermaid_diagram}\n```").send()

    # Cost comparison
    if result.cost_comparison:
        cost_text = format_cost_comparison(result.cost_comparison)
        await cl.Message(content=cost_text).send()

    # Evidence trace
    trace = format_evidence_trace(result)
    await cl.Message(content="## Trazabilidad de evidencia\n\n" + trace).send()

    # Rewrite summary
    if result.rewrite_counts:
        rewrite_text = "## Resumen de reescrituras\n\n"
        for agent, count in result.rewrite_counts.items():
            rewrite_text += f"- **{agent.upper()}**: {count} reescritura(s)\n"
        await cl.Message(content=rewrite_text).send()

    # Actions for individual proposals
    actions = [
        cl.Action(name="show_azure", payload={"type": "azure"}, label="Ver propuesta Azure"),
        cl.Action(name="show_aws", payload={"type": "aws"}, label="Ver propuesta AWS"),
    ]
    if result.gcp_proposal:
        actions.append(cl.Action(name="show_gcp", payload={"type": "gcp"}, label="Ver propuesta GCP"))
    actions.append(cl.Action(name="show_comparison", payload={"type": "comparison"}, label="Ver comparativa"))
    actions.append(cl.Action(name="new_project", payload={"type": "new"}, label="Nuevo proyecto"))

    await cl.Message(
        content=(
            "Puedes ver las propuestas individuales o **hacer preguntas de seguimiento** "
            "(cualquier mensaje sera tratado como follow-up).\n\n"
            "Para iniciar un nuevo proyecto, usa el boton o escribe *\"nuevo proyecto: [idea]\"*"
        ),
        actions=actions,
    ).send()


@cl.action_callback("show_azure")
async def show_azure(action: cl.Action):
    result = cl.user_session.get("arena_result")
    if result:
        await cl.Message(content=result.azure_proposal).send()


@cl.action_callback("show_aws")
async def show_aws(action: cl.Action):
    result = cl.user_session.get("arena_result")
    if result:
        await cl.Message(content=result.aws_proposal).send()


@cl.action_callback("show_gcp")
async def show_gcp(action: cl.Action):
    result = cl.user_session.get("arena_result")
    if result and result.gcp_proposal:
        await cl.Message(content=result.gcp_proposal).send()


@cl.action_callback("show_comparison")
async def show_comparison(action: cl.Action):
    result = cl.user_session.get("arena_result")
    if result:
        await cl.Message(content=result.final_comparison).send()


@cl.action_callback("new_project")
async def new_project(action: cl.Action):
    cl.user_session.set("arena_result", None)
    await cl.Message(
        content="Sesion reiniciada. Describe tu nueva idea de proyecto."
    ).send()
