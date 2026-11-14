-- Ninja Golf 3D peer-to-peer lobby. Realtime only: no tables, nothing stored.
-- Scoped to ng3d: topics, so Bullets of Fury's room policies are unaffected.
create policy "ng3d receives lobby signals" on realtime.messages for select to authenticated using (
  extension in ('broadcast','presence') and (select realtime.topic()) like 'ng3d:%'
);
create policy "ng3d sends lobby signals" on realtime.messages for insert to authenticated with check (
  extension in ('broadcast','presence') and (select realtime.topic()) like 'ng3d:%'
);
