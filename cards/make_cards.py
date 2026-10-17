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
    # An article header: section label, a two-line serif headline, and a byline.
    w, h = 1200, 280
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Moving AI from demos into production, one measured failure at a time. By Vinay Roy, VP of Product at Burq.ai.">
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="{t["bg"]}" stroke="{t["border"]}"/>
<text x="60" y="64" font-family="{SANS}" font-size="17" font-weight="700" fill="{t["accent"]}">Applied AI</text>
<text x="60" y="124" font-family="{SERIF}" font-size="50" font-weight="700" letter-spacing="-0.8" fill="{t["ink"]}">Moving AI from demos into production,</text>
<text x="60" y="182" font-family="{SERIF}" font-size="50" font-weight="700" letter-spacing="-0.8" fill="{t["ink"]}">one measured failure at a time</text>
<circle cx="80" cy="231" r="20" fill="{t["ink"]}"/>
<text x="80" y="237" text-anchor="middle" font-family="{SERIF}" font-size="16" font-weight="700" fill="{t["bg"]}">VR</text>
<text x="112" y="238" font-family="{SANS}" font-size="20" fill="{t["muted"]}">By <tspan font-weight="700" fill="{t["ink"]}">Vinay Roy</tspan>, VP of Product at Burq.ai</text>
</svg>
'''


S = "https://vinayroy.substack.com/p/"
ARTICLES = [  # newest first; (slug, outlet, title lines, url)
    ("article-retros-rewired", "Substack", ["The Retrospective,", "Rewired: How to Run Retros", "When Agents Write the Code"], S + "the-retrospective-rewired-how-to"),
    ("article-product-job", "Substack", ["AI Didn't Take the", "Product Job. It Took", "Our Excuse."], S + "ai-didnt-take-the-product-job-it"),
    ("article-agents-stepping", "Medium", ["When Your Team's Coding", "Agents Start Stepping on", "Each Other"],
     "https://vinaysays.medium.com/when-your-teams-coding-agents-start-stepping-on-each-other-c6fd4c0f44aa"),
    ("article-claude-sessions", "Substack", ["More Claude Code Sessions", "Made Me Ship Less. Here's", "What Fixed It."], S + "more-claude-code-sessions-made-me"),
    ("article-survive-production", "Medium", ["Building AI Agents That", "Survive Production"],
     "https://vinaysays.medium.com/building-ai-agents-that-survive-production-5bbb2257ba0a"),
    ("article-10x-pms", "Substack", ["Same Team, 10x the Output:", "How PMs Become 10x", "with AI"], S + "same-team-10x-the-output-how-pms"),
    ("article-harness-engineering", "Substack", ["Harness Engineering:", "The Last Guide You Need"], S + "harness-engineering-the-last-guide-you-need-b0a5708b93b5"),
    ("article-pm-agent-stack", "Substack", ["The PM's Agent Stack:", "What I Delegate to Agents", "vs. Keep Human"], S + "the-pms-agent-stack-what-i-delegate-to-agents-vs-keep-human-6947b51f3416"),
    ("article-knowledge-graph", "Substack", ["The Future of Knowledge", "Is a Graph"], S + "the-future-of-knowledge-is-a-graph-824847e16e74"),
    ("article-subagents-teams", "Substack", ["Claude Code: Subagents", "vs Agent Teams"], S + "claude-code-subagents-vs-agent-teams-54cacb96f6c0"),
]


def article(pub, lines, t, slug):
    # Dark tiles in both themes, with the outlet's initial set large and faint behind the title.
    w, h = 400, 230
    dark = t["bg"] != "#FFFFFF"
    tile, border, ghost = ("#1C2533", "#30363D", "#2A3446") if dark else ("#18202C", "#18202C", "#243042")
    title = "".join(
        f'<text x="28" y="{62 + i * 30}" font-family="{SERIF}" font-size="23" font-weight="700" fill="#F0F3F6">{escape(l)}</text>'
        for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(" ".join(lines))}, on {pub}">
<defs><clipPath id="c-{slug}"><rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16"/></clipPath></defs>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{tile}" stroke="{border}"/>
<g clip-path="url(#c-{slug})"><text x="{w + 8}" y="{h + 34}" text-anchor="end" font-family="{SERIF}" font-size="190" font-weight="700" fill="{ghost}">{pub[0]}</text></g>
{title}
<text x="28" y="{h - 26}" font-family="{SANS}" font-size="15" font-weight="700" fill="#FF8A3D">{pub}</text>
</svg>
'''


TIMELINE = [("2008", "NVIDIA", "Engineering"), ("2012", "Qualcomm", "Engineering"), ("2015", "Apple", "Sidecar, macOS"),
            ("2019", "Zeus Living", "Marketplace growth"), ("2020", "Vista", "Team of about 80"),
            ("2024", "AI SaaS startup", "Founding product"), ("Now", "Burq.ai", "VP of Product")]


def about(t):
    w, h = 1200, 360
    x0, x1 = 60, 1140
    step = 154
    stops = []
    for i, (year, org, note) in enumerate(TIMELINE):
        x = x0 + 8 + i * step
        last = i == len(TIMELINE) - 1
        anchor = "start"
        tx = x - 8
        color = t["accent"] if last else t["ink"]
        dot = (f'<circle cx="{x:.0f}" cy="186" r="9" fill="{t["accent"]}"/>' if last else
               f'<circle cx="{x:.0f}" cy="186" r="7" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="2.5"/>')
        stops.append(f'''{dot}
<text x="{tx:.0f}" y="166" text-anchor="{anchor}" font-family="{SANS}" font-size="15" fill="{t["accent"] if last else t["muted"]}" font-weight="{700 if last else 400}">{year}</text>
<text x="{tx:.0f}" y="220" text-anchor="{anchor}" font-family="{SANS}" font-size="18" font-weight="700" fill="{color}">{escape(org)}</text>
<text x="{tx:.0f}" y="243" text-anchor="{anchor}" font-family="{SANS}" font-size="14" fill="{t["muted"]}">{escape(note)}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Career: NVIDIA 2008, Qualcomm 2012, Apple 2015 (Sidecar), Zeus Living 2019, Vista 2020, founding product lead at an AI SaaS startup 2024, now VP of Product at Burq.ai. Seven years as Head Instructor for the AI/ML executive program at UC Berkeley Executive Education, 10,000+ leaders. 3 US patents. MBA, Berkeley Haas. MS, IIT Roorkee.">
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="{t["bg"]}" stroke="{t["border"]}"/>
<text x="60" y="64" font-family="{SANS}" font-size="17" font-weight="700" fill="{t["accent"]}">About</text>
<text x="60" y="106" font-family="{SERIF}" font-size="32" font-weight="700" fill="{t["ink"]}">VP of Product at Burq.ai, leading Product, Design and AI.</text>
<line x1="{x0 + 8}" y1="186" x2="{x0 + 8 + step * (len(TIMELINE) - 1):.0f}" y2="186" stroke="{t["border"]}" stroke-width="2"/>
{"".join(stops)}
<line x1="60" y1="282" x2="1140" y2="282" stroke="{t["border"]}"/>
<text x="60" y="318" font-family="{SANS}" font-size="17" fill="{t["body"]}">Seven years as Head Instructor, AI/ML executive program, UC Berkeley Exec Ed, 10,000+ leaders.</text>
<text x="60" y="342" font-family="{SANS}" font-size="17" fill="{t["muted"]}">3 US patents. MBA, Berkeley Haas. MS, IIT Roorkee. San Jose, CA.</text>
</svg>
'''


for name, t in THEMES.items():
    (OUT / f"about-{name}.svg").write_text(about(t))
    for slug, pub, lines, _url in ARTICLES:
        (OUT / f"{slug}-{name}.svg").write_text(article(pub, lines, t, f"{slug}-{name}"))
    (OUT / f"banner-{name}.svg").write_text(banner(t))
    for slug, *rest in CARDS:
        (OUT / f"{slug}-{name}.svg").write_text(card(slug, *rest, t))
print("Wrote", len(list(OUT.glob("*.svg"))), "SVGs")


def writing_row():
    """The README's Writing grid. GitHub shrinks images in a wide table instead of scrolling it,
    so tiles go three to a row: the newest six show, the rest sit in a collapsed list."""
    def tile(slug, pub, lines, url):
        alt = escape(" ".join(lines)) + f", on {pub}"
        return (f'<a href="{url}"><picture><source media="(prefers-color-scheme: dark)" srcset="cards/{slug}-dark.svg">'
                f'<img src="cards/{slug}-light.svg" width="32%" alt="{alt}"></picture></a>')
    def rows(items):
        return "\n\n".join("<p>\n" + "\n".join(tile(*a) for a in items[i:i+3]) + "\n</p>" for i in range(0, len(items), 3))
    shown, rest = ARTICLES[:6], ARTICLES[6:]
    out = rows(shown)
    if rest:
        out += f"\n\n<details><summary>{len(rest)} more articles</summary>\n\n" + rows(rest) + "\n\n</details>"
    return out

if __name__ == "__main__":
    (OUT / "writing-row.html").write_text(writing_row() + "\n")
