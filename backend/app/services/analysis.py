"""
Simple analysis engine stub.
- Accepts MR change object (from get_mr_changes)
- Runs placeholder static checks (you will plug real linters / LLM here)
- Returns structured result and markdown summary
"""
import json

def analyze_mr(mr_changes):
    # mr_changes expected structure contains 'changes' list with file diffs
    summary_lines = []
    problems = []
    changes = mr_changes.get("changes", [])
    summary_lines.append(f"**Files changed:** {len(changes)}\n")
    for ch in changes:
        new_path = ch.get("new_path")
        old_path = ch.get("old_path")
        diff = ch.get("diff", "")
        # trivial heuristic checks - TODO replace with real linters
        if new_path and new_path.endswith(".py") and "print(" in diff:
            problems.append({
                "file": new_path,
                "severity": "warning",
                "description": "Found 'print()' usage in code change. Consider using logging."
            })
        if "TODO" in diff or "FIXME" in diff:
            problems.append({
                "file": new_path,
                "severity": "info",
                "description": "Contains TODO/FIXME markers."
            })
    # Make markdown
    md = []
    md.append(f"### AgentOps Review Summary")
    md.append(f"- Files changed: **{len(changes)}**")
    if problems:
        md.append("\n**Potential issues found:**\n")
        for p in problems:
            md.append(f"- `{p['file']}` — **{p['severity']}**: {p['description']}")
    else:
        md.append("\nNo obvious issues found by the basic checks.\n")
    md_text = "\n".join(md)
    return {"summary_markdown": md_text, "problems": problems}
