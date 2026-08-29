# Agent Architecture Advisor

Asistente de arquitectura cloud basado en agentes que transforma una idea de proyecto en una propuesta técnica **trazable, comparativa y auditable** para Azure, AWS y GCP.

El proyecto no pretende sustituir la validación de un arquitecto o la documentación contractual del proveedor. Su objetivo es acelerar el análisis inicial con recomendaciones apoyadas en conocimiento recuperado, citas verificables y experiencia propia de cada organización.

## En qué se basa

El sistema combina cuatro principios:

1. **RAG con evidencia**. Las recomendaciones se construyen a partir de fragmentos recuperados de la base de conocimiento en Qdrant. Cada componente recomendado debe incluir citas `CTX-XXXX`, que se validan contra el contexto realmente entregado al agente.
2. **Debate multiagente**. Agentes especializados plantean una arquitectura equivalente para Azure, AWS y GCP. Un juez compara las alternativas y un agente final sintetiza la propuesta y sus trade-offs.
3. **Conocimiento verificable y actualizable**. El constructor de conocimiento obtiene documentación de fuentes oficiales de Microsoft, AWS y Google Cloud, la conserva como Markdown con URL y fecha de actualización, y después la indexa.
4. **Contexto empresarial separado**. El conocimiento público de cloud se distribuye con el producto; cada empresa puede añadir casos reales, decisiones, restricciones, principios y lecciones aprendidas sin mezclarlos con la base pública.

```text
Idea de negocio
      |
Planner + aclaraciones interactivas
      |
Retrieval semántico (Qdrant) + reranking opcional
      |
Azure Agent | AWS Agent | GCP Agent
      |             |              |
Validación y reescritura de citas (máximo configurable)
      |
Juez + especialistas (seguridad, FinOps, compliance y datos)
      |
Síntesis final + costes orientativos + diagrama + auditoría
```

## Capacidades

- Comparativa de arquitecturas Azure, AWS y GCP.
- Extracción de requisitos y preguntas de aclaración cuando falta información crítica.
- RAG grounded: propuestas con evidencia y verificación de citas.
- Reintentos acotados si hay referencias inválidas; no hay bucles infinitos.
- Estimaciones orientativas de coste para MVP y producción.
- Diagramas Mermaid y representación visual en la interfaz.
- Revisión por especialistas: seguridad, FinOps, cumplimiento y datos.
- Memoria por cliente y snapshots de auditoría reproducibles.
- Preguntas de seguimiento sobre una propuesta sin relanzar todo el flujo.
- API FastAPI con SSE, CORS, rate limiting y autenticación opcional con Supabase.
- Frontend Next.js y una interfaz Chainlit heredada para desarrollo local.

## Estructura

```text
agent_arena/          Orquestación, agentes, prompts, RAG, auditoría y validación
knowledge_base/       Conocimiento indexable
  cloud_services/     Público: documentación de servicios por proveedor
  patterns/           Público: patrones arquitectónicos curados
  decisions/          Público: ADRs y trade-offs generales
  cost_references/    Público: referencias de precios
  project_cases/      Privado por empresa: proyectos, decisiones y resultados
  company_context/    Privado por empresa: estrategia y restricciones internas
knowledge_builder/    Scraper/generador de documentación oficial
frontend/             Aplicación Next.js
api.py                API FastAPI
ingest_and_index.py   Ingesta y creación del índice Qdrant
build_knowledge_base.py Actualización del conocimiento cloud desde la web
```

## Requisitos

- Python 3.11+ recomendado.
- Docker Desktop, si se usará Qdrant como servidor.
- Node.js 18+ para el frontend.
- Una clave de OpenAI o la configuración de Azure AI Foundry.

Instala las dependencias del backend:

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows PowerShell
pip install -r requirements.txt
```

Configura las credenciales en `.env` (nunca lo subas a Git):

```env
OPENAI_API_KEY=tu_clave
# Opcional: FOUNDRY_PROJECT_ENDPOINT=...
# Opcional: FOUNDRY_MODEL=...
```

## Inicio rápido

### 1. Levantar la infraestructura

```bash
docker compose up -d qdrant
```

Si Qdrant no está disponible, el script de ingesta puede usar el modo embebido local. Para forzarlo:

```bash
set QDRANT_FORCE_LOCAL=true
```

### 2. Indexar la base de conocimiento

```bash
python ingest_and_index.py
```

El comando genera los artefactos procesados en `data/processed/` y recrea el índice vectorial. Para una previsualización sin escribir en Qdrant:

```bash
python ingest_and_index.py --dry-run
```

### 3. Ejecutar la API

```bash
python -m uvicorn api:app --reload --port 8080
```

La comprobación de estado queda disponible en `http://localhost:8080/healthz`.

### 4. Ejecutar el frontend

```bash
cd frontend
npm install
npm run dev
```

Abre `http://localhost:3000`.

Como alternativa para la UI de desarrollo basada en Chainlit:

```bash
python run_chainlit.py run app.py --port 8081
```

## Conocimiento cloud oficial

El catálogo de `knowledge_builder/catalog.py` define servicios y URLs oficiales. El constructor descarga, limpia y convierte las páginas en documentos Markdown con sus fuentes.

```bash
# Ver el catálogo disponible
python build_knowledge_base.py --list

# Actualizar todos los servicios y reindexar
python build_knowledge_base.py --index

# Actualizar solo un proveedor o servicio
python build_knowledge_base.py --provider azure --index
python build_knowledge_base.py --service azure_document_intelligence --index
```

Las respuestas generadas deben considerarse fundamentadas únicamente cuando sus afirmaciones pueden rastrearse a los contextos `CTX-XXXX` recuperados. Los documentos creados por el builder incluyen las URLs oficiales de origen; las páginas pueden cambiar con el tiempo, por lo que se recomienda refrescar la base periódicamente.

## Personalización por empresa

Para conservar la portabilidad del producto:

- Usa `knowledge_base/project_cases/_template.md` para incorporar proyectos entregados, decisiones, costes observados, problemas y lecciones aprendidas.
- Usa `knowledge_base/company_context/_template.md` para definir estrategia cloud, restricciones de cumplimiento, regiones, herramientas aprobadas y skills del equipo.
- El endpoint `POST /arena/upload` admite la carga de documentos de casos de proyecto y los reindexa.
- Después de incorporar archivos directamente, ejecuta `python ingest_and_index.py`.

No introduzcas secretos, datos personales, contratos completos o información sensible en la base de conocimiento sin aplicar antes los controles de seguridad y retención propios de la empresa.

## Configuración relevante

| Variable | Propósito |
| --- | --- |
| `OPENAI_API_KEY` | Clave para el proveedor OpenAI. |
| `FOUNDRY_PROJECT_ENDPOINT` | Activa Azure AI Foundry si está configurada. |
| `QDRANT_HOST` / `QDRANT_PORT` | Dirección del servidor Qdrant. |
| `QDRANT_FORCE_LOCAL` | Fuerza el uso de Qdrant embebido. |
| `AGENT_ARENA_MODEL` | Modelo por defecto para los agentes. |
| `AGENT_ARENA_REASONING_MODEL` | Modelo para las fases intensivas de razonamiento. |
| `AGENT_ARENA_GCP_ENABLED` | Activa o desactiva GCP. |
| `AGENT_ARENA_RERANKER_ENABLED` | Activa el reranking cross-encoder. |
| `AGENT_ARENA_MAX_REWRITE_RETRIES` | Límite de reescrituras de citas. |
| `SUPABASE_URL`, `SUPABASE_JWT_SECRET`, `SUPABASE_SERVICE_ROLE_KEY` | Activa autenticación y cuota por usuario. |
| `CORS_ORIGINS` | Orígenes permitidos por la API. |

Sin las tres variables de Supabase, la API se ejecuta en modo abierto, adecuado únicamente para desarrollo local.

## Calidad y pruebas

```bash
python -m pytest -q
```

Las pruebas cubren validación de citas, planner, esquemas, costes, diagramas, reranking, memoria, auditoría y especialistas.

## Limitaciones y uso responsable

- Los precios son estimaciones, no cotizaciones ni compromisos comerciales.
- La disponibilidad regional, cuotas, versiones preview y SLA deben confirmarse en la documentación oficial y en la suscripción concreta antes de implementar.
- La validación de citas garantiza que una referencia existe en el contexto recuperado; no sustituye una revisión humana de la pertinencia técnica.
- Los casos internos mejoran el asesoramiento, pero deben gobernarse según las políticas de datos de cada empresa.

## Licencia

Define la licencia antes de distribuir el proyecto fuera de tu organización.
