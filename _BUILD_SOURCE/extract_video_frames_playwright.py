"""Extract exact visual-reference frames from an MP4 with Playwright Chromium.

This avoids re-encoding the source video and is intended only for QA/reference work.
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


def parse_time(value: str) -> float:
    parts = [float(part) for part in value.split(":" )]
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    raise argparse.ArgumentTypeError(f"Invalid timestamp: {value}")


async def extract(video: Path, output: Path, times: list[float], browser_path: Path | None) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
            executable_path=str(browser_path) if browser_path else None,
            args=["--allow-file-access-from-files"],
        )
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        # Navigate to the file itself. Browsers reject a file:// media URL when it
        # is injected into an about:blank page, but their native media page can
        # safely decode and seek the same local recording.
        await page.goto(video.resolve().as_uri(), wait_until="commit", timeout=30_000)
        await page.wait_for_selector("video", timeout=30_000)
        await page.locator("video").evaluate("video => { video.id = 'source'; video.muted = true; }")
        try:
            await page.wait_for_function(
                "document.querySelector('#source').readyState >= 1",
                timeout=120_000,
            )
        except Exception:
            status = await page.locator("#source").evaluate(
                "video => ({ readyState: video.readyState, networkState: video.networkState, error: video.error && video.error.message })"
            )
            raise RuntimeError(f"Browser could not load video metadata: {status}")
        duration = await page.locator("#source").evaluate("video => video.duration")
        print(f"duration={duration:.3f}s")
        for seconds in times:
            if seconds < 0 or seconds > duration:
                raise ValueError(f"Timestamp {seconds:.3f}s is outside 0-{duration:.3f}s")
            await page.locator("#source").evaluate(
                """async (video, seconds) => {
                    await new Promise((resolve, reject) => {
                        const done = () => { cleanup(); resolve(); };
                        const fail = () => { cleanup(); reject(video.error || new Error('video seek failed')); };
                        const cleanup = () => {
                            video.removeEventListener('seeked', done);
                            video.removeEventListener('error', fail);
                        };
                        video.addEventListener('seeked', done, { once: true });
                        video.addEventListener('error', fail, { once: true });
                        video.currentTime = seconds;
                    });
                }""",
                seconds,
            )
            stamp = f"{int(seconds // 60):02d}m{seconds % 60:06.3f}s".replace(".", "_")
            target = output / f"frame_{stamp}.png"
            await page.locator("#source").screenshot(path=str(target))
            print(target)
        await browser.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--time", action="append", required=True, type=parse_time)
    parser.add_argument("--browser", type=Path)
    args = parser.parse_args()
    asyncio.run(extract(args.video, args.out, args.time, args.browser))


if __name__ == "__main__":
    main()
