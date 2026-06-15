# DEMO — Agent Architecture Advisor MVP

Guion para enseñar el sistema a un compañero en vivo. **Tiempo total: ~25 min** (3 proyectos x ~7 min + intro).

---

## Preparación (antes de la demo)

```bash
docker compose up -d                 # Qdrant arriba
chainlit run app.py                  # http://localhost:8000
```

Ten a mano el **REPORT.md** abierto en otra pestaña para el score y el roadmap.

---

## 0. Intro (2 min)

Una frase: *"Esto es un asesor multi-agente de arquitectura cloud. Le das una idea de proyecto, agentes Azure/AWS/GCP debaten en paralelo basándose en una knowledge base local (Qdrant + reranker), un juez compara y un agente final sintetiza la arquitectura recomendada con citas, costes y diagrama. Todo grounded — si no está en la KB, no lo propone."*

Enseña la pantalla de bienvenida con las 4 ideas sugeridas.

---

## 1. Proyecto A — RAG normativa interna de un banco (regulado)

**Pega esto literal:**

> Quiero un asistente RAG sobre la normativa interna de un banco español. Los empleados de cumplimiento harán preguntas en lenguaje natural y deben obtener respuestas con citas exactas al documento y página. Debe cumplir requisitos de auditoría (registro inmutable de cada consulta), datos en residencia europea, y soportar ~500 usuarios concurrentes.

**Qué señalar mientras corre:**

- El **flujo en vivo** — los nodos se van iluminando. "Aquí ves que el retrieval ya terminó, Azure y AWS están corriendo en paralelo".
- Al acabar: el **cloud recomendado** en la cabecera (probable Azure por residencia EU + Azure OpenAI + AI Search).
- El **diagrama coloreado** — todo azul Azure agrupado por capas.
- Las **citas [CTX-XXXX]** en la propuesta detallada.

**Pregunta de follow-up para demostrar Q&A:**
> "¿Cómo encaja la auditoría inmutable? ¿Qué servicio usaría?"

---

## 2. Proyecto B — Detección de fraude en tiempo real

**Pega esto literal:**

> Necesito un pipeline de detección de fraude en tiempo real sobre transacciones de tarjeta. Latencia objetivo p99 <200ms, ~10k TPS pico, modelo de scoring servido como API, almacenamiento de features online + offline, y dashboard de alertas para el equipo antifraude. Sin preferencia de cloud todavía.

**Qué señalar:**

- Aquí los **3 clouds compiten en serio** (AWS Kinesis + SageMaker, Azure Event Hubs + ML, GCP Pub/Sub + Vertex). El juez tiene trabajo de verdad.
- En la **comparativa** vas a ver trade-offs explícitos (coste vs madurez del feature store).
- Los **costes estimados** comparados lado a lado (MVP low/high y producción low/high).

**Pregunta de follow-up:**
> "Si quisiera reentrenar el modelo cada noche con datos del día, ¿cómo cambia la arquitectura?"

---

## 3. Proyecto C — Copiloto PMO sobre Jira + SharePoint

**Pega esto literal:**

> Un copiloto interno para el PMO que pueda responder "¿qué proyectos están en riesgo?" leyendo Jira, SharePoint y emails de Outlook, generar resúmenes ejecutivos semanales y mandarlos por Teams. Empresa Microsoft 365.

**Qué señalar:**

- Aquí el **business context** sesga claramente a Azure (M365 nativo, Graph API, Logic Apps, Azure OpenAI).
- El **diagrama** muestra la integración nativa con productos Microsoft.
- La **trazabilidad de evidencia** referencia `project_cases/pmo_project_status_assistant.md` — está usando el caso real del KB.

**Pregunta de follow-up:**
> "¿Y si la empresa nos pide GDPR estricto y no quieren que ningún dato salga de su tenant?"

---

## 4. Cierre — qué falta para producto (3 min)

Abre `REPORT.md` y enseña la sección 4 (Brechas restantes). Los 3 puntos a destacar:

1. **On-prem provider** — vía clave para diferenciarse.
2. **Auditoría inmutable** — desbloquea BFSI/health/pharma.
3. **Multi-tenancy + UI self-service del KB** — convierte la herramienta en producto vendible a consultoras.

---

## Troubleshooting durante la demo

- **El flow no actualiza** → mira la consola del Chainlit; verifica que el LLM tiene API key (`OPENAI_API_KEY` o vars de Foundry).
- **GCP no aparece** → revisa `GCP_ENABLED` en `agent_arena/config.py` y que haya documentos GCP indexados (`build_knowledge_base.py --provider gcp --index`).
- **Citas inválidas / muchas reescrituras** → es esperado en ideas muy fuera del KB (e.g. juegos, IoT industrial). Quédate en los 3 proyectos de arriba.
