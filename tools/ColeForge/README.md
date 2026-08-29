# ColeForge

A local 16-bit video smithy. Paste a link, pick your metal, strike the anvil.
It's a pixel-art front end for [yt-dlp](https://github.com/yt-dlp/yt-dlp) that runs
entirely on your own machine — nothing is uploaded anywhere, and there is no account.

## Running it

Double-click **`START-COLEFORGE.bat`**. It checks Node and yt-dlp, starts the
server, and opens the forge at <http://127.0.0.1:8420>.

Or from a terminal:

```bash
node server.js
```

To use a different port: `set COLEFORGE_PORT=8421 && node server.js`

## What you need

| Tool | Why | Status on this machine |
|---|---|---|
| Node.js | runs the local server | installed |
| yt-dlp | does the actual fetching | installed via `pip` |
| ffmpeg | merges video+audio, makes MP3 | installed |

Keep yt-dlp current — YouTube changes often and a stale copy is the usual cause of
a failed forge:

```bash
python -m pip install -U yt-dlp
```

## Using it

1. **Paste a link.** It scries automatically on paste (or press Enter / hit SCRY)
   and shows the title, channel, duration, and the best resolution available.
2. **Choose your metal.** Resolutions the video doesn't actually have are greyed out.
   MP3 / M4A / WAV pull audio only.
3. **Strike the anvil.** The hammer swings in time with your download speed, the
   ingot glows from cold iron to white-hot as it progresses, and sparks fly on
   every strike.

Finished files land in `downloads/` and appear in **THE VAULT** at the bottom,
where SHOW opens the file in Explorer and SAVE pulls it through the browser.

**Playlists:** tick `WHOLE PLAYLIST` before scrying. You get a checklist of every
video and can untick the ones you don't want; each becomes its own queue entry
with its own progress bar.

**Subtitles:** tick `BURN IN SUBTITLES` to fetch English subs (including
auto-generated) and embed them in the file.

Two downloads run at a time. Change `concurrency` in `coleforge.config.json`
along with `outputDir` if you want them somewhere other than `downloads/`.

## How it's put together

```
server.js            zero-dependency Node HTTP server; spawns and parses yt-dlp
coleforge.config.json  output folder + concurrency
public/index.html    markup
public/style.css     the 16-bit skin (hard bevels, no rounded corners anywhere)
public/forge.js      the animated smithy — sprites are ASCII art compiled to rects
public/app.js        probing, the queue, SSE progress, chiptune audio
downloads/           the vault
```

The server binds to `127.0.0.1` only, so nothing on your network can reach it.
Progress comes back through yt-dlp's `--progress-template` and is streamed to the
page over Server-Sent Events. Cancelling kills the whole process tree, so a
half-finished ffmpeg merge doesn't keep running in the background.

There are no npm dependencies — `node server.js` is the whole install.

## If a forge fails

Every job keeps its full yt-dlp log; the red line under the queue entry is the
actual error. Two common ones:

- **`ffmpeg not found`** — ColeForge resolves ffmpeg's absolute path from `PATH`
  at startup. The banner it prints on launch shows exactly which binary it found;
  if that line says `missing`, ffmpeg isn't on `PATH`.
- **`No supported JavaScript runtime could be found`** — a warning, not a failure.
  yt-dlp now prefers a JS runtime for YouTube extraction and some formats may be
  missing without one. Everything still works today; if a video starts refusing
  to yield its higher resolutions, installing Deno (`winget install DenoLand.Deno`)
  clears it.

## A note on what you forge

This is a tool, and what it fetches is up to you. Stick to material you have the
right to keep: your own uploads, Creative Commons and public-domain works, or
anything the rights holder allows. Downloading other people's copyrighted video
generally breaches YouTube's terms and may infringe copyright where you live.
