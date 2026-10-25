"""
Week 26 (30-01-2027 - 05-02-2027)
Task: Test how it looks and reads in the actual UI

Why this matters:
NLP output should remain concise and interpretable when rendered, especially
for uncertain actions. Until Dev connects a live summary endpoint, the display
contract provides the testable part of this requirement.

What this script does:
Checks that the display payload includes short action text, explicit uncertainty,
and evidence metadata required by the UI.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp.combined_pipeline import MeetingNlpPipeline
from ml.nlp.display_contract import validate_display_payload


if __name__ == "__main__":
    case = json.loads((ROOT / "ml/nlp/fixtures/week_03_sample_transcripts.json").read_text(encoding="utf-8"))["cases"][0]
    replies = iter((case["reference_summary"], case["reference_extraction"]))
    output = MeetingNlpPipeline(lambda _messages: next(replies)).process(session_id="ui-fixture", segments=case["transcript_segments"])
    assert not validate_display_payload(output)
    for action in output["display"]["action_items"]:
        assert action["text"] and action["owner_status"] in {"assigned", "unassigned", "uncertain"} and action["evidence"]
    print("PASS: UI-facing action items expose readable text, uncertainty, and evidence.")
