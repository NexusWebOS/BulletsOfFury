"""Browser smoke test for the non-destructive sound-library review page."""

from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
URL = "http://127.0.0.1:8772/docs/sound-library-review/index.html"
SHOT = ROOT / "docs" / "sound-library-review" / "sound-library-review-page.png"


def main() -> None:
    errors: list[str] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
        page = browser.new_page(viewport={"width": 1500, "height": 1050}, device_scale_factor=1)
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(URL, wait_until="networkidle", timeout=60_000)
        assert page.title() == "Bullets of Fury — Sound Library Review"
        assert page.locator(".sound-card").count() == 55
        assert page.locator(".category-section").count() == 11
        assert page.locator(".safety-lock").inner_text().strip() == "Production audio untouched"
        assert page.locator(".wave-row img").evaluate_all(
            "imgs => imgs.length === 55 && imgs.every(img => img.complete && img.naturalWidth > 0)"
        )
        assert page.evaluate(
            """async () => {
              const urls = SOUND_REVIEW.entries.map(entry =>
                SOUND_REVIEW.audioBase + encodeURIComponent(entry.file));
              const responses = await Promise.all(urls.map(url => fetch(url, {method: 'HEAD'})));
              return responses.length === 55 && responses.every(response => response.ok);
            }"""
        )

        first = page.locator(".sound-card").first
        first.locator('[data-action="play"]').click()
        page.wait_for_timeout(650)
        assert page.locator("#player").evaluate("audio => audio.error === null && audio.currentTime > 0")
        first.locator('[data-value="primary"]').click()
        assert first.get_attribute("data-decision") == "primary"
        first.locator('[data-action="compare"]').click()
        assert page.locator("#compareDrawer").get_attribute("class").endswith("show")

        page.locator("#categoryFilter").select_option("Shotguns")
        assert page.locator(".sound-card").count() == 4
        page.locator("#categoryFilter").select_option("all")
        page.evaluate("localStorage.removeItem('bof-sound-review-v1')")
        page.reload(wait_until="networkidle")
        assert page.locator(".summary-card").nth(2).locator("strong").inner_text() == "0"
        page.screenshot(path=str(SHOT), full_page=False)
        browser.close()

    if errors:
        raise RuntimeError("Browser errors: " + " | ".join(errors))
    print("Sound review browser QA OK: 55 cards, 11 categories, audio playback, decisions, A/B, filtering")
    print(SHOT)


if __name__ == "__main__":
    main()
