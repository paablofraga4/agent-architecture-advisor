# Frontend (Next.js + React Flow) — scaffold guide

The backend `api.py` exposes everything a frontend needs. This folder is a
placeholder describing the contract and the recommended stack. The Next.js
app is **not built in this MVP** because it's 2-3 weeks of work; the
backend API is production-shaped so the frontend can be plugged in later
without changing arena/agent code.

## Stack

- **Next.js 14 (App Router) + TypeScript**
- **React Flow** for the live pipeline graph (nodes/edges driven by SSE events)
- **TanStack Query** for `/arena/runs` and `/arena/runs/{id}`
- **shadcn/ui + Tailwind** for the report layout
- **react-markdown + rehype-raw** to render the architecture markdown
- **next-themes** for dark mode (default)

## API contract

### POST /arena/run (SSE)

Body:
```json
{ "idea": "...", "client_id": "acme", "model": "gpt-4o-mini" }
```

The response is a Server-Sent Events stream. Events to listen for:

| Event                          | Payload                                                  |
|--------------------------------|----------------------------------------------------------|
| `planner_started/_finished`    | `{ planner_json }`                                        |
| `retrieval_started/_finished`  | `{ contexts_summary, ... }`                              |
| `azure_agent_started/_finished`| `{ proposal }`                                            |
| `aws_agent_started/_finished`  | `{ proposal }`                                            |
| `gcp_agent_started/_finished`  | `{ proposal }`                                            |
| `citation_validation_*`        | `{ azure_valid, aws_valid, gcp_valid }`                   |
| `judge_started/_finished`      | `{ final_comparison }`                                    |
| `verdict_finished`             | `{ verdict: JudgeVerdict (json string) }`                |
| `specialists_started/_finished`| `{ count, findings_total, summary }`                     |
| `final_architecture_*`         | `{ proposal }`                                            |
| `cost_estimation_*`            | `{ cost_comparison }`                                     |
| `diagram_generation_*`         | `{ mermaid_diagram }` (actually D2 code now)             |
| `audit_saved`                  | `{ run_id, path, kb_hash, prompts_hash }`                |
| `result`                       | Full `AgentArenaResult` JSON                              |
| `done`                         | `{}`                                                      |
| `error`                        | `{ error }`                                               |

Drive React Flow node states off the started/finished events. The pipeline
node ids match `agent_arena/flow_visualizer.py:PIPELINE_NODES`.

### GET /arena/runs?client_id=acme

Returns `{ runs: [{ run_id, client_id, timestamp_utc, project_summary, verdict_winner, verdict_confidence }] }`.

### GET /arena/runs/{run_id}

Full immutable snapshot — same shape as `data/runs/<run_id>.json`. Includes
`signature_sha256` for audit verification.

### POST /arena/upload (multipart)

Fields: `file`, `client_id`, `doc_type` (`project_case` | `company_context` | `decisions`), `title`.

Triggers a background reindex.

## Local dev

```bash
# Backend
python -m uvicorn api:app --reload --port 8080

# Frontend (when built)
cd frontend && npm install && npm run dev   # http://localhost:3000
```

Set `NEXT_PUBLIC_API_BASE=http://localhost:8080` in `frontend/.env.local`.

## Page layout (recommended)

- `/` — landing + project idea input + client selector
- `/run/[runId]` — live pipeline view (React Flow) + report + diagram
- `/runs` — history table per client
- `/kb` — upload + browse project_cases per client
- `/eval` — eval dashboard (hit rate, variance) from `data/evals/*.md`

## Why no code yet

Building Next.js properly is 2-3 weeks (auth, RBAC, white-label, PDF export,
production deployment). The MVP focuses on the backend being shaped so that
work can start without backend changes. The Chainlit UI in `app.py` covers
the demo use case until then.
