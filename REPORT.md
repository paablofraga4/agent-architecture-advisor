# Agent Architecture Advisor — Informe de evaluación y mejoras MVP

**Fecha:** 2026-06-15
**Autor:** Pablo Fraga + Claude (análisis + implementación)
**Repo base:** `paablofraga4/agent-architecture-advisor`
**Repo MVP:** `paablofraga4/agent-architecture-advisor-mvp`

---

## 1. Resumen ejecutivo

El proyecto es un MVP **sólido y bien estructurado** de un asesor de arquitectura cloud multi-agente. El pipeline (planner → retrieval grounded → debate Azure/AWS/GCP → juez → arquitectura final + costes + diagrama) está bien separado, tipado con Pydantic y con verificación real de citas contra una knowledge base local en Qdrant.

> **Score global: 74 / 100**

Las mejoras de este MVP añaden lo que faltaba para una demo convincente a un compañero o cliente:

- Visualización del flujo del pipeline como **nodos Mermaid en vivo** (pending → running → done) en un único mensaje que se va actualizando.
- **Informe final** con cabecera ejecutiva (cloud ganador, métricas, restricciones, citas, reescrituras).
- **Diagrama de arquitectura por capas y coloreado por proveedor** (Azure azul, AWS naranja, GCP azul Google, neutral gris).
- 3 ideas de proyecto preparadas en `DEMO.md` para enseñar en vivo.

---

## 2. Score detallado

| Eje | Score | Comentario |
|---|---|---|
| Código / arquitectura | 18/25 | Buena separación de módulos, schemas Pydantic, async, validators. Falta test e2e con LLM mockeado. |
| Grounding y KB | 16/20 | KB exportable, scraper con manifest, separación pública/privada por empresa. Falta versionado y re-scrape periódico. |
| Funcionalidades vs intención | 15/20 | Debate AWS/Azure/GCP + juez + follow-up cubren la intención principal. **On-prem no implementado**. Un único agente por cloud → no hay perspectivas (seguridad/FinOps/compliance). |
| Lógica producto | 14/20 | `business_context` y `project_cases` son la base correcta para multi-tenant. Falta UI admin del KB, multi-tenancy real, RBAC, snapshot auditable. |
| Escalabilidad | 11/15 | Qdrant + async escalan. Chainlit es para demo, no para SaaS. KB en parquet local sin pipelines incrementales. |
| **TOTAL** | **74/100** | MVP demo-ready con piezas vendibles y caminos claros a producto. |

---

## 3. Mejoras implementadas en este MVP

### 3.1 Flow visualizer en vivo (`agent_arena/flow_visualizer.py`)

Un único `FlowState` que mapea cada evento del arena (`planner_started`, `retrieval_finished`, etc.) a transiciones de estado por nodo. Renderiza un `flowchart LR` Mermaid con `classDef` por estado, y se inyecta en un solo `cl.Message` de Chainlit que se va actualizando — el usuario ve la información **fluir** de un nodo al siguiente en tiempo real, no una lista de pasos.

Cubierto con 4 tests unitarios (`tests/test_flow_visualizer.py`, todos pasan).

### 3.2 Reporte ejecutivo (`agent_arena/report_renderer.py`)

`render_report_header(result)` produce una cabecera con:

- Proyecto + tipo + cloud recomendado (heurística sobre `final_comparison`).
- Tabla de métricas: capacidades, restricciones, contextos recuperados por proveedor, citas totales, reescrituras.

`render_architecture_section(result)` aísla el diagrama Mermaid en su propia sección.

### 3.3 Diagrama de arquitectura mejorado (`agent_arena/diagram.py`)

Nuevas reglas en el prompt del agente de diagramas:

- **Formas por tipo de componente** (DB cilindros, storage barras, colas estadium, LLMs/agents diamantes, usuarios círculos).
- **Subgraph por capa** (Ingestion, Processing, AI/Agents, Storage, Serving, Observability).
- **`classDef` obligatorio por proveedor** con colores oficiales (Azure #0078D4, AWS #FF9900, GCP #4285F4, neutral gris). Cada nodo se asigna a una clase → diagrama legible como ilustración.

### 3.4 Reescritura completa de `app.py`

- Bienvenida con 4 ideas de demo sugeridas.
- Single live message para el flow (sustituye los 10+ `cl.Step` separados de antes).
- Pasos de detalle (`cl.Step`) solo para los hitos con output relevante (planner JSON, propuestas Azure/AWS/GCP, comparativa del juez) — colapsables.
- Reporte final dividido en cabecera + arquitectura + propuesta detallada + costes + trazabilidad de evidencia + reescrituras.

---

## 4. Brechas restantes (roadmap para llevar a producto)

Ordenadas por impacto sobre la visión "herramienta para consultoras":

1. **On-prem provider** — falta agente y KB para Kubernetes/OpenShift + vLLM/Ollama. Es lo que más diferencia frente a competencia.
2. **Multi-tenancy real** — colecciones Qdrant por cliente, aislamiento de `project_cases`, claves por org.
3. **Auditoría inmutable** — snapshot por run (prompts hash + KB version hash + modelo + outputs + citas firmadas). Sin esto no hay "100% fiable" para sectores regulados.
4. **Agentes especialistas** además del per-cloud: Security, FinOps, Compliance, Data. Convierte el "debate" simulado en debate real.
5. **UI self-service** para que la consultora suba `project_cases`, decisiones y preferencias sin tocar markdown.
6. **Evaluación continua** — golden dataset "idea → arquitectura esperada" con métricas de cobertura de citas, alucinación, coherencia inter-agente.
7. **Frontend producto** (FastAPI + Next.js) cuando se salga de demo. Chainlit limita branding, RBAC y embedding en SaaS.
8. **Versionado de KB y prompts** para reproducibilidad — sin esto no hay re-ejecución exacta de un run pasado.

---

## 5. Cómo correr el MVP

PowerShell (Windows):

```powershell
docker compose up -d
python build_knowledge_base.py --index   # solo la primera vez
chainlit run app.py
```

bash / zsh:

```bash
docker compose up -d && python build_knowledge_base.py --index && chainlit run app.py
```

Ver `DEMO.md` para el guion de la demo en vivo con 3 ideas preparadas.
