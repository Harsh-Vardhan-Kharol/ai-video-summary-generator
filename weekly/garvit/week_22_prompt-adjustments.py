"""
Week 22 (02-01-2027 - 08-01-2027)
Task: Adjust prompts based on evaluation results

Why this matters:
The quality review showed that unsupported descriptive wording and ambiguous
person records are especially harmful to downstream graph ownership links.
The prompt must therefore ask for exact names and source-faithful wording.

What this script does:
Checks that prompt set 1.1 contains the grounded wording and exact-person rules.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.nlp import week5_final_prompt_templates as prompts


if __name__ == "__main__":
    assert prompts.PROMPT_SET_VERSION == "1.1"
    assert "Prefer source wording" in prompts.SUMMARY_SYSTEM_PROMPT
    assert "use only the exact explicitly named person" in prompts.EXTRACTION_SYSTEM_PROMPT
    print("PASS: prompt set 1.1 includes source-faithful and exact-person extraction rules.")
