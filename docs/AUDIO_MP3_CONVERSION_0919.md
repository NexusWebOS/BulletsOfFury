# MP3 runtime audio conversion — 0919

Converted 172 tracked WAV files to VBR MP3 (libmp3lame quality 4). Source bytes: 83,957,112; MP3 bytes: 8,000,802; reduction: 90.5%. The original PCM files remain recoverable from Git history.

Updated the runtime manifest, game references, active audio tests, and staging copy script. Historical build generators remain unchanged and may still emit WAV masters; transcode their outputs before adding them to runtime assets. Historical prose notes remain unchanged. A Chromium loading probe decoded sampled effects and music without request or console errors; audible playback was not established by that headless probe.
