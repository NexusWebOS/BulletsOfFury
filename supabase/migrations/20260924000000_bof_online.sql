-- Bullets of Fury online services. Apply to the dedicated ColeForgeProductions project.
-- Only the publishable browser key may be shipped with the game.
create extension if not exists pgcrypto;

create table if not exists public.bof_scores (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  pilot text not null check (pilot ~ '^[a-z]{2,24}$'),
  callsign text not null check (char_length(callsign) between 2 and 18),
  difficulty text not null check (difficulty in ('easy','normal','hard','furious','insanity')),
  mode text not null check (mode in ('arcade','campaign','coop','bossrush','timeattack')),
  stage smallint not null check (stage between 1 and 9),
  score bigint not null check (score between 0 and 1000000000),
  created_at timestamptz not null default now()
);
create index if not exists bof_scores_rank on public.bof_scores (difficulty, score desc, created_at asc);
create index if not exists bof_scores_user on public.bof_scores (user_id, created_at desc);
alter table public.bof_scores enable row level security;
create or replace function public.bof_score_cooldown()
returns trigger language plpgsql set search_path = public, pg_temp as $$
begin
  if exists (select 1 from public.bof_scores
             where user_id = new.user_id and created_at > now() - interval '30 seconds') then
    raise exception 'Wait before submitting another score';
  end if;
  return new;
end $$;
create trigger bof_score_cooldown before insert on public.bof_scores
  for each row execute function public.bof_score_cooldown();
create policy "read public ranks" on public.bof_scores for select to anon, authenticated using (true);
create policy "submit own rank" on public.bof_scores for insert to authenticated
  with check (user_id = (select auth.uid()));
grant select on public.bof_scores to anon, authenticated;
grant insert on public.bof_scores to authenticated;
grant usage on sequence public.bof_scores_id_seq to authenticated;

create table if not exists public.bof_announcements (
  id bigint generated always as identity primary key,
  title text not null check (char_length(title) between 1 and 100),
  body text not null check (char_length(body) between 1 and 1000),
  published_at timestamptz not null default now(),
  expires_at timestamptz,
  published boolean not null default false
);
alter table public.bof_announcements enable row level security;
create policy "read live announcements" on public.bof_announcements for select to anon, authenticated
  using (published and published_at <= now() and (expires_at is null or expires_at > now()));
grant select on public.bof_announcements to anon, authenticated;
-- Announcements are written only through the Supabase dashboard/server role.

create table if not exists public.bof_rooms (
  id uuid primary key default gen_random_uuid(),
  code text not null unique check (code ~ '^[A-F0-9]{12}$'),
  host_id uuid not null references auth.users(id) on delete cascade,
  status text not null default 'open' check (status in ('open','playing','closed')),
  created_at timestamptz not null default now(),
  expires_at timestamptz not null default (now() + interval '3 hours')
);
create table if not exists public.bof_room_members (
  room_id uuid not null references public.bof_rooms(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  seat smallint not null check (seat in (1,2)),
  joined_at timestamptz not null default now(),
  primary key (room_id, user_id),
  unique (room_id, seat)
);
create index if not exists bof_room_member_user on public.bof_room_members (user_id);
alter table public.bof_rooms enable row level security;
alter table public.bof_room_members enable row level security;
-- The browser uses only the room RPCs; direct room/member reads remain closed.

create or replace function public.bof_create_room()
returns table(room_id uuid, join_code text, topic text)
language plpgsql security definer set search_path = public, extensions, pg_temp as $$
declare r public.bof_rooms;
begin
  if auth.uid() is null then raise exception 'Sign in first'; end if;
  insert into public.bof_rooms(code, host_id)
    values (upper(encode(gen_random_bytes(6),'hex')), auth.uid()) returning * into r;
  insert into public.bof_room_members(room_id,user_id,seat) values(r.id,auth.uid(),1);
  return query select r.id,r.code,'bof-room-'||r.id::text;
end $$;
revoke all on function public.bof_create_room() from public;
grant execute on function public.bof_create_room() to authenticated;

create or replace function public.bof_join_room(p_code text)
returns table(room_id uuid, topic text)
language plpgsql security definer set search_path = public, extensions, pg_temp as $$
declare r public.bof_rooms;
begin
  if auth.uid() is null then raise exception 'Sign in first'; end if;
  select * into r from public.bof_rooms
    where code = upper(trim(p_code)) and status = 'open' and expires_at > now() for update;
  if not found then raise exception 'Room unavailable'; end if;
  if r.host_id = auth.uid() then raise exception 'Use a second account for the wingman'; end if;
  insert into public.bof_room_members(room_id,user_id,seat)
    values(r.id,auth.uid(),2) on conflict (room_id,user_id) do nothing;
  return query select r.id,'bof-room-'||r.id::text;
exception when unique_violation then
  raise exception 'Room already has two pilots';
end $$;
revoke all on function public.bof_join_room(text) from public;
grant execute on function public.bof_join_room(text) to authenticated;

create or replace function public.bof_close_room(p_room uuid)
returns void language plpgsql security definer set search_path = public, pg_temp as $$
begin
  update public.bof_rooms set status='closed' where id=p_room and host_id=auth.uid();
end $$;
revoke all on function public.bof_close_room(uuid) from public;
grant execute on function public.bof_close_room(uuid) to authenticated;

create or replace function public.bof_leave_room(p_room uuid)
returns void language plpgsql security definer set search_path = public, pg_temp as $$
begin
  delete from public.bof_room_members
    where room_id=p_room and user_id=auth.uid() and seat=2;
end $$;
revoke all on function public.bof_leave_room(uuid) from public;
grant execute on function public.bof_leave_room(uuid) to authenticated;

create or replace function public.bof_can_signal(p_topic text)
returns boolean language sql stable security definer set search_path = public, pg_temp as $$
  select exists (
    select 1 from public.bof_room_members m join public.bof_rooms r on r.id=m.room_id
    where m.user_id=auth.uid() and p_topic='bof-room-'||m.room_id::text
      and r.status <> 'closed' and r.expires_at > now()
  )
$$;
revoke all on function public.bof_can_signal(text) from public;
grant execute on function public.bof_can_signal(text) to authenticated;

create policy "room receives game signals" on realtime.messages for select to authenticated using (
  extension in ('broadcast','presence') and public.bof_can_signal((select realtime.topic()))
);
create policy "room sends game signals" on realtime.messages for insert to authenticated with check (
  extension in ('broadcast','presence') and public.bof_can_signal((select realtime.topic()))
);
