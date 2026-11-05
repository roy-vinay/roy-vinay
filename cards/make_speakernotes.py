"""Art for the SpeakerNotes page (applied-ai-agents/tools/speakernotes), in the profile's newspaper style.

Buttons, section headers, an at-a-glance grid, decision cards, a keycap sheet and a status strip, each as
light and dark SVGs. Run: python3 roy-vinay/roy-vinay/cards/make_speakernotes.py <applied-ai-agents clone>
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from make_cards import card
from masthead import SANS, SERIF, THEMES

ORANGE = "#FF8A3D"


def ink(t):
    """Dark ink tiles in both themes, like the profile's cards."""
    dark = t["bg"] != "#FFFFFF"
    return ("#1C2533", "#30363D", "#2A3446") if dark else ("#18202C", "#18202C", "#222C3B")


def button(slug, kicker, title, lines, cta, t):
    # Same as the Brand Review buttons: an ink card with an orange outline and a call to action.
    w, h = 480, 210
    tile, _, ghost = ink(t)
    body = "".join(f'<text x="28" y="{122 + i * 25}" font-family="{SANS}" font-size="17" fill="#C9D1D9">{escape(l)}</text>'
                   for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}: {escape(" ".join(lines))} {escape(cta)}">
<defs><clipPath id="c-{slug}"><rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="14"/></clipPath></defs>
<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="14" fill="{tile}" stroke="{ORANGE}" stroke-width="3"/>
<g clip-path="url(#c-{slug})"><text x="{w + 6}" y="{h + 52}" text-anchor="end" font-family="{SERIF}" font-size="220" font-weight="700" fill="{ghost}">{escape(title[0])}</text></g>
<text x="28" y="40" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="1.2" fill="{ORANGE}">{escape(kicker.upper())}</text>
<text x="28" y="82" font-family="{SERIF}" font-size="29" font-weight="700" fill="#F0F3F6">{escape(title)}</text>
{body}
<text x="28" y="186" font-family="{SANS}" font-size="15" font-weight="700" fill="{ORANGE}">{escape(cta)}  →</text>
</svg>
'''


def section(kicker, title, t):
    """A section header: kicker, serif headline, and the masthead's double rule."""
    w, h = 1200, 96
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<text x="0" y="22" font-family="{SANS}" font-size="14" font-weight="700" letter-spacing="1.4" fill="{t["accent"]}">{escape(kicker.upper())}</text>
<text x="0" y="68" font-family="{SERIF}" font-size="40" font-weight="700" letter-spacing="-0.5" fill="{t["ink"]}">{escape(title)}</text>
<line x1="0" y1="86" x2="{w}" y2="86" stroke="{t["ink"]}"/>
<line x1="0" y1="90" x2="{w}" y2="90" stroke="{t["ink"]}"/>
</svg>
'''


def strip(label, cols, t):
    """Four short newspaper columns, like the masthead's, on their own."""
    w, h = 1200, 96
    parts = []
    for i, (head, lines) in enumerate(cols):
        x = i * 306
        if i:
            parts.append(f'<line x1="{x - 20}" y1="6" x2="{x - 20}" y2="80" stroke="{t["border"]}"/>')
        parts.append(f'<text x="{x}" y="20" font-family="{SANS}" font-size="14" font-weight="700" fill="{t["accent"]}">{escape(head)}</text>')
        for j, l in enumerate(lines):
            parts.append(f'<text x="{x}" y="{46 + j * 24}" font-family="{SERIF}" font-size="19" font-weight="700" fill="{t["ink"]}">{escape(l)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
{"".join(parts)}
</svg>
'''


def keycaps(groups, t):
    """A shortcut sheet: keycaps on an ink card, in two columns."""
    w = 1200
    rows = max(len(items) for _, items in groups)
    h = 92 + rows * 58 + 14
    tile, border, _ = ink(t)
    parts = []
    label = []
    for g, (heading, items) in enumerate(groups):
        x0 = 36 + g * 588
        parts.append(f'<text x="{x0}" y="50" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="1.2" fill="{ORANGE}">{escape(heading.upper())}</text>')
        for r, (keys, desc) in enumerate(items):
            y = 82 + r * 58
            x = x0
            for k in keys:
                kw = max(50, 24 + 15 * len(k))
                parts.append(f'<rect x="{x}" y="{y}" width="{kw}" height="38" rx="8" fill="#26303F" stroke="#3B4759"/>'
                             f'<rect x="{x}" y="{y + 32}" width="{kw}" height="6" rx="3" fill="#141B25" opacity="0.6"/>'
                             f'<text x="{x + kw / 2}" y="{y + 25}" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="600" fill="#F0F3F6">{escape(k)}</text>')
                x += kw + 8
            parts.append(f'<text x="{max(x + 10, x0 + 200)}" y="{y + 25}" font-family="{SANS}" font-size="17" fill="#C9D1D9">{escape(desc)}</text>')
            label.append(f"{' '.join(keys)}: {desc}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Shortcuts. {escape('. '.join(label))}">
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{tile}" stroke="{border}"/>
<line x1="600" y1="34" x2="600" y2="{h - 24}" stroke="#30363D"/>
{"".join(parts)}
</svg>
'''


BUTTONS = [
    ("btn-speakernotes-download", "Start here", "Download for Mac",
     ["Free for macOS 13 and later, Apple silicon", "and Intel. Early build, MIT."], "Get SpeakerNotes-macOS.zip"),
    ("btn-speakernotes-install", "Or in Terminal", "One-line install",
     ["Paste one command. Run it again any time", "to update; notes and settings are kept."], "See the command"),
]

SECTIONS = [
    ("problem", "The problem", "Your notes, or your audience's view"),
    ("glance", "At a glance", "What it does"),
    ("share", "Private by design", "How it stays out of your share"),
    ("follow", "On-device intelligence", "Follows your slides"),
    ("demo", "Reliability", "Built for a live demo"),
    ("decisions", "Design", "Decisions and trade-offs"),
    ("shortcuts", "Keyboard", "Shortcuts"),
    ("status", "Quality", "Status"),
    ("install", "Get it", "Install and build"),
]

GLANCE = [
    ("glance-private", "At a glance", "Hidden, even full screen",
     ["Share your entire screen or desktop, and", "your audience still sees only your slides.", "You see your notes; they never do."],
     "Checked in CI on every change."),
    ("glance-slides", "At a glance", "Follows your slides",
     ["Move your slides, and the notes move with", "you: Keynote, PowerPoint, Google Slides or", "anything else. It works the other way too."],
     "No extra clicks while you present."),
    ("glance-readable", "At a glance", "Easy to read",
     ["Size, typeface and spacing. Highlight what", "matters, by hand or by describing it to", "Apple's on-device model."],
     "Your notes never leave your Mac."),
    ("glance-demo", "At a glance", "Demo-safe",
     ["Dock icon, Open at Login, reopens on the", "same slide, and moves back on screen if a", "projector is unplugged."],
     "Never steals focus from your slides."),
]

DECISIONS = [
    ("decision-hide", "Decision", "Hide, don't detect",
     ["macOS has no public way to know a share", "started, so the notes are always private", "to capture. Nothing to remember."],
     "Always on, not switched on by a guess."),
    ("decision-model", "Decision", "The model finds, code decides",
     ["Instructions return phrases. A phrase is", "kept only if it appears word for word in", "your notes."],
     "A made-up phrase can't be emphasized."),
    ("decision-file", "Decision", "Emphasis beside the file",
     ["Highlights are saved next to each notes", "file, not inside it, so the file stays", "exactly as you wrote it."],
     "Still works in any editor and in git."),
    ("decision-permissions", "Decision", "Exact first, then read",
     ["When Keynote or PowerPoint can say which", "slide is up, ask them. Read the screen only", "for apps that can't, and only when sure."],
     "Near-exact titles move it at once."),
]

SHORTCUTS = [
    ("From any app", [
        (["⌃⌥→", "⌃⌥←"], "Next or previous slide"),
        (["⌃⌥Space"], "Start or stop auto-scroll"),
        (["⌃⌥↑", "⌃⌥↓"], "Scroll faster or slower"),
        (["⌃⌥T"], "Click-through on or off"),
        (["⌃⌥F"], "Follow my slides on or off"),
        (["⌃⌥V"], "Scroll as I speak on or off"),
        (["⌃⌥P"], "Park an audience question"),
    ]),
    ("In the notes", [
        (["→", "←", "Space"], "Next or previous slide"),
        (["⌘O", "⌘S"], "Open a file, save"),
        (["⌘E"], "Edit or present"),
        (["⌘T", "⌘+", "⌘−"], "Text settings and size"),
        (["⌘]", "⌘["], "Less or more see-through"),
    ]),
]

STATUS = ("Status: 32 tests, Apple silicon and Intel builds, screen-capture and slide-reading checks, instructions not tested in CI.", [
    ("Tests", ["32 tests: parsing, slide", "and speech matching"]),
    ("Builds", ["Apple silicon and Intel,", "opens on macOS 13"]),
    ("Checked in CI", ["Hidden from capture,", "reading a slide's title"]),
    ("Not yet", ["Instructions untested", "in CI (no Apple AI)"]),
])


def main(root):
    out = Path(root) / ".github" / "assets"
    out.mkdir(parents=True, exist_ok=True)
    for theme, t in THEMES.items():
        def write(name, svg):
            (out / f"{name}-{theme}.svg").write_text(svg)
        for slug, *args in BUTTONS:
            write(slug, button(f"{slug}-{theme}", *args, t))
        for key, kicker, title in SECTIONS:
            write(f"speakernotes-sec-{key}", section(kicker, title, t))
        for slug, *args in GLANCE + DECISIONS:
            write(f"speakernotes-{slug}", card(f"speakernotes-{slug}-{theme}", *args, t))
        write("speakernotes-shortcuts", keycaps(SHORTCUTS, t))
        write("speakernotes-status", strip(*STATUS, t))
    print(f"Wrote SpeakerNotes art to {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
