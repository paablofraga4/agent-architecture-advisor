from __future__ import annotations

from typing import Any, Optional
import asyncio
import os

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework.openai import OpenAIChatClient
from azure.identity import AzureCliCredential

try:
    from langfuse import Langfuse
except Exception:
    Langfuse = None

load_dotenv()


def _build_agent_client(model: str):
    """
    Prefer Microsoft Agent Framework clients.
    If Foundry env vars are present, use Foundry.
    Otherwise fall back to OpenAI provider via OPENAI_API_KEY for local compatibility.
    """
    foundry_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    foundry_model = os.getenv("FOUNDRY_MODEL") or model

    if foundry_endpoint:
        return FoundryChatClient(
            project_endpoint=foundry_endpoint,
            model=foundry_model,
            credential=AzureCliCredential(),
        )

    return OpenAIChatClient(model=model)


def _build_langfuse_client():
    if Langfuse is None:
        return None

    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST")

    if not public_key or not secret_key:
        return None

    try:
        return Langfuse(
            public_key=public_key,
            secret_key=secret_key,
            host=host,
        )
    except Exception as exc:
        print(f"Langfuse disabled due to initialization error: {exc}")
        return None


LANGFUSE_CLIENT = _build_langfuse_client()


def _lf_start_trace(name: str, input_data: Any = None, metadata: Optional[dict] = None):
    if LANGFUSE_CLIENT is None:
        return None
    try:
        return LANGFUSE_CLIENT.trace(
            name=name,
            input=input_data,
            metadata=metadata or {},
        )
    except Exception:
        return None


def _lf_start_span(parent: Any, name: str, input_data: Any = None, metadata: Optional[dict] = None):
    if parent is None:
        return None

    span_fn = getattr(parent, "span", None)
    if callable(span_fn):
        try:
            return span_fn(name=name, input=input_data, metadata=metadata or {})
        except Exception:
            pass

    generation_fn = getattr(parent, "generation", None)
    if callable(generation_fn):
        try:
            return generation_fn(name=name, input=input_data, metadata=metadata or {})
        except Exception:
            pass

    return None


def _lf_update(
    obs: Any,
    *,
    metadata: Optional[dict] = None,
    tags: Optional[list[str]] = None,
    input_data: Any = None,
    output_data: Any = None,
):
    if obs is None:
        return

    update_fn = getattr(obs, "update", None)
    if not callable(update_fn):
        return

    payload = {}
    if metadata is not None:
        payload["metadata"] = metadata
    if tags is not None:
        payload["tags"] = tags
    if input_data is not None:
        payload["input"] = input_data
    if output_data is not None:
        payload["output"] = output_data

    if not payload:
        return

    try:
        update_fn(**payload)
    except Exception:
        pass


def _lf_end(obs: Any, output_data: Any = None, error: Optional[Exception] = None):
    if obs is None:
        return

    end_fn = getattr(obs, "end", None)
    if not callable(end_fn):
        return

    payload = {}
    if output_data is not None:
        payload["output"] = output_data
    if error is not None:
        payload["status_message"] = str(error)

    try:
        end_fn(**payload)
    except TypeError:
        try:
            end_fn(output_data)
        except Exception:
            pass
    except Exception:
        pass


def _lf_flush():
    if LANGFUSE_CLIENT is None:
        return
    flush_fn = getattr(LANGFUSE_CLIENT, "flush", None)
    if callable(flush_fn):
        try:
            flush_fn()
        except Exception:
            pass


def _stringify_agent_response(response: Any) -> str:
    if hasattr(response, "messages") and getattr(response, "messages", None):
        text_parts = [m.text for m in response.messages if getattr(m, "text", None)]
        if text_parts:
            return "\n".join(text_parts).strip()
    if isinstance(response, list):
        return "\n".join(_stringify_agent_response(item) for item in response).strip()
    return str(response).strip()


def _create_workflow_backed_agent(
    *,
    model: str,
    name: str,
    instructions: str,
    description: Optional[str] = None,
) -> Agent:
    # Keep the model/provider layer on Microsoft Agent Framework, but avoid wrapping
    # one-shot calls in a nested workflow-as-agent. That pattern triggers notebook timeout issues.
    return Agent(
        client=_build_agent_client(model=model),
        name=name,
        instructions=instructions,
        description=description,
    )


async def call_llm_async(
    prompt: str,
    model: str = "gpt-4o-mini",
    trace: Any = None,
    span_name: str = "llm_call",
    metadata: Optional[dict] = None,
    instructions: Optional[str] = None,
    agent_name: str = "single_shot_agent",
) -> str:
    agent = _create_workflow_backed_agent(
        model=model,
        name=agent_name,
        instructions=instructions or "You are a precise architecture assistant. Follow the user prompt strictly.",
    )

    llm_span = _lf_start_span(
        parent=trace,
        name=span_name,
        input_data=prompt,
        metadata={"model": model, "runtime": "agent_framework_agent", **(metadata or {})},
    )

    try:
        response = await agent.run(prompt)
        result_text = _stringify_agent_response(response)
        _lf_end(llm_span, output_data=result_text)
        return result_text
    except Exception as exc:
        _lf_end(llm_span, error=exc)
        raise


def _run_coroutine_in_new_thread(coro):
    import threading

    result_holder = {}
    error_holder = {}

    def runner():
        try:
            result_holder["value"] = asyncio.run(coro)
        except Exception as exc:
            error_holder["error"] = exc

    thread = threading.Thread(target=runner, daemon=True)
    thread.start()
    thread.join()

    if "error" in error_holder:
        raise error_holder["error"]

    return result_holder["value"]


def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    # Notebook-safe sync wrapper for async Agent Framework APIs.
    return _run_coroutine_in_new_thread(call_llm_async(prompt=prompt, model=model))
