"""Mastheads for each project page, in the same style as the profile.

Each repo keeps its own copy of the SVGs (in .github/assets) so its README has no outside dependency.
Run from a folder that holds the repo clones: python3 roy-vinay/roy-vinay/cards/make_pages.py <clones-dir>
"""
import sys
from pathlib import Path

from make_cards import CARDS, about, article, card
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
            ("What it is", ["What changed since each", "person or agent last read"]),
            ("For agents", ["CLI and MCP server that", "return only what changed"]),
            ("For people", ["A native Mac app with", "changes highlighted"]),
            ("Across", ["Sessions, coding tools,", "and uncommitted edits"])]),
    "mcp-chat": ("applied-ai-agents", "mcp-chat-masthead", "MCP Chat", "applied-ai-agents / agents / mcp-chat",
        "Build and evaluate", [
            ("What it is", ["A terminal chat app on the", "Model Context Protocol"]),
            ("How it works", ["An MCP client and server", "talking over stdio"]),
            ("Features", ["@document mentions", "and /commands"]),
            ("Needs", ["Python 3.9 or later and", "an Anthropic API key"])]),
    "guarded-support-agent": ("applied-ai-agents", "guarded-agent-masthead", "Guarded Support Agent",
        "applied-ai-agents / production-patterns", "Build and evaluate", [
            ("What it is", ["A support agent built", "to survive production"]),
            ("Guards", ["Authorization in code,", "budgets, idempotent writes"]),
            ("Evidence", ["Duplicate payments:", "79/100 off, 0/100 on"]),
            ("Run it", ["Locally, no API key,", "12 evals in CI"])]),
    "ff-01": ("applied-ai-agents", "ff-01-masthead", "FF-01: Made-up Policy", "applied-ai-agents / failure-files",
        "Explore failure experiments", [
            ("The question", ["Can you stop a chatbot", "from making up policy?"]),
            ("The incident", ["An airline chatbot case,", "Canada, 2024"]),
            ("Best guard", ["A small yes/no model:", "80% caught, 6% blocked"]),
            ("Cost", ["About 2 cents across", "600 answers"])]),
    "ff-05": ("applied-ai-agents", "ff-05-masthead", "FF-05: Rules in the Prompt", "applied-ai-agents / failure-files",
        "Explore failure experiments", [
            ("The question", ["What do rules in the", "prompt actually buy?"]),
            ("The incident", ["A coding agent deleted a", "production database, 2025"]),
            ("With rules", ["Neither model broke", "a single rule"]),
            ("Without them", ["The larger model gave out", "emails on every try"])]),
    "mdeditdiff-moved": ("applied-ai-agents", "mdeditdiff-moved-masthead", "mdEditDiff Has Moved",
        "applied-ai-agents / tools / mdeditdiff", "Try the tools", [
            ("New home", ["github.com/roy-vinay/", "mdeditdiff"]),
            ("There", ["Mac app, CLI, MCP server,", "docs and website"]),
            ("Old releases", ["Up to 0.5.3 stay on this", "repo's Releases page"]),
            ("History", ["Before the move, in this", "repo's git log"])]),
    "text-to-sql": ("enterprise-ai-platform", "text-to-sql-masthead", "Text-to-SQL Evals",
        "enterprise-ai-platform / evals / text-to-sql", "Build and evaluate", [
            ("The question", ["When should a BI bot", "stay quiet?"]),
            ("Trap set", ["Refusing and clarifying", "scored as right answers"]),
            ("No answer key", ["Metamorphic tests check", "answers against each other"]),
            ("Mutation testing", ["Break the semantic model,", "see if the evals notice"])]),
    "d-001": ("ai-decision-log", "d-001-masthead", "D-001: Ticket Routing", "ai-decision-log / decisions",
        "Decisions and practices", [
            ("The question", ["Rules, LLM, or hybrid for", "support ticket routing?"]),
            ("Status", ["Decided"]),
            ("Area", ["Agent architecture,", "cost"]),
            ("Model", ["A cost model you can", "rerun, in models/"])]),
    "d-002": ("ai-decision-log", "d-002-masthead", "D-002: How Many Evals", "ai-decision-log / decisions",
        "Decisions and practices", [
            ("The question", ["How many evals", "are enough?"]),
            ("Status", ["Decided"]),
            ("Area", ["Evaluation"]),
            ("Model", ["A sample-size model you", "can rerun, in models/"])]),
    "d-003": ("ai-decision-log", "d-003-masthead", "D-003: When to Stay Quiet", "ai-decision-log / decisions",
        "Decisions and practices", [
            ("The question", ["When should a BI bot", "answer, or stay quiet?"]),
            ("Status", ["Decided, no launch yet"]),
            ("Area", ["Evaluation, trust,", "cost"]),
            ("Model", ["An abstention model you", "can rerun, in models/"])]),
}

# Dark cards and tiles, same design as the profile. (repo, asset name, kind, args)
PROFILE_CARDS = {c[0]: c[1:] for c in CARDS}
EXTRA = [
    ("applied-ai-agents", "card-guarded-support-agent", "card", ("Build and evaluate", "Guarded Support Agent",
        ["Authorization in code, retries, budgets,", "idempotent writes, PII redaction and", "injection screening, tested in CI."],
        "Duplicate payments: 79/100 unguarded, 0/100 guarded.")),
    ("applied-ai-agents", "card-mcp-chat", "card", ("Build and evaluate", "MCP Chat",
        ["A terminal chat app that shows the Model", "Context Protocol end to end: a client and", "a server talking over stdio."],
        "Python and MCP, with @mentions and /commands.")),
    ("applied-ai-agents", "card-ff-01", "card", ("Failure Files", "FF-01: Made-up Policy",
        ["Can you stop a support chatbot from", "inventing policy? The Air Canada case,", "tested in four phases."],
        "80% of failures caught, 6% wrongly blocked.")),
    ("applied-ai-agents", "card-ff-05", "card", ("Failure Files", "FF-05: Rules in the Prompt",
        ["What does telling an agent the rules buy", "you? The Replit database deletion,", "tested on a data bot."],
        "No rules: the larger model leaked emails.")),
    ("applied-ai-agents", "card-tech60", "card", PROFILE_CARDS["tech60"]),
    ("applied-ai-agents", "card-mdeditdiff", "card", PROFILE_CARDS["mdeditdiff"]),
    ("applied-ai-agents", "card-ai-decision-log", "card", PROFILE_CARDS["ai-decision-log"]),
    ("enterprise-ai-platform", "card-text-to-sql", "card", ("Modules", "Text-to-SQL Evals",
        ["Evals for BI chat bots that measure when", "they should stay quiet: trap questions,", "metamorphic and mutation testing."],
        "Fails right answers produced the wrong way.")),
    ("ai-decision-log", "tile-d-001", "tile", ("D-001", ["Rules, LLM, or hybrid", "for support ticket", "routing?"])),
    ("ai-decision-log", "tile-d-002", "tile", ("D-002", ["How many evals", "are enough?"])),
    ("ai-decision-log", "tile-d-003", "tile", ("D-003", ["When should a BI bot", "answer, and when should", "it stay quiet?"])),
    ("applied-ai-agents", "card-download-tech60", "card", ("Mac app downloads", "Tech60",
        ["A tech news front page for the Mac desktop.", "Early build for macOS 14 and later. Summaries", "need Apple Intelligence on macOS 26."],
        "Download for Mac")),
    ("applied-ai-agents", "card-download-mdeditdiff", "card", ("Mac app downloads", "mdEditDiff",
        ["What changed since each reader last looked.", "Early release for macOS 14 and later.", "Free and open source, MIT."],
        "Download for Mac")),
    ("claude-code-team-playbook", "tile-article", "tile", ("Substack", ["More Claude Code Sessions", "Made Me Ship Less. Here's", "What Fixed It."])),
]
ABOUT_REPOS = ["applied-ai-agents", "enterprise-ai-platform", "ai-decision-log", "claude-code-team-playbook", "mdeditdiff"]

LOCAL = {"applied-ai-agents": "aaa"}  # clone folder names that differ from the repo name


def main(root):
    for key, (repo, name, title, left, center, cols) in PAGES.items():
        out = Path(root) / LOCAL.get(repo, repo) / ".github" / "assets"
        out.mkdir(parents=True, exist_ok=True)
        label = f"{title}. {center}. " + " ".join(f"{h}: {' '.join(ls)}." for h, ls in cols)
        for theme, t in THEMES.items():
            (out / f"{name}-{theme}.svg").write_text(masthead(t, title, left, center, BY, cols, label))
        print(out / name)
    for repo, name, kind, args in EXTRA:
        out = Path(root) / LOCAL.get(repo, repo) / ".github" / "assets"
        for theme, t in THEMES.items():
            svg = card(f"{name}-{theme}", *args, t) if kind == "card" else article(args[0], args[1], t, f"{name}-{theme}")
            (out / f"{name}-{theme}.svg").write_text(svg)
    for repo in ABOUT_REPOS:
        out = Path(root) / LOCAL.get(repo, repo) / ".github" / "assets"
        for theme, t in THEMES.items():
            (out / f"about-{theme}.svg").write_text(about(t))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
