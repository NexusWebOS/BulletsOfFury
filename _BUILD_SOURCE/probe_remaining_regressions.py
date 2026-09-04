#!/usr/bin/env python3
"""Live browser audit for the remaining reported transition, control, and boss regressions."""

from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "proofs" / "remaining_regressions_live"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    report: dict[str, object] = {}
    page_errors: list[str] = []
    console_errors: list[str] = []

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
            page = browser.new_page(viewport={"width": 980, "height": 1024}, device_scale_factor=1)
            page.on("pageerror", lambda err: page_errors.append(str(err)))
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

            cases = [
                ("map_left", "_BUILD_SOURCE/qa_campaign_map_controls_0826.html?dir=left", "__qaMapControls", 1500),
                ("map_right", "_BUILD_SOURCE/qa_campaign_map_controls_0826.html?dir=right", "__qaMapControls", 1500),
                ("stage6_transition", "_BUILD_SOURCE/qa_stage6_transition_0826.html", "__qaStage6", 1400),
                ("stage5_missile", "_BUILD_SOURCE/qa_stage5_chaos_missile_0826.html", "__qaStage5Missile", 3300),
                ("stage4_mg", "_BUILD_SOURCE/qa_stage4_boss_0826.html?phase=mg", "__qaStage4", 1600),
                ("stage4_energy", "_BUILD_SOURCE/qa_stage4_boss_0826.html?phase=energy", "__qaStage4", 1600),
                ("stage4_homing", "_BUILD_SOURCE/qa_stage4_boss_0826.html?phase=homing", "__qaStage4", 1600),
                ("launch", "_BUILD_SOURCE/qa_regression_batch_0826.html?phase=launch", "__qaRegression", 1800),
                ("boss2", "_BUILD_SOURCE/qa_regression_batch_0826.html?phase=boss2", "__qaRegression", 2000),
                ("dialogue", "_BUILD_SOURCE/qa_regression_batch_0826.html?phase=dialogue", "__qaRegression", 1800),
            ]
            for name, url, state_name, delay in cases:
                page.goto(f"{base}/{url}", wait_until="load", timeout=60_000)
                page.wait_for_function(
                    f"() => typeof window.{state_name} !== 'undefined' && (window.__bofFrames|0)>4",
                    timeout=60_000,
                )
                page.wait_for_timeout(delay)
                state = page.evaluate(f"() => window.{state_name}")
                report[name] = state
                page.locator("#screen").screenshot(path=str(OUT / f"{name}.png"))

            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    # The page keeps a rolling sample across consecutive missiles. Split it whenever a new launch
    # lane appears; comparing the last sample of missile A with the first of missile B would report
    # a fake sideways jump and negative acceleration.
    missile = report["stage5_missile"]
    runs: list[list[dict]] = []
    for sample in missile["samples"]:
        if not runs or abs(sample["x"] - runs[-1][-1]["x"]) > 1.5:
            runs.append([])
        runs[-1].append(sample)
    missile["straightRuns"] = [
        {
            "count": len(run),
            "xRange": max(row["x"] for row in run) - min(row["x"] for row in run),
            "speedGain": run[-1]["speed"] - run[0]["speed"],
        }
        for run in runs
    ]

    report["pageErrors"] = page_errors
    report["consoleErrors"] = console_errors
    (OUT / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

    assert not page_errors and not console_errors
    assert report["map_left"]["correct"] and report["map_right"]["correct"]
    assert report["stage6_transition"]["advanced"] > 8
    assert not report["stage6_transition"]["starOverlayDrawn"]
    assert report["stage5_missile"]["count"] > 0
    assert any(run["count"] >= 4 and run["xRange"] < 1.5 and run["speedGain"] > 0.1
               for run in report["stage5_missile"]["straightRuns"])
    assert report["dialogue"]["bmfDialogue"] and report["dialogue"]["portrait"]


if __name__ == "__main__":
    main()
