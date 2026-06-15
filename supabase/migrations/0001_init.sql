-- ============================================================================
-- Agent Architecture Advisor — initial auth/quota schema
-- Run this in the Supabase SQL editor (or `supabase db push`).
-- ============================================================================

-- 1. Profiles: one row per auth user, holds role + run quota.
create table if not exists public.profiles (
  id          uuid primary key references auth.users(id) on delete cascade,
  email       text,
  role        text not null default 'user' check (role in ('user', 'admin')),
  run_limit   integer not null default 1,   -- free tier: 1 run
  runs_used   integer not null default 0,
  created_at  timestamptz not null default now()
);

-- 2. Row Level Security: a user can read ONLY their own profile.
--    Writes are done by the backend with the service-role key (bypasses RLS).
alter table public.profiles enable row level security;

drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_own"
  on public.profiles for select
  using (auth.uid() = id);

-- 3. Auto-create a profile when a new auth user signs up.
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, email, role, run_limit, runs_used)
  values (new.id, new.email, 'user', 1, 0)
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- 4. Atomic quota increment, called by the backend after a successful run.
create or replace function public.increment_runs_used(p_user_id uuid)
returns void
language sql
security definer set search_path = public
as $$
  update public.profiles
     set runs_used = runs_used + 1
   where id = p_user_id;
$$;

-- ============================================================================
-- AFTER RUNNING: make yourself admin (unlimited runs). Replace the email.
--   update public.profiles set role = 'admin'
--    where id = (select id from auth.users where email = 'pf.pablofraga@gmail.com');
--
-- To grant a specific user extra runs manually (e.g. after talking to them):
--   update public.profiles set run_limit = 50
--    where id = (select id from auth.users where email = 'cliente@empresa.com');
-- ============================================================================
