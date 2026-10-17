"""Generates the profile's banner and project cards as light and dark SVGs.

GitHub renders SVG images with their own styling, but loads no web fonts, so the cards use system
font stacks. Text is wrapped here by hand. Run: python3 cards/make_cards.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

THEMES = {
    "light": dict(bg="#FFFFFF", border="#D0D7DE", ink="#1F2328", body="#424A53", muted="#59636E",
                  accent="#C2410C", track="#EAEEF2"),
    "dark": dict(bg="#161B22", border="#30363D", ink="#E6EDF3", body="#C9D1D9", muted="#9198A1",
                 accent="#FF8A3D", track="#262C36"),
}

CARDS = [
    ("applied-ai-agents", "Build and evaluate", "Applied AI Agents",
     ["Agents with guardrails and evals, plus Failure",
      "Files: public AI incidents reproduced and the",
      "fixes measured."],
     "Duplicate payments: 79/100 unguarded, 0/100 guarded."),
    ("enterprise-ai-platform", "Build and evaluate", "Enterprise AI Platform",
     ["Evals for BI chat bots that test when a bot",
      "should answer, refuse, or ask, with results",
      "from two real models."],
     "Trap questions, consistency, mutation testing."),
    ("ai-decision-log", "Decisions and practices", "AI Decision Log",
     ["One-page memos on applied AI product choices:",
      "the options, the numbers, and what would",
      "change the answer."],
     "Latest: when should a BI bot stay quiet?"),
    ("claude-code-team-playbook", "Decisions and practices", "Claude Code Team Playbook",
     ["Run several coding agents like a small team.",
      "Claim Before Code sends overlapping edits to",
      "the owner, not a merge conflict."],
     "Starter files, specs, and a rework log."),
    ("mdeditdiff", "Try the tools", "mdEditDiff",
     ["A Markdown editor for people and a change diff",
      "for agents: agents see only what changed since",
      "they last looked."],
     "Mac app, CLI, and MCP server. Free, MIT."),
    ("tech60", "Try the tools", "Tech60",
     ["A tech news front page for the Mac desktop:",
      "only stories with real signal, each with a",
      "short on-device summary."],
     "Summaries must pass checks against the source."),
]


def ring(cx, cy, r, width, fraction, color, track):
    import math
    circ = 2 * math.pi * r
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{track}" stroke-width="{width}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-dasharray="{circ * fraction:.1f} {circ:.1f}" '
            f'transform="rotate(-90 {cx} {cy})"/>')


def card(slug, kicker, title, lines, evidence, t):
    # The section heading above each pair already names the group, so the card leads with its title.
    w, h = 480, 224
    body = "".join(
        f'<text x="28" y="{100 + i * 25}" font-family="{SANS}" font-size="17" fill="{t["body"]}">{escape(l)}</text>'
        for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}: {escape(" ".join(lines))}">
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>
{ring(w - 40, 44, 12, 3.5, 0.82, t["accent"], t["track"])}
<text x="28" y="56" font-family="{SERIF}" font-size="29" font-weight="700" fill="{t["ink"]}">{escape(title)}</text>
{body}
<line x1="28" y1="178" x2="{w - 28}" y2="178" stroke="{t["border"]}"/>
<text x="28" y="204" font-family="{SANS}" font-size="15" font-weight="600" fill="{t["accent"]}">{escape(evidence)}</text>
</svg>
'''


def banner(t):
    w, h = 1200, 280
    rings = "".join([
        ring(1040, 140, 96, 10, 0.86, t["accent"], t["track"]),
        ring(1040, 140, 72, 10, 0.62, t["ink"], t["track"]),
        ring(1040, 140, 48, 10, 0.38, t["muted"], t["track"]),
    ])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Vinay Roy. I build, evaluate, and ship AI decision systems.">
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="{t["bg"]}" stroke="{t["border"]}"/>
<text x="56" y="128" font-family="{SERIF}" font-size="76" font-weight="700" fill="{t["ink"]}" letter-spacing="-1">Vinay Roy</text>
<rect x="58" y="150" width="64" height="4" rx="2" fill="{t["accent"]}"/>
<text x="56" y="196" font-family="{SANS}" font-size="29" fill="{t["ink"]}">I build, evaluate, and ship AI decision systems.</text>
<text x="56" y="232" font-family="{SANS}" font-size="19" fill="{t["muted"]}">VP of Product at Burq.ai. Seven years teaching AI strategy at UC Berkeley Exec Ed.</text>
{rings}
</svg>
'''


for name, t in THEMES.items():
    (OUT / f"banner-{name}.svg").write_text(banner(t))
    for slug, *rest in CARDS:
        (OUT / f"{slug}-{name}.svg").write_text(card(slug, *rest, t))
print("Wrote", len(list(OUT.glob("*.svg"))), "SVGs")
