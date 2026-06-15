# Frontend (Next.js 14 + React Flow)

Frontend operativo para el backend `api.py`. Páginas implementadas:

- `/` — formulario de proyecto + selector de cliente + ejemplos
- `/run?idea=...&client_id=...` — **live pipeline** con React Flow (12 nodos), veredicto, diagrama D2 renderizado vía kroki, propuesta detallada con react-markdown, hallazgos de especialistas por colores de severidad
- `/runs` — historial filtrado por cliente con run_id, winner, confidence
- `/kb` — upload de markdown/txt/pdf como project_case, company_context o decisions

## Quickstart

```bash
# 1. Backend
cd ..
python -m uvicorn api:app --reload --port 8080

# 2. Frontend
cd frontend
cp .env.example .env.local      # NEXT_PUBLIC_API_BASE=http://localhost:8080
npm install
npm run dev                     # http://localhost:3000
```

## Stack

- **Next.js 14 App Router + TypeScript**
- **React Flow** para el grafo del pipeline (animated edges cuando el flujo pasa)
- **react-markdown + rehype-raw + remark-gfm** para el informe
- **Tailwind CSS** (modo oscuro por defecto, paleta panel/border/accent/ok/warn/err)
- SSE consumida vía `fetch` + `ReadableStream` (no `EventSource` porque necesitamos POST con body)

## Arquitectura

```
app/
  layout.tsx          # nav global
  globals.css         # tailwind + estilos report-md
  page.tsx            # home (form)
  run/page.tsx        # live pipeline + report
  runs/page.tsx       # history table
  kb/page.tsx         # upload form
components/
  PipelineGraph.tsx   # React Flow + EVENT_MAP
  Report.tsx          # markdown renderer
  ArchitectureImage.tsx  # POST D2 → kroki → SVG
lib/
  api.ts              # listRuns, getRun, uploadDoc
  sse.ts              # streamArenaRun (POST SSE parser)
```

## Contrato API

### POST /arena/run (SSE)

Body: `{ "idea": "...", "client_id": "acme", "model"?: "gpt-4o-mini" }`

Eventos consumidos por la UI (ver `components/PipelineGraph.tsx:EVENT_MAP`):

| Evento                          | Acción UI                          |
|--------------------------------|-------------------------------------|
| `*_started` / `*_finished`     | Cambia color del nodo en React Flow |
| `verdict_finished`             | (queda en el snapshot result)       |
| `final_architecture_finished`  | Renderiza markdown del informe      |
| `diagram_generation_finished`  | POST a kroki → muestra SVG          |
| `audit_saved`                  | Marca nodo "audit" como done        |
| `result`                       | Snapshot completo: veredicto + findings |
| `error` / `done`               | Cierra stream                       |

### REST

- `GET  /arena/runs?client_id=acme` → `{ runs: RunSummary[] }`
- `GET  /arena/runs/{run_id}` → snapshot completo (firmado)
- `POST /arena/upload` (multipart: `file`, `client_id`, `doc_type`, `title?`)

## Lo que **NO** está hecho aún (para iteraciones siguientes)

- Auth / RBAC / multi-tenant aislado
- White-label / branding por consultora
- Export PDF/PPTX del informe
- Streaming de tokens del LLM (los eventos son por hito, no por token)
- Eval dashboard (lee `data/evals/*.md` que produce `eval.py`)
- Diff entre runs del mismo cliente

Esto es el MVP visual del frontend: arranca, llama a la API, muestra el flujo en vivo y el informe completo. Suficiente para demo a un compañero o cliente potencial.
