# Despliegue en producción

Arquitectura de despliegue:

```
  Navegador
     │  (login Supabase, JWT)
     ▼
  Frontend Next.js  ── Vercel
     │  fetch + Bearer <jwt>
     ▼
  API FastAPI       ── Railway (Docker)
     ├── Qdrant server   ── Railway (servicio aparte)
     └── Supabase        ── Postgres + Auth (gestionado)
```

El backend deriva el `client_id` del JWT, así que ningún usuario puede leer los
runs de otro. Sin las variables de Supabase, la API arranca en **modo abierto**
(sin auth) — útil sólo para desarrollo local.

---

## 1. Supabase (auth + cuotas)

1. Crea un proyecto en https://supabase.com.
2. **SQL Editor** → pega y ejecuta `supabase/migrations/0001_init.sql`.
3. **Authentication → Providers**: activa *Email* (magic link) y, si quieres,
   *Google* (necesita OAuth client ID/secret).
4. **Authentication → URL Configuration**: añade a *Redirect URLs*:
   - `http://localhost:3000/auth/callback`
   - `https://TU-APP.vercel.app/auth/callback`
5. Apúntate de **Project Settings → API**:
   - `Project URL`  → `SUPABASE_URL` y `NEXT_PUBLIC_SUPABASE_URL`
   - `anon public`  → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `service_role` → `SUPABASE_SERVICE_ROLE_KEY` (¡secreto! sólo backend)
   - `JWT Secret`   → `SUPABASE_JWT_SECRET`
6. Date de alta una vez en la app (login), luego en SQL Editor hazte admin:
   ```sql
   update public.profiles set role = 'admin'
    where id = (select id from auth.users where email = 'pf.pablofraga@gmail.com');
   ```

**Conceder acceso a un cliente** (tras hablarlo en persona):
```sql
update public.profiles set run_limit = 50
 where id = (select id from auth.users where email = 'cliente@empresa.com');
```

---

## 2. Backend + Qdrant en Railway

1. Crea un proyecto en https://railway.app y conéctalo a este repo.
2. Añade un servicio **Qdrant**: *New → Docker Image → `qdrant/qdrant`*, con un
   volumen montado en `/qdrant/storage`. Anota su host interno (p.ej. `qdrant.railway.internal`).
3. Añade el servicio **API**: usa este repo (detecta el `Dockerfile` / `railway.json`).
4. Variables del servicio API:
   ```
   OPENAI_API_KEY=...
   QDRANT_HOST=qdrant.railway.internal
   QDRANT_PORT=6333
   SUPABASE_URL=...
   SUPABASE_JWT_SECRET=...
   SUPABASE_SERVICE_ROLE_KEY=...
   CORS_ORIGINS=https://TU-APP.vercel.app
   ```
5. Tras el primer deploy, **indexa la KB** contra el Qdrant remoto una vez:
   ```bash
   railway run python ingest_and_index.py     # con QDRANT_HOST apuntando al server
   ```
   (o ejecútalo desde el contenedor con `railway shell`).

---

## 3. Frontend en Vercel

1. *Import Project* → carpeta `frontend`.
2. Variables de entorno:
   ```
   NEXT_PUBLIC_API_BASE=https://TU-API.up.railway.app
   NEXT_PUBLIC_SUPABASE_URL=https://TU-PROYECTO.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=...
   ```
3. Deploy. Verifica que `CORS_ORIGINS` del backend incluye el dominio de Vercel.

---

## 4. Local prod-like (Docker)

```bash
cp .env.example .env          # rellena OPENAI_API_KEY (deja Supabase vacío = modo abierto)
docker compose up --build
docker compose exec api python ingest_and_index.py   # indexa la KB una vez
```

---

## Checklist de seguridad antes de abrir al público
- [ ] `CORS_ORIGINS` cerrado al dominio real (no `*`).
- [ ] Las 3 variables de Supabase puestas en el backend (auth activa: `/healthz` → `auth_enabled: true`).
- [ ] Tu usuario es `role = 'admin'`; el resto arranca con `run_limit = 1`.
- [ ] `service_role` key NUNCA en el frontend ni en el repo.
- [ ] Qdrant no expuesto públicamente (sólo red interna de Railway).
