"""Mastheads for each project page, in the same style as the profile.

Each repo keeps its own copy of the SVGs (in .github/assets) so its README has no outside dependency.
Run from a folder that holds the repo clones: python3 roy-vinay/roy-vinay/cards/make_pages.py <clones-dir>
"""
import sys
from pathlib import Path

from masthead import THEMES, masthead

BY = "By Vinay Roy"
PAGES = {
    # key: (repo dir, asset name, title, left, center, cols)
    "applied-ai-agents": ("applied-ai-agents", "masthead", "Applied AI Agents", "roy-vinay / applied-ai-agents",
        "Build and evaluate", [
            ("What it is", ["Agents with guardrails,", "evals and trade-offs"]),
            ("Start here", ["A guarded support agent,", "no API key needed"]),
            ("Failure Files", ["Public AI incidents,", "reproduced and measured"]),
            ("Tools", ["Tech60 and mdEditDiff,", "two Mac apps"])]),
    "failure-files": ("applied-ai-agents", "failure-files-masthead", "Failure Files", "applied-ai-agents / failure-files",
        "Explore failure experiments", [
            ("The idea", ["Public AI failures,", "turned into experiments"]),
            ("Latest", ["FF-05: what do rules in", "the prompt actually buy?"]),
            ("FF-01", ["Made-up policy: 80% caught,", "6% of good answers blocked"]),
            ("Method", ["Fixes tested one at a time,", "with what each one costs"])]),
    "tech60": ("applied-ai-agents", "tech60-masthead", "Tech60", "applied-ai-agents / tools / tech60",
        "Try the tools", [
            ("What it is", ["A tech news front page", "on your Mac desktop"]),
            ("Signal", ["Only stories getting real", "attention, ranked"]),
            ("Summaries", ["Checked against the source,", "made on your Mac"]),
            ("Get it", ["Free for macOS 14", "and later, MIT"])]),
    "enterprise-ai-platform": ("enterprise-ai-platform", "masthead", "Enterprise AI Platform",
        "roy-vinay / enterprise-ai-platform", "Build and evaluate", [
            ("What it is", ["AI decision systems", "for B2B SaaS"]),
            ("First module", ["Evals for BI chat bots:", "answer, refuse, or ask"]),
            ("Methods", ["Trap questions, metamorphic", "and mutation testing"]),
            ("Runs locally", ["Synthetic data,", "no API keys"])]),
    "ai-decision-log": ("ai-decision-log", "masthead", "AI Decision Log", "roy-vinay / ai-decision-log",
        "Decisions and practices", [
            ("What it is", ["One-page memos on applied", "AI product choices"]),
            ("Latest", ["When should a BI bot", "stay quiet?"]),
            ("Format", ["Options, evidence, decision,", "and what would change it"]),
            ("Models", ["Rerun the numbers with", "your own assumptions"])]),
    "claude-code-team-playbook": ("claude-code-team-playbook", "masthead", "Claude Code Team Playbook",
        "roy-vinay / claude-code-team-playbook", "Decisions and practices", [
            ("The constraint", ["AI made code cheap.", "Review is now scarce"]),
            ("The model", ["One spec, one builder,", "QA and review in parallel"]),
            ("Claim Before Code", ["Overlapping edits go to", "the owner, not a conflict"]),
            ("Inside", ["Starter files, specs,", "and a rework log"])]),
    "mdeditdiff": ("mdeditdiff", "masthead", "mdEditDiff", "roy-vinay / mdeditdiff", "Try the tools", [
            ("What it is", ["An editor for people,", "a diff for agents"]),
            ("For agents", ["CLI and MCP server that", "return only what changed"]),
            ("For people", ["A native Mac app with", "changes highlighted"]),
            ("License", ["Free and open source,", "MIT"])]),
}

LOCAL = {"applied-ai-agents": "aaa"}  # clone folder names that differ from the repo name


def main(root):
    for key, (repo, name, title, left, center, cols) in PAGES.items():
        out = Path(root) / LOCAL.get(repo, repo) / ".github" / "assets"
        out.mkdir(parents=True, exist_ok=True)
        label = f"{title}. {center}. " + " ".join(f"{h}: {' '.join(ls)}." for h, ls in cols)
        for theme, t in THEMES.items():
            (out / f"{name}-{theme}.svg").write_text(masthead(t, title, left, center, BY, cols, label))
        print(out / name)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
