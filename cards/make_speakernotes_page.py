"""Product-page art for SpeakerNotes (applied-ai-agents/tools/speakernotes): a hero, feature panels with the
app's real screenshots, diagrams and an icon grid. Complements make_speakernotes.py (headers, cards, keycaps).

Screenshots are read from tools/speakernotes/docs/img (CI keeps them current) and embedded in the SVGs, so
rerun this after the screenshots change. Needs Pillow.
Run: python3 roy-vinay/roy-vinay/cards/make_speakernotes_page.py <applied-ai-agents clone>
"""
import base64
import io
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image

from masthead import SANS, SERIF, THEMES

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
ORANGE = "#FF8A3D"
INK, INK_BORDER, INK_TEXT, INK_BODY, INK_MUTED = "#18202C", "#2A3446", "#F0F3F6", "#C9D1D9", "#8B949E"


def embed(path, width):
    """A screenshot as a data URI, resized to `width` pixels (kept at 2x where the source allows)."""
    im = Image.open(path).convert("RGB")
    target = min(im.width, width * 2)
    if im.width != target:
        im = im.resize((target, round(im.height * target / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), im.width / im.height


def popover(path):
    """Just the popover from a screenshot of the notes window with a popover open (its near-black panel)."""
    im = Image.open(path).convert("RGB")
    px = im.load()
    xs, ys = [], []
    for y in range(im.height):
        for x in range(im.width // 3, im.width):
            r, g, b = px[x, y]
            if r < 24 and g < 24 and b < 24:
                xs.append(x)
                ys.append(y)
    box = (min(xs), min(ys) + 8, max(xs) + 1, max(ys) + 1)
    crop = im.crop(box)
    buf = io.BytesIO()
    crop.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), crop.width / crop.height


def text(x, y, s, size, fill, font=SANS, weight="400", anchor="start", spacing=None):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{ls}>{escape(s)}</text>')


def lines(x, y, rows, size, fill, gap, font=SANS, weight="400", anchor="start"):
    return "".join(text(x, y + i * gap, r, size, fill, font, weight, anchor) for i, r in enumerate(rows))


SHADOW = ('<filter id="sh" x="-10%" y="-10%" width="120%" height="130%">'
          '<feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000" flood-opacity="0.45"/></filter>')


def shot(uri, x, y, w, h, r=12, stroke="#3B4759"):
    clip = f"c{abs(hash((x, y, w, h))) % 10**8}"
    return (f'<defs><clipPath id="{clip}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath></defs>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#000" filter="url(#sh)"/>'
            f'<image href="{uri}" x="{x}" y="{y}" width="{w}" height="{h}" clip-path="url(#{clip})" preserveAspectRatio="xMidYMid slice"/>'
            f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="{r}" fill="none" stroke="{stroke}"/>')


def ink_frame(w, h, label, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
<defs>{SHADOW}<linearGradient id="glow" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1E2836"/><stop offset="1" stop-color="#141A23"/></linearGradient></defs>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="url(#glow)" stroke="{INK_BORDER}"/>
{body}
</svg>
'''


# ---------- hero: what you see, what your audience sees ----------

def hero(img):
    w, h = 1200, 600
    pw, ph = 532, 399
    you, _ = embed(img / "capture-visible.png", pw)
    them, _ = embed(img / "capture-hidden.png", pw)
    body = [
        text(48, 62, "WHAT YOU SEE", 13, ORANGE, weight="700", spacing="1.4"),
        text(48, 100, "Your notes, over your slides", 30, INK_TEXT, SERIF, "700"),
        text(620, 62, "WHAT YOUR AUDIENCE SEES", 13, ORANGE, weight="700", spacing="1.4"),
        text(620, 100, "Just your slides", 30, INK_TEXT, SERIF, "700"),
        shot(you, 48, 128, pw, ph),
        shot(them, 620, 128, pw, ph),
        # the "hidden" badge on the right panel
        f'<rect x="{620 + pw - 214}" y="146" width="196" height="34" rx="17" fill="#0D1117" opacity="0.85" stroke="{ORANGE}"/>',
        text(620 + pw - 116, 168, "Notes hidden from share", 14, ORANGE, weight="700", anchor="middle"),
        text(600, 568, "The same screen at the same moment. The notes window is left out of every screen share and recording.",
             16, INK_BODY, anchor="middle"),
    ]
    return ink_frame(w, h, "What you see: your notes over your slides. What your audience sees: just your slides. "
                           "The notes window is left out of every screen share and recording.", "".join(body))


# ---------- feature panels: copy on one side, the real app on the other ----------

def feature(img, kicker, title, body_rows, proof, shots, image_left=False):
    w, h = 1200, 440
    tx = 660 if image_left else 56
    parts = [
        text(tx, 92, kicker.upper(), 13, ORANGE, weight="700", spacing="1.4"),
        lines(tx, 140, title, 34, INK_TEXT, 42, SERIF, "700"),
        lines(tx, 140 + 42 * len(title) + 22, body_rows, 18, INK_BODY, 28),
        text(tx, 378, proof, 16, ORANGE, weight="700"),
    ]
    area_x = 56 if image_left else 620
    area_w, area_h = 524, 344
    if len(shots) == 1:
        uri, ratio = embed(img / shots[0], area_w)
        sw = min(area_w, area_h * ratio)
        sh = sw / ratio
        parts.append(shot(uri, area_x + (area_w - sw) / 2, 48 + (area_h - sh) / 2, sw, sh))
    else:
        # the main screenshot, with a second screenshot's popover floating over its corner
        a, ra = embed(img / shots[0], area_w)
        aw = 430
        ah = aw / ra
        ax = area_x + area_w - aw
        parts.append(shot(a, ax, 40, aw, ah))
        b, rb = popover(img / shots[1])
        bw = 250
        parts.append(shot(b, area_x, 40 + area_h - bw / rb, bw, bw / rb, r=10, stroke="#4A5568"))
    label = f"{' '.join(title)}. {' '.join(body_rows)} {proof}"
    return ink_frame(w, h, label, "".join(parts))


# ---------- diagrams (follow the light or dark theme) ----------

def arrow_defs(t):
    return (f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{t["accent"]}"/></marker></defs>')


def mini_screen(x, y, w, h, t, notes=True, cross=False):
    """A tiny slide with (or without) the dark notes window on it."""
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>',
         f'<rect x="{x + 12}" y="{y + 12}" width="{w * 0.5}" height="8" rx="4" fill="{t["ink"]}" opacity="0.85"/>']
    for i in range(3):
        cx = x + 22 + i * (w - 44) / 2
        s.append(f'<circle cx="{cx}" cy="{y + h * 0.62}" r="{h * 0.14}" fill="none" stroke="{t["accent"]}" stroke-width="2.5"/>')
    if notes:
        s.append(f'<rect x="{x + w * 0.52}" y="{y + h * 0.36}" width="{w * 0.42}" height="{h * 0.52}" rx="5" fill="#1C2533" stroke="#3B4759"/>')
        for j in range(3):
            s.append(f'<rect x="{x + w * 0.56}" y="{y + h * (0.46 + j * 0.12)}" width="{w * (0.3 - j * 0.06)}" height="4" rx="2" fill="{"#FFD25C" if j == 0 else "#8B949E"}"/>')
    if cross:
        cx, cy = x + w - 4, y + 4
        s.append(f'<circle cx="{cx}" cy="{cy}" r="13" fill="#D1242F"/><path d="M{cx - 5},{cy - 5} L{cx + 5},{cy + 5} M{cx + 5},{cy - 5} L{cx - 5},{cy + 5}" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>')
    return "".join(s)


def check(cx, cy, t):
    return (f'<circle cx="{cx}" cy="{cy}" r="13" fill="{t["accent"]}"/>'
            f'<path d="M{cx - 6},{cy} L{cx - 1.5},{cy + 5} L{cx + 6},{cy - 5}" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')


def problem(t):
    """Three ways to present from one laptop."""
    w, h = 1200, 250
    cols = [
        ("Share your whole screen", ["Everyone reads", "your notes"], True, "bad"),
        ("Share only the slides", ["Presenter View is gone;", "your notes vanish"], False, "bad"),
        ("SpeakerNotes", ["You see your notes;", "your audience doesn't"], True, "good"),
    ]
    parts = []
    for i, (head, desc, notes, kind) in enumerate(cols):
        x = i * 410
        good = kind == "good"
        parts.append(f'<rect x="{x + 0.5}" y="0.5" width="379" height="{h - 1}" rx="16" fill="{t["bg"]}" stroke="{t["accent"] if good else t["border"]}" stroke-width="{2 if good else 1}"/>')
        parts.append(mini_screen(x + 28, 28, 150, 96, t, notes=notes and not good or good, cross=False))
        if good:
            parts.append(mini_screen(x + 202, 28, 150, 96, t, notes=False))
            parts.append(text(x + 103, 146, "You", 12, t["muted"], weight="600", anchor="middle"))
            parts.append(text(x + 277, 146, "Your audience", 12, t["muted"], weight="600", anchor="middle"))
            parts.append(check(x + 352, 30, t))
        else:
            parts.append(f'<circle cx="{x + 178}" cy="30" r="13" fill="#D1242F"/><path d="M{x + 173},25 L{x + 183},35 M{x + 183},25 L{x + 173},35" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>')
        parts.append(text(x + 28, 184, head, 21, t["ink"], SERIF, "700"))
        parts.append(lines(x + 28, 212, desc, 16, t["body"], 22))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Share your whole screen: everyone reads your notes. Share only the slides: your notes vanish. SpeakerNotes: you see your notes, your audience doesn't.">
{"".join(parts)}
</svg>
'''


def share_flow(t):
    """Your screen → macOS screen capture → Zoom, Meet, recordings."""
    w, h = 1200, 270
    boxes = [
        (0, "Your screen", ["Slides, with the", "notes window on top"], True),
        (420, "macOS screen capture", ["The notes window is", "marked private"], None),
        (840, "Zoom, Meet, recordings", ["Your slides,", "without the notes"], False),
    ]
    parts = [arrow_defs(t)]
    for x, head, desc, notes in boxes:
        parts.append(f'<rect x="{x + 0.5}" y="0.5" width="359" height="{h - 1}" rx="16" fill="{t["bg"]}" stroke="{t["border"]}"/>')
        if notes is None:
            # a lock over a frame
            cx, cy = x + 180, 76
            parts.append(f'<rect x="{cx - 60}" y="{cy - 40}" width="120" height="80" rx="10" fill="none" stroke="{t["muted"]}" stroke-width="2" stroke-dasharray="6 5"/>')
            parts.append(f'<rect x="{cx - 16}" y="{cy - 4}" width="32" height="26" rx="5" fill="{t["accent"]}"/>'
                         f'<path d="M{cx - 9},{cy - 4} v-8 a9,9 0 0 1 18,0 v8" fill="none" stroke="{t["accent"]}" stroke-width="4"/>')
        else:
            parts.append(mini_screen(x + 105, 28, 150, 96, t, notes=notes))
        parts.append(text(x + 180, 176, head, 21, t["ink"], SERIF, "700", anchor="middle"))
        parts.append(lines(x + 180, 206, desc, 16, t["body"], 22, anchor="middle"))
    for x in (366, 786):
        parts.append(f'<line x1="{x}" y1="{h / 2}" x2="{x + 48}" y2="{h / 2}" stroke="{t["accent"]}" stroke-width="3" marker-end="url(#ar)"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Your screen shows slides with the notes window on top. macOS screen capture leaves the notes window out because it's marked private. Zoom, Meet and recordings get your slides without the notes.">
{"".join(parts)}
</svg>
'''


def follow_flow(t):
    """Two lanes: exact for Keynote and PowerPoint, reading the header for everything else."""
    w, h = 1200, 420
    parts = [arrow_defs(t)]

    def pill(x, y, wd, label, fill, color, mono=False):
        parts.append(f'<rect x="{x}" y="{y}" width="{wd}" height="44" rx="22" fill="{fill}" stroke="{t["border"]}"/>')
        parts.append(text(x + wd / 2, y + 28, label, 16 if not mono else 15, color, MONO if mono else SANS, "700" if not mono else "500", "middle"))

    def lane(y, tag, source, step, seen, notes):
        parts.append(f'<rect x="0.5" y="{y + 0.5}" width="{w - 1}" height="150" rx="16" fill="{t["bg"]}" stroke="{t["border"]}"/>')
        parts.append(text(28, y + 34, tag.upper(), 13, t["accent"], weight="700", spacing="1.4"))
        parts.append(text(28, y + 70, source, 22, t["ink"], SERIF, "700"))
        parts.append(text(28, y + 98, step, 15, t["body"]))
        pill(500, y + 52, 250, seen, t["track"], t["ink"])
        parts.append(f'<line x1="770" y1="{y + 74}" x2="830" y2="{y + 74}" stroke="{t["accent"]}" stroke-width="3" marker-end="url(#ar)"/>')
        pill(850, y + 52, 322, notes, "#1C2533", "#FFD25C", mono=True)
        parts.append(f'<line x1="420" y1="{y + 74}" x2="482" y2="{y + 74}" stroke="{t["accent"]}" stroke-width="3" marker-end="url(#ar)"/>')

    lane(0, "Exact", "Keynote and PowerPoint", "Asks the app which slide is up", "Slide 7", "## 7. Pricing")
    lane(170, "Reads the header", "Google Slides, Canva, PDFs", "Reads the slide's title on your Mac", "“The agent loop”", "## The agent loop")
    # two-way band
    y = 340
    parts.append(f'<rect x="0.5" y="{y + 0.5}" width="{w - 1}" height="79" rx="16" fill="#1C2533" stroke="#30363D"/>')
    parts.append(f'<path d="M40,{y + 32} h44 l-8,-7 M84,{y + 32} l-8,7 M84,{y + 50} h-44 l8,-7 M40,{y + 50} l8,7" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    parts.append(text(110, y + 36, "Two-way", 20, INK_TEXT, SERIF, "700"))
    parts.append(text(110, y + 60, "Move the notes with ⌃⌥→, and your slides move too. Press → in your slides, and the notes follow.", 16, INK_BODY))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Keynote and PowerPoint: exact, SpeakerNotes asks the app which slide is up, so slide 7 goes to the notes headed 7. Google Slides, Canva and PDFs: SpeakerNotes reads the slide's title on your Mac and finds the notes heading with that title. Two-way: move the notes and your slides move too.">
{"".join(parts)}
</svg>
'''


def icon(kind, cx, cy, t):
    a, m = t["accent"], t["muted"]
    if kind == "dock":
        return (f'<rect x="{cx - 44}" y="{cy + 6}" width="88" height="24" rx="8" fill="none" stroke="{m}" stroke-width="2.5"/>'
                + "".join(f'<rect x="{cx - 36 + i * 26}" y="{cy - 6 + (0 if i == 1 else 8)}" width="20" height="20" rx="5" fill="{a if i == 1 else m}" opacity="{1 if i == 1 else 0.5}"/>' for i in range(3))
                + f'<circle cx="{cx}" cy="{cy + 36}" r="3" fill="{a}"/>')
    if kind == "power":
        return (f'<path d="M{cx - 16},{cy - 14} a24,24 0 1 0 32,0" fill="none" stroke="{a}" stroke-width="4" stroke-linecap="round"/>'
                f'<line x1="{cx}" y1="{cy - 26}" x2="{cx}" y2="{cy + 2}" stroke="{a}" stroke-width="4" stroke-linecap="round"/>')
    if kind == "bookmark":
        return (f'<path d="M{cx - 20},{cy - 28} h40 v58 l-20,-14 l-20,14 z" fill="none" stroke="{a}" stroke-width="3.5" stroke-linejoin="round"/>'
                + text(cx, cy + 6, "7", 22, t["ink"], SERIF, "700", "middle"))
    if kind == "screens":
        return (f'<rect x="{cx - 38}" y="{cy - 18}" width="30" height="22" rx="3" fill="none" stroke="{m}" stroke-width="2.5" stroke-dasharray="4 3"/>'
                f'<rect x="{cx + 6}" y="{cy - 18}" width="32" height="24" rx="3" fill="none" stroke="{a}" stroke-width="3"/>'
                f'<path d="M{cx - 4},{cy - 7} h6 M{cx - 1},{cy - 11} l4,4 l-4,4" fill="none" stroke="{a}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<line x1="{cx + 22}" y1="{cy + 6}" x2="{cx + 22}" y2="{cy + 14}" stroke="{a}" stroke-width="3"/>'
                f'<line x1="{cx + 14}" y1="{cy + 16}" x2="{cx + 30}" y2="{cy + 16}" stroke="{a}" stroke-width="3" stroke-linecap="round"/>')
    return ""


def demo_grid(t):
    w, h = 1200, 250
    tiles = [
        ("dock", "One click away", ["A Dock icon that always", "brings the notes back"]),
        ("power", "Ready before the call", ["Open at Login starts it", "with your Mac"]),
        ("bookmark", "Back where you left it", ["Reopens on the same file", "and the same slide"]),
        ("screens", "Survives a projector", ["Moves back on screen if a", "display is unplugged"]),
    ]
    parts = []
    for i, (kind, head, desc) in enumerate(tiles):
        x = i * 305
        parts.append(f'<rect x="{x + 0.5}" y="0.5" width="284" height="{h - 1}" rx="16" fill="{t["bg"]}" stroke="{t["border"]}"/>')
        parts.append(f'<circle cx="{x + 142}" cy="74" r="50" fill="{t["track"]}"/>')
        parts.append(icon(kind, x + 142, 74, t))
        parts.append(text(x + 142, 166, head, 20, t["ink"], SERIF, "700", "middle"))
        parts.append(lines(x + 142, 194, desc, 15, t["body"], 21, anchor="middle"))
    label = ". ".join(f"{h_}: {' '.join(d)}" for _, h_, d in tiles)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
{"".join(parts)}
</svg>
'''


def terminal(cmd):
    w, h = 1200, 128
    body = ("".join(f'<circle cx="{30 + i * 22}" cy="28" r="7" fill="{c}"/>' for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]))
            + text(600, 33, "Terminal", 13, INK_MUTED, weight="600", anchor="middle")
            + f'<line x1="0" y1="52" x2="{w}" y2="52" stroke="{INK_BORDER}"/>'
            + text(30, 94, "$", 17, ORANGE, MONO, "700")
            + text(52, 94, cmd, 15.5, INK_TEXT, MONO))
    return ink_frame(w, h, f"In Terminal: {cmd}", body)


INSTALL = "curl -fsSL https://raw.githubusercontent.com/roy-vinay/applied-ai-agents/main/tools/speakernotes/install.sh | bash"


def main(root):
    root = Path(root)
    img = root / "tools" / "speakernotes" / "docs" / "img"
    out = root / ".github" / "assets"
    out.mkdir(parents=True, exist_ok=True)
    ink_svgs = {
        "speakernotes-feature-slides": feature(img, "Presenting", ["One slide at a time"],
            ["Write notes in Markdown with a line of ---", "between slides. Headings work too, so a Word",
             "or PDF script converts in a minute."], "⌃⌥→ and ⌃⌥← from any app.", ["app-present.png"]),
        "speakernotes-feature-read": feature(img, "Readability", ["Make it easy", "to read"],
            ["Size, typeface and spacing. Highlight what", "matters by hand, or ask: “highlight the",
             "parts of an agent.”"], "Your notes never leave your Mac.",
            ["app-emphasize.png", "app-text-settings.png"], image_left=True),
        "speakernotes-feature-voice": feature(img, "Scroll as I speak", ["Your notes keep", "pace with you"],
            ["Read naturally. What you've said dims and the", "line you're on stays in view. Code decides",
             "where you are, so an ad-lib can't throw it off."], "\u2303\u2325V. Your mic only, on your Mac.",
            ["app-voice.png"], image_left=True),
        **({"speakernotes-feature-parking": feature(img, "Question parking lot", ["Never lose an", "\u201cI'll come back to that\u201d"],
            ["\u2303\u2325P parks an audience question with its", "slide, from any app. On your last slide, the",
             "list comes back. Check off, or copy for follow-up."], "Prefilled from what you just said.",
            ["app-parking.png"])} if (img / "app-parking.png").exists() else {}),
        "speakernotes-feature-edit": feature(img, "Writing", ["Edit right in", "the window"],
            ["⌘E switches to editing, with headings and", "slide breaks colored. Edits save to your",
             "file, and edits elsewhere reload here."], "Or import a deck’s notes in one step.",
            ["app-edit.png"]),
    }
    for name, svg in ink_svgs.items():
        (out / f"{name}.svg").write_text(svg)
    for theme, t in THEMES.items():
        for name, fn in [("speakernotes-problem", problem), ("speakernotes-share-flow", share_flow),
                         ("speakernotes-follow-flow", follow_flow), ("speakernotes-demo-grid", demo_grid)]:
            (out / f"{name}-{theme}.svg").write_text(fn(t))
    print(f"Wrote SpeakerNotes page art to {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
