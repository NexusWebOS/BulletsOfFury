"""Record the Stage-clear layout proof without disturbing other request rows."""
import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "docs/REQUEST_CHECKLIST_0914.json"
raw = path.read_bytes()
newline = b"\r\n" if b"\r\n" in raw else b"\n"
data = json.loads(raw.decode("utf-8"))
row, = [item for item in data["items"] if item["id"] == "UI-18"]
row["status"] = "complete"
row["evidence"] = "STAGECLEAR_SEPARATION_0920.md"
row["request"] = (
    "Stage-clear achievement notices stay queued while the debrief owns the screen, and "
    "Fury Point conversion, sign-off, password and Continue occupy separate bands at wide, "
    "square and portrait display sizes."
)
data["latestBatch"] = {
    "description": "Stage-clear Fury Point, sign-off, password, Continue and achievement-notice separation",
    "evidence": "STAGECLEAR_SEPARATION_0920.md",
}
path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8").replace(b"\n", newline))
print("Recorded UI-18 complete")
