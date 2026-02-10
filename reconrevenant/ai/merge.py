from typing import List


def merge_ai_insights(baseline: List[str], ai_text: str | None) -> List[str]:
    if not ai_text:
        return baseline

    insights = [line.strip("- ").strip() for line in ai_text.splitlines() if line.strip()]

    # avoid duplicates
    merged = baseline[:]
    for i in insights:
        if i and i not in merged:
            merged.append(i)

    return merged

