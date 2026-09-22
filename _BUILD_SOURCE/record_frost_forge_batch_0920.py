"""Record the verified Forge audit and Furious ice-beam pass in the request ledger."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "docs/REQUEST_CHECKLIST_0914.json"
raw = path.read_bytes()
newline = b"\r\n" if b"\r\n" in raw else b"\n"
data = json.loads(raw.decode("utf-8"))
items = {item["id"]: item for item in data["items"]}

items["ENG-23"]["status"] = "partial"
items["ENG-23"]["evidence"] = "FORGE_REWARD_AUDIT_0920.md"
items["ENG-23"]["request"] = (
    "Audit and repair the Forge/weapon upgrade loop. The Stage-1-to-2 boss reward, two "
    "combines, re-spec, loadout swap, death persistence and audible UI cues have a Chromium "
    "proof; later stages and campaign save/load still need natural-play review."
)
items["S2-09"]["status"] = "complete"
items["S2-09"]["evidence"] = "FROST_FURIOUS_BEAM_0920.md"
items["S2-09"]["request"] = (
    "Regenerated Furnace giant core-beam art and a dark-blue, pale-core variant for the "
    "Stage-3 Furious boss; both have native-browser visual proof."
)
items["S3-12"]["status"] = "partial"
items["S3-12"]["evidence"] = "FROST_FURIOUS_BEAM_0920.md"
items["S3-12"]["request"] = (
    "Furious Rime Wall: enlarged blue laser with matching Simon-Says warning is integrated; "
    "black/blue hull palette and full Hard-pattern parity remain."
)
data["latestBatch"] = {
    "description": "Stage-3 Furious Rime Wall/Frost Cruiser blue beams and Stage-1-to-2 Forge reward-flow audit",
    "evidence": "FROST_FURIOUS_BEAM_0920.md",
}
content = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
path.write_bytes(content.replace(b"\n", newline))
print("Recorded ENG-23 partial, S2-09 complete, S3-12 partial")
