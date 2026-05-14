#!/usr/bin/env python3
"""
Post-Meeting Report HTML Renderer — fills the Jinja2 template with structured data and outputs rendered HTML.

Usage:
    python render_pmr.py input.json output.html

Input: JSON file with the PMR data structure (see DATA_SCHEMA below).
Output: Rendered HTML file.

DATA SCHEMA (what the agent produces):
{
    "customer_name": "明华重工",
    "meeting_title": "POC 验证方案评审会",
    "meeting_date": "2026-03-20",
    "recorded_by": "Sarah Chen (AM)",
    "related_document": "Call Plan - POC 验证方案评审会",
    "outcome_results": [
        {
            "number": 1,
            "target_outcome": "...",
            "result": "achieved",  // achieved, partial, not_achieved
            "evidence": "..."
        }
    ],
    "fallback_outcome_assessment": "...",
    "stage_progression": {
        "planned": "Technical Validation → Business Validation",
        "actual": "Technical Validation → Business Validation",
        "achieved": true
    },
    "sentiment_changes": [
        {
            "attendee": "刘总 (CTO)",
            "stance_before": "Supporter",
            "stance_after": "Sponsor",
            "evidence": "..."
        }
    ],
    "key_findings": [
        {
            "finding": "...",
            "source": "...",
            "implication": "..."
        }
    ],
    "info_gap_check": [
        {
            "question": "...",
            "status": "answered",  // answered, unanswered
            "answer_notes": "..."
        }
    ],
    "ep_updates": [
        {
            "section": "Key Stakeholders",
            "change_type": "Update",  // Update, Add, Remove
            "what_to_write": "..."
        }
    ],
    "execution_log_update": "...",
    "agent_recommendation": "...",
    "planned_next_steps": [
        {"step": "...", "owner": "...", "timeline": "..."}
    ],
    "actual_next_steps": [
        {"step": "...", "owner": "...", "timeline": "...", "delta": "..."}
    ],
    "action_items": [
        {
            "priority": "High",  // High, Medium, Low
            "action": "...",
            "owner": "...",
            "eta": "...",
            "status": "Pending"  // Pending, In Progress, Done
        }
    ],
    "recap_email_points": ["..."],
    "last_updated": "2026-05-14"
}
"""

import json
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2", file=sys.stderr)
    sys.exit(1)


def render_pmr(data: dict, template_dir: str = None) -> str:
    """Render Post-Meeting Report data into HTML string."""
    if template_dir is None:
        template_dir = str(Path(__file__).parent)

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=True
    )
    template = env.get_template("post-meeting-report.html.j2")
    return template.render(**data)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} input.json output.html", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html = render_pmr(data)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Rendered: {output_path}")


if __name__ == "__main__":
    main()
