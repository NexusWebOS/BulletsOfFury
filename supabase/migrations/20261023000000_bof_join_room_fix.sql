-- bof_join_room returns table(room_id, topic), so inside its body `room_id` is also a
-- PL/pgSQL OUT variable. `on conflict (room_id,user_id)` was therefore ambiguous (42702)
-- and every wingman join failed. Name the primary-key constraint instead.
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
    values(r.id,auth.uid(),2) on conflict on constraint bof_room_members_pkey do nothing;
  return query select r.id,'bof-room-'||r.id::text;
exception when unique_violation then
  raise exception 'Room already has two pilots';
end $$;
revoke all on function public.bof_join_room(text) from public;
grant execute on function public.bof_join_room(text) to authenticated;
