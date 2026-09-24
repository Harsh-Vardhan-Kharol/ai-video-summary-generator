# Week 01 (10-08-2026 - 16-08-2026)
Task: Research summarization approaches: extractive vs abstractive

Why this matters:
Summaries and extracted decisions/actions are the bridge between noisy conversation transcripts and searchable session memory. Choosing an approach affects readability, factual risk, latency, and whether each statement can be traced back to what a speaker actually said.

What this deliverable does:
Compares extractive and abstractive summarization for multi-speaker meetings and recommends a grounded hybrid approach that preserves transcript evidence for later storage and cited RAG answers.

## Comparison

| Property | Extractive | Abstractive |
|---|---|---|
| Method | Selects source transcript sentences or spans and reuses their wording | Generates new wording that can combine or paraphrase information from multiple turns |
| Readability | Can retain disfluencies, repetition, and context-dependent fragments | Can produce a concise narrative and merge repeated statements |
| Faithfulness | Source wording is directly available, though selection can omit qualifiers or context | Can misstate details or invent connections; requires explicit evidence checks |
| Coverage | Often favors salient individual turns and may miss a decision spread across turns | Can consolidate a decision, rationale, and follow-up across turns |
| Citations | Straightforward: selected sentences map to transcript spans | Must retain the source turn/span IDs used to generate each claim |
| Incremental updates | Simple to recompute from recent turns, but can become a list of disconnected quotes | Supports rolling narrative summaries, but prior summary context can bias later updates |
| Best fit here | Evidence snippets, verbatim quotes, and a safe fallback | Human-readable overview, decisions, and action-item wording |

Meeting dialogue is repetitive, informal, and multi-speaker; research on meeting summarization treats abstractive generation as useful for consolidating this kind of distributed information while emphasizing task-specific challenges and evaluation. An empirical comparison also reports that model outputs labeled abstractive can remain partly extractive, so the distinction is not a guarantee of safer or more original output. [Rennard et al., *Abstractive Meeting Summarization: A Survey*](https://aclanthology.org/2023.tacl-1.49/), [Kumar & Gangadharaiah, *Are Abstractive Summarization Models truly ‘Abstractive’?*](https://aclanthology.org/2022.gem-1.17/)

## Recommendation

Use a hybrid pipeline:

1. Preserve the timestamped speaker turns from Dhruv as the source of truth.
2. Select or index relevant evidence spans for each candidate summary claim.
3. Generate a concise abstractive overview and normalized decision/action-item text from those spans.
4. Attach `source_segment_ids` to every generated claim and action item. Keep exact quote snippets available for verification.
5. Mark uncertain owner, date, or commitment fields as unknown instead of inferring them. Store confidence separately from the claim text.
6. Use extractive evidence as a fallback if generation is unavailable or a claim cannot be supported.

This lets the UI show readable summaries while Harsh’s later RAG pipeline retrieves evidence and provides citations. The source segments remain independently useful if the summarizer is replaced.

## Suggested output shape for later contract work

```json
{
  "summary": {
    "text": "The team will review the capture prototype next week.",
    "source_segment_ids": ["seg-014", "seg-019"],
    "confidence": 0.86
  },
  "action_items": [
    {
      "text": "Review the capture prototype",
      "owner": null,
      "due_date": null,
      "source_segment_ids": ["seg-019"],
      "confidence": 0.78
    }
  ]
}
```

The shape is an initial proposal for Week 2 prompt and contract work; it is not a frozen schema. Confidence is an internal signal for review prioritization, not a calibrated probability until evaluated against labeled examples.

## Evaluation criteria for later prompt tests

- **Coverage:** important decisions and commitments from the transcript appear in output.
- **Evidence support:** every factual claim is entailed by its cited source turns.
- **Attribution:** speaker, owner, and due date are not assigned without transcript evidence.
- **Readability:** the summary removes filler and repetition without losing disagreement or uncertainty.
- **Incremental stability:** new turns update the summary without silently reversing prior decisions.

Automatic overlap scores can help compare drafts, but human review of support, coverage, and attribution is needed for this meeting use case. The meeting-summary survey discusses the task’s datasets, models, and evaluation metrics, underscoring that a single generic score does not capture all of these properties. [Rennard et al.](https://aclanthology.org/2023.tacl-1.49/)

## Week output contract

**Input:** Timestamped transcript segments with speaker IDs from Dhruv, or synthetic transcript fixtures while the capture/ASR stage is not implemented.

**Output:** A readable overview plus candidate decisions/actions, each with source segment IDs and confidence; unsupported fields remain unknown.

## Sources

- [Rennard et al. (2023), *Abstractive Meeting Summarization: A Survey*](https://aclanthology.org/2023.tacl-1.49/)
- [Kumar & Gangadharaiah (2022), *Are Abstractive Summarization Models truly ‘Abstractive’?*](https://aclanthology.org/2022.gem-1.17/)
- [Beckage et al. (2021), *Context or No Context? Incremental Temporal Summarization in meetings*](https://aclanthology.org/2021.newsum-1.11/)
