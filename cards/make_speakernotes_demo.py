"""The animated demo at the top of the SpeakerNotes page: you press → and the slide and the notes advance
together, while the right side shows what a full-screen share receives (the slides, never the notes).

Frames come from CI (tools/speakernotes/docs/img/demo/visible-N.png and hidden-N.png). Each frame is laid out
in HTML, rendered with Playwright, and the frames are saved as an animated GIF.
Needs Pillow and Python Playwright. Run: python3 make_speakernotes_demo.py <applied-ai-agents clone> [serif.woff2]
"""
import sys
import tempfile
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

W, H = 1200, 680
SLIDES = 3

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Serif; src: url("{serif}"); font-weight: 600 800; }}
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ background: transparent; }}
.card {{ width: {W}px; height: {H}px; border-radius: 20px; padding: 40px 44px 0; position: relative; overflow: hidden;
        background: linear-gradient(135deg, #1E2836, #121821); border: 1px solid #2A3446; font-family: Inter, sans-serif; }}
.cols {{ display: flex; gap: 40px; }}
.col {{ width: 536px; }}
.kick {{ color: #FF8A3D; font: 700 13px Inter; letter-spacing: 1.4px; text-transform: uppercase; }}
.title {{ color: #F0F3F6; font: 700 29px Serif, Georgia, serif; margin: 8px 0 22px; letter-spacing: -0.3px; }}
.screen {{ position: relative; width: 536px; height: 402px; border-radius: 12px; overflow: hidden;
          box-shadow: 0 16px 40px rgba(0,0,0,.5); outline: 1px solid #3B4759; }}
.screen img {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.pill {{ position: absolute; display: flex; align-items: center; gap: 8px; padding: 7px 13px; border-radius: 999px;
        font: 700 13px Inter; background: rgba(13,17,23,.88); color: #F0F3F6; border: 1px solid #3B4759; }}
.dot {{ width: 9px; height: 9px; border-radius: 50%; background: #F85149; box-shadow: 0 0 0 3px rgba(248,81,73,.25); }}
.hidden {{ color: #FF8A3D; border-color: #FF8A3D; }}
.under {{ height: 74px; display: flex; align-items: center; justify-content: center; gap: 10px; }}
.key {{ transform: scale({key_scale}); opacity: {key_opacity}; transition: none;
       display: flex; align-items: center; gap: 12px; padding: 10px 16px 10px 10px; border-radius: 14px;
       background: rgba(13,17,23,.9); border: 1px solid #FF8A3D; color: #F0F3F6; font: 600 15px Inter; }}
.cap {{ width: 46px; height: 42px; border-radius: 9px; display: grid; place-items: center; font: 700 22px Inter;
       background: #FF8A3D; color: #18202C; box-shadow: 0 3px 0 #B4561C; }}
.foot {{ position: absolute; left: 0; right: 0; bottom: 26px; text-align: center; color: #C9D1D9; font: 400 16px Inter; }}
.foot b {{ color: #F0F3F6; font-weight: 600; }}
</style></head><body>
<div class="card">
  <div class="cols">
    <div class="col">
      <div class="kick">What you see</div>
      <div class="title">Move your slides. Your notes follow.</div>
      <div class="screen">
        <img src="{you_a}" style="opacity:{a}"><img src="{you_b}" style="opacity:{b}">
      </div>
      <div class="under"><div class="key"><div class="cap">→</div>You press Next</div></div>
    </div>
    <div class="col">
      <div class="kick">What your audience sees</div>
      <div class="title">Your entire screen, minus your notes</div>
      <div class="screen">
        <img src="{them_a}" style="opacity:{a}"><img src="{them_b}" style="opacity:{b}">
      </div>
      <div class="under"><div class="pill" style="position:static"><span class="dot"></span>Sharing entire screen</div>
        <div class="pill hidden" style="position:static">Notes hidden</div></div>
    </div>
  </div>
  <div class="foot">Captured on one Mac: <b>left</b> is your display, <b>right</b> is what a full-screen share or recording receives.</div>
</div>
</body></html>"""


def main(root, serif=None):
    root = Path(root)
    demo = root / "tools" / "speakernotes" / "docs" / "img" / "demo"
    out = root / ".github" / "assets" / "speakernotes-demo.gif"
    serif_url = Path(serif).resolve().as_uri() if serif else ""
    you = [(demo / f"visible-{i}.png").resolve().as_uri() for i in range(1, SLIDES + 1)]
    them = [(demo / f"hidden-{i}.png").resolve().as_uri() for i in range(1, SLIDES + 1)]

    # (from slide, to slide, blend 0..1, key shown, duration ms)
    script = []
    for i in range(SLIDES):
        j = (i + 1) % SLIDES
        script.append((i, i, 0.0, 0.0, 1900))          # hold on this slide
        script.append((i, i, 0.0, 1.0, 420))           # press →
        for k in (1, 2):                                # slide and notes change together
            script.append((i, j, k / 3, 1.0, 45))
        script.append((j, j, 0.0, 0.0, 0))              # (merged into the next hold)

    script = [s for s in script if s[4] > 0]
    frames, durations = [], []
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        html = Path(tmp) / "frame.html"
        for n, (i, j, t, key, ms) in enumerate(script):
            html.write_text(PAGE.format(W=W, H=H, serif=serif_url, you_a=you[i], you_b=you[j], them_a=them[i],
                                        them_b=them[j], a=1 - t, b=t, key_opacity=key,
                                        key_scale=1.0 if key else 0.9))
            page.goto(html.as_uri())
            page.wait_for_timeout(120 if n else 600)
            path = Path(tmp) / f"f{n:03}.png"
            page.locator(".card").screenshot(path=str(path), omit_background=True)
            rgba = Image.open(path).convert("RGBA")
            # 256 colors a frame keeps the file small; the screenshots are mostly flat color.
            alpha = rgba.getchannel("A")
            q = rgba.convert("RGB").quantize(255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
            q.paste(255, mask=alpha.point(lambda v: 255 if v < 128 else 0))
            q.info["transparency"] = 255
            frames.append(q)
            durations.append(ms)
        browser.close()
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=durations, loop=0,
                   disposal=2, transparency=255, optimize=False)
    print(f"Wrote {out} ({out.stat().st_size // 1024} KB, {len(frames)} frames)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".", sys.argv[2] if len(sys.argv) > 2 else None)
