# Stage-clear layout (UI-18)

The full-screen debrief plate has separate areas for score conversion, sign-off, Continue, and the password footer. Achievement notices remain queued while the stage-clear screen is active. The Continue prompt was moved to the midpoint between sign-off and footer because its icon touched the sign-off border.

Live Chromium verification used portrait (720x1100), standard (1280x720), and ultrawide (1920x720) windows. The debrief kept its authored 918x512 viewport at all three sizes. In each, the score row ended at y=386.9, sign-off occupied y=425.4..456.2, Continue centered at y=467.7, password footer began at y=479.3, and the queued achievement card remained at age zero. The finished canvas was inspected visually. `node --check assets/game.js` and `git diff --check` passed.
