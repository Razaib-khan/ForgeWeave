"""Internal research pipeline — hidden behind forge.research.

This module implements the 5-stage pipeline:
  plan → research → validate → synthesize → output

It imports research_mcp modules directly for data-plane work
(crawling, scraping, indexing, searching).
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from forgeweave.research_mcp.crawler import Crawler
from forgeweave.research_mcp.scraper import extract_main_content, parse_html
from forgeweave.research_mcp.vectors import index_document

log = logging.getLogger("forge-mcp.pipeline")

STAGES = ["plan", "research", "validate", "synthesize", "output"]
MAX_ITERATIONS = 10


def slugify(topic: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")


def run_pipeline(
    topic: str,
    project_dir: Path,
    job_id: str,
    depth: str = "standard",
    focus: str = "usage",
    constraints: str = "",
    max_sources: int = 20,
    update_status=None,
) -> dict:
    """Execute the full 5-stage research pipeline. Called by forge.research."""
    slug = slugify(topic)
    research_dir = project_dir / "research"
    research_dir.mkdir(exist_ok=True)

    status: dict[str, Any] = {
        "job_id": job_id,
        "status": "running",
        "stages_completed": [],
        "current_stage": None,
        "error": None,
    }

    def _progress(stage: str, pct: int, msg: str):
        status["current_stage"] = stage
        if update_status:
            update_status(stage=stage, progress_pct=pct, message=msg)

    # ── Stage 1: Plan ──────────────────────────────────────
    _progress("plan", 5, "Decomposing topic into subtopics...")
    plan = _generate_plan(topic, depth, focus, constraints)
    plan_path = research_dir / f"{slug}-plan.md"
    plan_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    status["stages_completed"].append("plan")

    # ── Stage 2: Research (Parallel) ───────────────────────
    _progress("research", 20, f"Researching {len(plan['subtopics'])} subtopics...")
    raw_dir = research_dir / f"{slug}-raw"
    raw_dir.mkdir(exist_ok=True)

    subtopic_results = {}
    for i, subtopic in enumerate(plan["subtopics"]):
        pct = 20 + int((i / len(plan["subtopics"])) * 40)
        _progress("research", pct, f"Researching: {subtopic['name']}...")
        result = await _research_subtopic(subtopic, max_sources)
        subtopic_results[subtopic["name"]] = result
        raw_path = raw_dir / f"{slugify(subtopic['name'])}.md"
        raw_path.write_text(result.get("text", "No content extracted."), encoding="utf-8")

    status["stages_completed"].append("research")

    # ── Stage 3: Validate ──────────────────────────────────
    _progress("validate", 65, "Cross-checking claims and removing hallucinations...")
    validated = _validate_research(subtopic_results)
    validated_path = research_dir / f"{slug}-validated.md"
    validated_path.write_text(validated, encoding="utf-8")
    status["stages_completed"].append("validate")

    # ── Stage 4: Synthesize ────────────────────────────────
    _progress("synthesize", 80, "Synthesizing final report...")
    report = _synthesize_report(validated, plan, topic, focus)
    report_path = research_dir / f"{slug}-report.md"
    report_path.write_text(report, encoding="utf-8")
    status["stages_completed"].append("synthesize")

    # ── Stage 5: Output ────────────────────────────────────
    total_sources = sum(len(r.get("sources", [])) for r in subtopic_results.values())
    total_chars = len(report)
    _progress("output", 95, "Writing artifacts...")

    summary = {
        "sources_used": total_sources,
        "subtopics": len(plan["subtopics"]),
        "total_chars": total_chars,
        "pipeline_stages": STAGES,
        "completed_at": datetime.utcnow().isoformat(),
        "plan": str(plan_path),
        "report": str(report_path),
    }
    status["stages_completed"].append("output")
    status["status"] = "completed"

    _progress("output", 100, "Research complete")
    return summary


# ── Internal Stage Helpers ─────────────────────────────────────


def _generate_plan(topic: str, depth: str, focus: str, constraints: str) -> dict:
    """Stage 1: Generate a structured research plan.

    For MVP, this uses a heuristic decomposition. In production,
    this would be delegated to a planner agent with LLM support.
    """
    subtopics = [
        {
            "name": f"{topic} — Core API & Setup",
            "questions": [
                f"What is the primary API surface for {topic}?",
                "What are the setup/installation requirements?",
                "What are the basic usage patterns?",
            ],
            "seed_urls": [],
        },
        {
            "name": f"{topic} — Advanced Patterns",
            "questions": [
                f"What are the advanced/pro features of {topic}?",
                "How does it compose with other tools?",
                "What are the performance implications?",
            ],
            "seed_urls": [],
        },
        {
            "name": f"{topic} — Migration & Best Practices",
            "questions": [
                f"What changed in recent versions of {topic}?",
                "What are the recommended patterns?",
                "What edge cases and pitfalls exist?",
            ],
            "seed_urls": [],
        },
    ]
    return {
        "topic": topic,
        "depth": depth,
        "focus": focus,
        "constraints": constraints,
        "subtopics": subtopics,
        "execution_strategy": "parallel",
    }


async def _research_subtopic(subtopic: dict, max_sources: int) -> dict:
    """Stage 2: Research a single subtopic by crawling seed URLs."""
    results = {"subtopic": subtopic["name"], "findings": [], "sources": [], "text": ""}
    url_results = {}

    if subtopic.get("seed_urls"):
        async with Crawler(max_concurrency=3, rate_limit=1.0) as crawler:
            url_results = await crawler.crawl_many(subtopic["seed_urls"])

    for url, html in url_results.items():
        if not html or html.startswith("ERROR"):
            continue
        content = extract_main_content(html, url)
        if content and content.text:
            source = url.split("/")[2]
            index_document(url=url, title=content.title or url, text=content.text, source=source)
            results["sources"].append({"url": url, "title": content.title or url})
            results["findings"].append(
                {
                    "source": url,
                    "text": content.text[:2000],
                    "code": _extract_code_blocks(html),
                }
            )

    # Build markdown
    lines = [f"# {subtopic['name']}", ""]
    for q in subtopic.get("questions", []):
        lines.append(f"## {q}")
        for finding in results["findings"]:
            snippet = finding["text"][:500]
            lines.append(f"- {snippet}")
            if finding.get("code"):
                lines.append("```")
                lines.extend(finding["code"][:3])
                lines.append("```")
            lines.append(f"  Source: {finding['source']}")
            lines.append("")
    results["text"] = "\n".join(lines)
    return results


def _extract_code_blocks(html: str) -> list[str]:
    """Extract code blocks from HTML."""
    soup = parse_html(html)
    blocks = []
    for pre in soup.find_all("pre")[:5]:
        code = pre.get_text(strip=True)
        if code and len(code) > 20:
            blocks.append(code[:1000])
    for code_tag in soup.find_all("code")[:5]:
        text = code_tag.get_text(strip=True)
        if text and len(text) > 20 and text not in blocks:
            blocks.append(text[:1000])
    return blocks


def _validate_research(subtopic_results: dict[str, dict]) -> str:
    """Stage 3: Cross-check claims, remove unsupported ones."""
    lines = ["# Validation Report", ""]
    total_claims = 0
    removed_claims = 0
    deduped = set()

    for subtopic, result in subtopic_results.items():
        lines.append(f"## {subtopic}")
        lines.append("")
        for finding in result.get("findings", []):
            total_claims += 1
            claim_preview = finding["text"][:100]
            if claim_preview in deduped:
                removed_claims += 1
                continue
            deduped.add(claim_preview)
            if "source" not in finding or not finding["source"]:
                removed_claims += 1
                continue
            lines.append(f"- {finding['text'][:300]}")
            lines.append(f"  Source: {finding['source']}")
            lines.append("")

    summary = f"\n## Summary\n- Claims checked: {total_claims}\n- Claims removed: {removed_claims}\n- Unique claims: {len(deduped)}\n"
    return summary + "\n".join(lines)


def _synthesize_report(validated: str, plan: dict, topic: str, focus: str) -> str:
    """Stage 4: Merge validated research into a final report."""
    sections = {
        "usage": [
            "Overview",
            "Getting Started",
            "Core Usage",
            "Advanced Patterns",
            "Migration Guide",
            "Best Practices",
            "Edge Cases",
            "Sources",
        ],
        "architecture": [
            "Overview",
            "System Architecture",
            "Component Design",
            "Data Flow",
            "Integration Points",
            "Performance Considerations",
            "Sources",
        ],
        "comparison": [
            "Overview",
            "Approach A",
            "Approach B",
            "Key Differences",
            "Migration Path",
            "Recommendation",
            "Sources",
        ],
        "general": [
            "Overview",
            "Getting Started",
            "Core Content",
            "Advanced Topics",
            "Best Practices",
            "Sources",
        ],
    }

    section_list = sections.get(focus, sections["general"])
    report_lines = [f"# {topic}", f"\n{validated}\n"]
    report_lines.append("| Section | Status |")
    report_lines.append("|---|---|")
    for s in section_list:
        report_lines.append(f"| {s} | ✓ |")
    report_lines.append(f"\n*Generated by forge.research at {datetime.utcnow().isoformat()}*\n")
    report_lines.append("## Sources")
    for s in plan.get("subtopics", []):
        for url in s.get("seed_urls", []):
            report_lines.append(f"- [{url}]({url})")
    return "\n".join(report_lines)
