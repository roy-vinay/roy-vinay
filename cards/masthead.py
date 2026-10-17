"""The newspaper masthead used at the top of the profile and every project page.

One function, so every page shares the same proportions: a dateline strip, the title as nameplate,
a double rule, and four short columns. Column text is wrapped by hand (two lines, about 27 characters).
"""
from xml.sax.saxutils import escape

SERIF = "Georgia, 'Times New Roman', serif"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

THEMES = {
    "light": dict(bg="#FFFFFF", border="#D0D7DE", ink="#1F2328", body="#424A53", muted="#59636E",
                  accent="#C2410C", track="#EAEEF2"),
    "dark": dict(bg="#161B22", border="#30363D", ink="#E6EDF3", body="#C9D1D9", muted="#9198A1",
                 accent="#FF8A3D", track="#262C36"),
}


def masthead(t, title, left, center, right, cols, label):
    """No card around it, so it sits flush with the README text below."""
    w, h = 1200, 236
    size = 80 if len(title) <= 16 else 64 if len(title) <= 24 else 58
    parts = []
    for i, (head, lines) in enumerate(cols):
        x = i * 306
        if i:
            parts.append(f'<line x1="{x - 20}" y1="160" x2="{x - 20}" y2="228" stroke="{t["border"]}"/>')
        parts.append(f'<text x="{x}" y="174" font-family="{SANS}" font-size="14" font-weight="700" fill="{t["accent"]}">{escape(head)}</text>')
        for j, l in enumerate(lines):
            parts.append(f'<text x="{x}" y="{199 + j * 24}" font-family="{SERIF}" font-size="19" font-weight="700" fill="{t["ink"]}">{escape(l)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
<text x="0" y="18" font-family="{SANS}" font-size="16" fill="{t["muted"]}">{escape(left)}</text>
<text x="600" y="18" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="600" fill="{t["ink"]}">{escape(center)}</text>
<text x="1200" y="18" text-anchor="end" font-family="{SANS}" font-size="16" fill="{t["muted"]}">{escape(right)}</text>
<line x1="0" y1="32" x2="1200" y2="32" stroke="{t["ink"]}"/>
<text x="600" y="{88 + size * 0.35:.0f}" text-anchor="middle" font-family="{SERIF}" font-size="{size}" font-weight="700" letter-spacing="-1.5" fill="{t["ink"]}">{escape(title)}</text>
<line x1="0" y1="138" x2="1200" y2="138" stroke="{t["ink"]}"/>
<line x1="0" y1="142" x2="1200" y2="142" stroke="{t["ink"]}"/>
{"".join(parts)}
</svg>
'''
