# ColeForge online services

The game has a dedicated Supabase client in `assets/online.js`. `assets/online-config.js`
contains only the project URL and **publishable** key. Never ship a secret, database
password, or service-role key in a browser file. The schema is
`supabase/migrations/20260924000000_bof_online.sql`.

The Co-op mode opens an Online Operations panel. Local Co-op enters the existing two-seat
game unchanged. Host Online creates a private room code; Join Online accepts that code.
The host runs the game and chooses the pilots, and the remote wingman controls seat two.
Supabase Realtime carries private WebRTC signaling, with room membership checked by RLS.
WebRTC carries a live composite of the host's HUD and game screen plus remote input. The
guest has keyboard and gamepad controls. The host's game remains authoritative; enemy
simulation does not diverge between two browsers.

The leaderboard submits a score at game-over or victory and displays top scores by
difficulty. The wide side panel uses the live top four when available, falling back to
the existing local save scores offline. Announcements are read from published,
unexpired rows; only a dashboard/server administrator can write them. Anonymous Supabase
Auth provides stable browser-local identities without asking players for email.

Project setup after creation:

1. Enable Anonymous Sign-Ins in Supabase Auth.
2. Apply the SQL migration to the dedicated project. Its explicit grants are needed
   because new tables are not automatically exposed to Data API roles.
3. Disable public access to Realtime channels in Realtime Settings. This makes the
   private room authorization policies effective for every join.
4. Place the project URL and publishable key in `assets/online-config.js`.
5. Open the game over HTTP, host from one browser profile, and join with the code from
   a second profile. Verify that seat-two controls move only the host's second ship.

The peer connection currently has a STUN server but no TURN relay. Some NAT combinations
will fail to connect; the panel reports that failure. Guest video does not yet include
game audio. The score table checks ownership, ranges, and a 30-second submission
cooldown, but a browser-authoritative score cannot be cheat-proof without a server-side
gameplay verifier.

Supabase references: [JavaScript browser installation](https://supabase.com/docs/reference/javascript/installing),
[anonymous sign-ins](https://supabase.com/docs/guides/auth/auth-anonymous),
[Realtime authorization](https://supabase.com/docs/guides/realtime/authorization).
