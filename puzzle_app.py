import base64
import io
import json
from pathlib import Path

import streamlit as st
from PIL import Image

st.set_page_config(page_title="Blululi Puzzle Studio", page_icon="🧩", layout="wide")

st.markdown(
    """
    <style>
      [data-testid="stHeader"],
      [data-testid="stToolbar"],
      #MainMenu,
      footer,
      [data-testid="stStatusWidget"],
      [data-testid="stDecoration"] {
        visibility: hidden !important;
        display: none !important;
        height: 0 !important;
      }

      html, body, .stApp, [data-testid="stAppViewContainer"] {
        margin: 0 !important;
        padding: 0 !important;
        background: #eef2ff !important;
      }

      .block-container,
      [data-testid="stAppViewBlockContainer"],
      .main .block-container {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
      }

      iframe {
        border: 0 !important;
        display: block !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

IMAGE_FOLDER = Path("images")

if not IMAGE_FOLDER.exists() or not IMAGE_FOLDER.is_dir():
    st.error("Folder ./images not found")
    st.stop()

image_paths = sorted(
    p for p in IMAGE_FOLDER.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
)

if not image_paths:
    st.error("No images found inside ./images")
    st.stop()

IMAGE_TITLES = {
    "01_web_rectangula_frame2": "Mandala Frame Pattern I",
    "02_web_IMG_2815": "Colorful Mandala on Pure Purple Background",
    "web_beige_green_plain_colors": "Beige & Green Mandala Balance",
    "web_blue_green_pink_plain_colors": "Blue Green Pink Mandala Harmony",
    "web_green_yellow_purple": "Green Yellow Purple Mandala Energy",
    "web_green_yellow_purple_plain_colors": "Green Yellow Purple Mandala Spectrum",
    "web_intricate_rectangular": "Intricate Mandala Geometry",
    "web_multicolor": "Multicolor Mandala Radiance",
    "web_multicolor_metallic": "Metallic Multicolor Mandala Glow",
    "web_orange_yellow": "Orange Yellow Mandala Sunrise",
    "web_purple": "Purple Mandala Serenity",
    "web_purple_yellow_red": "Purple Yellow Red Mandala Fire",
    "web_rectangular_frame": "Mandala Frame Pattern II",
    "web_rectangular_frame3": "Mandala Frame Pattern III",
}

PRODUCTS = [
    "https://blululi.com/products/colorful-mandala-tote-bag-vibrant-boho-all-over-print-beach-market-tote",
    "https://blululi.com/collections/wall-art/products/mandala-art-drawn-by-hand-vertical-framed-poster-mindfulness-yoga-purple-mandala",
    "https://blululi.com/collections/t-shirts/products/rainbow-mandala-womens-t-shirt-colorful-art-1",
    "https://blululi.com/collections/t-shirts/products/colorful-mandala-geometric-t-shirt",
    "https://blululi.com/collections/t-shirts/products/vibrant-mandala-tee-intricate-art-design",
    "https://blululi.com/products/vibrant-mandala-tee-colorful-intricate-2",
    "https://blululi.com/products/spun-polyester-square-pillowcase-mandala-art-original-fine-art-hand-drawn-dark-charcoal-blue-1",
    "https://blululi.com/collections/t-shirts/products/rainbow-mandala-womens-t-shirt-colorful-art",
    "https://blululi.com/products/rainbow-mandala-womens-short-sleeve-t-shirt-2",
    "https://blululi.com/collections/t-shirts/products/intricate-mandala-t-shirt-colorful-geometric-design",
    "https://blululi.com/collections/t-shirts/products/rainbow-mandala-womens-t-shirt-colorful-intricate-1",
    "https://blululi.com/products/one-shoulder-dress-with-hand-drawn-mandala-design-black-with-orange-red-and-gold-accents",
    "https://blululi.com/collections/kitchen-decor/products/mandala-art-15oz-ceramic-mug-perfect-for-coffee-tea-lovers-2",
    "https://blululi.com/products/colorful-mandala-tote-bag-boho-psychedelic-all-over-print",
]


def _to_data_uri(path: Path, max_dim: int = 1800, quality: int = 92) -> dict:
    with Image.open(path) as src:
        width, height = src.size
        img = src.convert("RGB")
        img.thumbnail((max_dim, max_dim))
        out_width, out_height = img.size
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)

    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    name = IMAGE_TITLES.get(path.stem, path.stem.replace("_", " ").replace("-", " ").title())
    return {
        "name": name,
        "url": f"data:image/jpeg;base64,{encoded}",
        "width": out_width,
        "height": out_height,
        "ratio": round(out_width / out_height, 6) if out_height else 1,
    }


assets = [_to_data_uri(p) for p in image_paths]
assets_json = json.dumps(assets)
products_json = json.dumps(PRODUCTS)

components_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>Blululi Puzzle Studio</title>
<style>
  :root {{
    --bg: #eef2ff;
    --bg2: #f8faff;
    --panel: rgba(255,255,255,.78);
    --panel-strong: rgba(255,255,255,.90);
    --line: rgba(79,70,229,.11);
    --text: #0f172a;
    --muted: #64748b;
    --accent: #6d28d9;
    --accent2: #8b5cf6;
    --success: #16a34a;
    --shadow: 0 18px 50px rgba(15,23,42,.10);
    --shadow-soft: 0 10px 30px rgba(15,23,42,.08);
    --radius-xl: 30px;
    --radius-lg: 22px;
    --radius-md: 16px;
    --safe-top: env(safe-area-inset-top, 0px);
    --safe-bottom: env(safe-area-inset-bottom, 0px);
  }}

  * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}

  html, body {{
    margin: 0;
    min-height: 100%;
    color: var(--text);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background:
      radial-gradient(circle at top left, rgba(109,40,217,.12), transparent 28%),
      radial-gradient(circle at top right, rgba(34,197,94,.08), transparent 20%),
      linear-gradient(180deg, #f8faff 0%, #eef2ff 100%);
    overflow-x: hidden;
  }}

  body {{
    padding: 12px 12px calc(12px + var(--safe-bottom));
  }}

  .app {{
    width: min(1440px, 100%);
    margin: 0 auto;
    border-radius: var(--radius-xl);
    overflow: hidden;
    background: linear-gradient(180deg, rgba(255,255,255,.74), rgba(255,255,255,.58));
    border: 1px solid rgba(255,255,255,.7);
    box-shadow: var(--shadow);
    backdrop-filter: blur(20px);
  }}

  .topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: calc(14px + var(--safe-top)) 20px 14px;
    border-bottom: 1px solid var(--line);
    background: linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.70));
  }}

  .brand {{ display: flex; align-items: center; gap: 12px; }}
  .logo {{
    width: 42px; height: 42px; border-radius: 14px;
    display: grid; place-items: center; color: white; font-size: 1.2rem;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    box-shadow: 0 12px 24px rgba(109,40,217,.25);
  }}
  .brand-copy {{ display: grid; gap: 2px; }}
  .brand-title {{ font-weight: 900; letter-spacing: .01em; }}
  .brand-sub {{ color: var(--muted); font-size: .9rem; }}

  .shell {{
    display: grid;
    grid-template-columns: 360px minmax(0, 1fr);
    gap: 18px;
    padding: 18px;
  }}

  .sidebar {{ display: grid; gap: 14px; align-content: start; }}
  .card {{
    border-radius: var(--radius-lg);
    background: var(--panel);
    border: 1px solid rgba(255,255,255,.74);
    box-shadow: var(--shadow-soft);
    backdrop-filter: blur(14px);
  }}
  .pad {{ padding: 18px; }}

  .hero {{
    padding: 20px;
    background:
      radial-gradient(circle at top right, rgba(139,92,246,.20), transparent 28%),
      linear-gradient(180deg, rgba(255,255,255,.94), rgba(255,255,255,.70));
  }}
  .eyebrow {{
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 12px; border-radius: 999px;
    background: rgba(109,40,217,.08); color: var(--accent);
    font-size: .76rem; font-weight: 900; letter-spacing: .12em; text-transform: uppercase;
    margin-bottom: 14px;
  }}
  .headline {{
    margin: 0 0 10px; font-weight: 950; letter-spacing: -.03em;
    line-height: 1.02; font-size: clamp(1.7rem, 3vw, 2.8rem);
  }}
  .sub {{ margin: 0; color: var(--muted); line-height: 1.6; font-size: 1rem; }}

  .controls {{ display: grid; gap: 14px; }}
  .control {{ display: grid; gap: 8px; }}
  .label {{
    font-size: .78rem; text-transform: uppercase; letter-spacing: .1em;
    color: var(--muted); font-weight: 900;
  }}
  .helper {{ color: var(--muted); font-size: .9rem; line-height: 1.5; }}

  select, input[type="range"] {{ width: 100%; }}
  select {{
    appearance: none; border: 1px solid rgba(15,23,42,.08); border-radius: 16px;
    background: rgba(255,255,255,.98); color: var(--text);
    padding: 14px 15px; font-size: .98rem; outline: none;
  }}
  input[type="range"] {{ accent-color: var(--accent); }}

  .range-wrap {{ display: grid; gap: 8px; }}
  .range-row {{ display: flex; align-items: center; gap: 12px; }}
  .range-value {{
    min-width: 86px; text-align: center; padding: 10px 12px;
    border-radius: 14px; background: rgba(255,255,255,.96);
    border: 1px solid rgba(15,23,42,.08); font-weight: 900;
  }}
  .difficulty-copy {{ display: flex; justify-content: space-between; gap: 8px; color: var(--muted); font-size: .84rem; }}

  .btn-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  button, .cta-link {{
    appearance: none; border: 0; border-radius: 16px; padding: 13px 16px;
    font-size: .96rem; font-weight: 900; cursor: pointer; text-decoration: none;
    display: inline-flex; align-items: center; justify-content: center; gap: 8px;
    transition: transform .16s ease, box-shadow .16s ease, opacity .16s ease;
  }}
  button:hover, .cta-link:hover {{ transform: translateY(-1px); }}
  .btn-primary {{ color: white; background: linear-gradient(135deg, var(--accent), var(--accent2)); box-shadow: 0 14px 24px rgba(109,40,217,.22); }}
  .btn-secondary {{ color: var(--text); background: rgba(255,255,255,.98); border: 1px solid rgba(15,23,42,.08); }}
  .btn-success {{ color: white; background: linear-gradient(135deg, #16a34a, #22c55e); box-shadow: 0 14px 24px rgba(34,197,94,.20); }}

  .preview-wrap {{ display: grid; gap: 12px; }}
  .preview {{
    width: 100%;
    border-radius: 22px;
    overflow: hidden;
    background: rgba(255,255,255,.95);
    border: 1px solid rgba(15,23,42,.07);
    position: relative;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.8);
  }}
  .preview-frame {{ width: 100%; aspect-ratio: var(--preview-ratio, 1 / 1); position: relative; }}
  .preview img {{ width: 100%; height: 100%; object-fit: contain; display: block; background: linear-gradient(180deg, #fff, #f8fafc); }}
  .preview-badge {{
    position: absolute; left: 12px; right: 12px; bottom: 12px;
    padding: 12px 14px; border-radius: 16px; background: rgba(15,23,42,.60);
    color: white; font-size: .86rem; font-weight: 800; backdrop-filter: blur(8px);
    display: flex; justify-content: space-between; gap: 10px;
  }}

  .mini-item {{
    border-radius: 16px; padding: 12px 14px; border: 1px solid rgba(15,23,42,.06);
    background: rgba(255,255,255,.82); display: flex; align-items: flex-start; gap: 10px;
  }}
  .mini-icon {{ width: 32px; height: 32px; border-radius: 12px; display: grid; place-items: center; background: rgba(109,40,217,.08); flex: 0 0 auto; }}
  .mini-copy strong {{ display: block; margin-bottom: 3px; }}
  .mini-copy span {{ color: var(--muted); font-size: .9rem; line-height: 1.45; }}

  .board-pane {{ min-width: 0; position: relative; }}
  .board-card {{
    padding: 16px;
    border-radius: 28px;
    background:
      radial-gradient(circle at top left, rgba(255,255,255,.98), transparent 18%),
      radial-gradient(circle at bottom right, rgba(139,92,246,.09), transparent 18%),
      linear-gradient(180deg, rgba(255,255,255,.80), rgba(255,255,255,.58));
    border: 1px solid rgba(255,255,255,.72);
  }}

  .board-head {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; margin-bottom: 14px; }}
  .board-title {{ font-size: 1.12rem; font-weight: 950; letter-spacing: -.01em; }}
  .board-note {{ color: var(--muted); font-size: .94rem; margin-top: 4px; }}
  .streak-pill {{
    border-radius: 999px; padding: 10px 14px; background: rgba(255,255,255,.92);
    border: 1px solid rgba(15,23,42,.08); font-size: .85rem; font-weight: 900; white-space: nowrap;
  }}

  .game-stage {{ position: relative; }}
  .board-shell {{
    width: min(100%, 980px);
    margin: 0 auto;
    display: flex; align-items: center; justify-content: center;
    min-height: 420px;
  }}
  #board {{
    width: min(100%, 940px);
    aspect-ratio: var(--board-ratio, 1 / 1);
    display: grid;
    grid-template-columns: repeat(var(--grid-size, 4), 1fr);
    gap: 2px;
    padding: 4px;
    background: rgba(255,255,255,.97);
    border: 1px solid rgba(109,40,217,.10);
    border-radius: 24px;
    overflow: hidden;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.94), 0 18px 36px rgba(15,23,42,.06);
    user-select: none;
    touch-action: manipulation;
  }}

  .tile {{
    position: relative;
    border: 0; outline: 0; width: 100%; height: 100%;
    border-radius: 6px;
    background-repeat: no-repeat;
    background-color: rgba(255,255,255,.72);
    cursor: grab;
    overflow: hidden;
    transition: transform .13s ease, box-shadow .13s ease, opacity .13s ease, filter .13s ease;
  }}
  .tile:hover {{ box-shadow: 0 8px 16px rgba(15,23,42,.12); filter: saturate(1.04); }}
  .tile.dragging {{ opacity: .74; cursor: grabbing; transform: scale(.985); }}
  .tile.selected {{ box-shadow: inset 0 0 0 3px rgba(109,40,217,.98); }}
  .tile.solved {{ cursor: default; }}

  .status-row {{ margin-top: 14px; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }}
  .status-card {{ border-radius: 18px; padding: 14px; background: rgba(255,255,255,.88); border: 1px solid rgba(15,23,42,.06); }}
  .status-label {{ font-size: .74rem; text-transform: uppercase; letter-spacing: .09em; color: var(--muted); font-weight: 800; margin-bottom: 6px; }}
  .status-value {{ font-size: 1.04rem; font-weight: 950; }}
  .focus-tip {{ margin-top: 14px; text-align: center; color: var(--muted); font-size: .93rem; }}

  .overlay {{
    position: absolute; inset: 0; display: none; align-items: center; justify-content: center;
    background: rgba(15,23,42,.56); backdrop-filter: blur(8px); padding: 20px; z-index: 20;
  }}
  .overlay.show {{ display: flex; }}
  .overlay-box {{
    width: min(640px, 94%); background: rgba(255,255,255,.99); border-radius: 28px; padding: 26px;
    text-align: center; box-shadow: 0 30px 60px rgba(0,0,0,.18); border: 1px solid rgba(255,255,255,.88);
  }}
  .overlay-badge {{
    display: inline-flex; padding: 8px 12px; border-radius: 999px; background: rgba(34,197,94,.10);
    color: #15803d; font-size: .78rem; font-weight: 900; text-transform: uppercase; letter-spacing: .1em; margin-bottom: 14px;
  }}
  .overlay-title {{ margin: 0 0 10px; font-size: 1.8rem; font-weight: 950; letter-spacing: -.03em; }}
  .overlay-copy {{ margin: 0 0 16px; color: var(--muted); line-height: 1.6; font-size: 1rem; }}
  .overlay-image-wrap {{
    width: min(100%, 360px); margin: 0 auto 18px; aspect-ratio: var(--overlay-ratio, 1 / 1);
    border-radius: 20px; overflow: hidden; box-shadow: 0 18px 30px rgba(15,23,42,.14); background: #fff;
  }}
  .overlay-image {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
  .overlay-stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 18px; }}
  .overlay-stat {{ border-radius: 18px; padding: 12px; background: #f8fafc; border: 1px solid rgba(15,23,42,.06); }}
  .overlay-stat small {{ display: block; color: var(--muted); font-weight: 800; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 4px; }}
  .overlay-stat strong {{ font-size: 1rem; font-weight: 950; }}
  .overlay-actions {{ display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }}

  @media (max-width: 1120px) {{
    .shell {{ grid-template-columns: 1fr; }}
    .sidebar {{ order: 2; }}
    .board-pane {{ order: 1; }}
  }}

  @media (max-width: 720px) {{
    body {{ padding: 0; }}
    .app {{ width: 100%; border-radius: 0; border: none; box-shadow: none; background: transparent; }}
    .topbar {{ padding: calc(12px + var(--safe-top)) 14px 12px; align-items: flex-start; flex-direction: column; }}
    .shell {{ padding: 10px; gap: 12px; }}
    .btn-row {{ grid-template-columns: 1fr; }}
    .board-head {{ flex-direction: column; }}
    .card, .board-card {{ border-radius: 18px; }}
    .status-row, .overlay-stats {{ grid-template-columns: 1fr 1fr; }}
  }}

  @media (max-width: 560px) {{
    .shell {{ padding: 8px; gap: 8px; }}
    .pad, .hero, .board-card {{ padding: 12px; }}
    #board {{ border-radius: 14px; }}
    .tile {{ border-radius: 3px; }}
    .overlay-box {{ padding: 18px; }}
  }}
</style>
</head>
<body>
  <div class="app">
    <div class="topbar">
      <div class="brand">
        <div class="logo">🧩</div>
        <div class="brand-copy">
          <div class="brand-title">Blululi Puzzle Studio</div>
          <div class="brand-sub">Experience-first mandala puzzle</div>
        </div>
      </div>
    </div>

    <div class="shell">
      <aside class="sidebar">
        <section class="card hero">
          <div class="eyebrow">Interactive Product Experience</div>
          <h1 class="headline">Play the art. Discover the product.</h1>
          <p class="sub">Choose a mandala, set the grid, and solve it with drag-and-drop on desktop or tap-to-swap on mobile.</p>
        </section>

        <section class="card pad">
          <div class="controls">
            <div class="control">
              <label class="label" for="imageSelect">Choose artwork</label>
              <select id="imageSelect"></select>
              <div class="helper">Rectangular and square artworks keep their real proportions.</div>
            </div>

            <div class="control">
              <label class="label" for="difficulty">Difficulty</label>
              <div class="range-wrap">
                <div class="range-row">
                  <input id="difficulty" type="range" min="2" max="8" value="4" />
                  <div class="range-value" id="gridBadge">4×4</div>
                </div>
                <div class="difficulty-copy">
                  <span id="difficultyName">Relaxed</span>
                  <span>2 to 8 tiles per side</span>
                </div>
              </div>
            </div>

            <div class="btn-row">
              <button class="btn-primary" id="shuffleBtn">Shuffle Puzzle</button>
              <button class="btn-secondary" id="resetBtn">Show Solved</button>
            </div>
          </div>
        </section>

        <section class="card pad preview-wrap">
          <div class="label">Artwork preview</div>
          <div class="preview" id="previewWrap">
            <div class="preview-frame" id="previewFrame">
              <img id="previewImg" alt="Selected artwork preview" />
              <div class="preview-badge">
                <span id="previewName">Mandala</span>
                <span id="difficultyTag">Relaxed</span>
              </div>
            </div>
          </div>
        </section>

        <section class="card pad">
          <div class="mini-item">
            <div class="mini-icon">✨</div>
            <div class="mini-copy">
              <strong>Clean puzzle UX</strong>
              <span>Fast start, no distortion, clear progress, and direct product CTA after completion.</span>
            </div>
          </div>
        </section>
      </aside>

      <main class="board-pane">
        <section class="board-card card">
          <div class="board-head">
            <div>
              <div class="board-title">Complete the artwork</div>
              <div class="board-note">Desktop: drag and drop. Mobile: tap one tile, then tap another.</div>
            </div>
            <div class="streak-pill" id="statusPill">Ready to play</div>
          </div>

          <div class="game-stage">
            <div class="board-shell">
              <div id="board"></div>
            </div>

            <div id="overlay" class="overlay">
              <div class="overlay-box">
                <div class="overlay-badge">Puzzle Complete</div>
                <h2 class="overlay-title">Mandala completed ✨</h2>
                <p class="overlay-copy" id="overlayCopy"></p>

                <div class="overlay-image-wrap" id="overlayImageWrap">
                  <img id="finalImage" class="overlay-image" alt="Completed design" />
                </div>

                <div class="overlay-stats">
                  <div class="overlay-stat">
                    <small>Moves</small>
                    <strong id="overlayMoves">0</strong>
                  </div>
                  <div class="overlay-stat">
                    <small>Time</small>
                    <strong id="overlayTime">0s</strong>
                  </div>
                  <div class="overlay-stat">
                    <small>Grid</small>
                    <strong id="overlayGrid">4×4</strong>
                  </div>
                </div>

                <div class="overlay-actions">
                  <a id="shopBtn" target="_blank" rel="noopener noreferrer" class="cta-link btn-success">Shop This Design</a>
                  <button class="btn-primary" id="againBtn">Play Again</button>
                  <button class="btn-secondary" id="closeOverlayBtn">Close</button>
                </div>
              </div>
            </div>
          </div>

          <div class="status-row">
            <div class="status-card">
              <div class="status-label">Grid</div>
              <div class="status-value" id="gridStat">4×4</div>
            </div>
            <div class="status-card">
              <div class="status-label">Moves</div>
              <div class="status-value" id="moves">0</div>
            </div>
            <div class="status-card">
              <div class="status-label">Time</div>
              <div class="status-value" id="time">0s</div>
            </div>
            <div class="status-card">
              <div class="status-label">Best This Session</div>
              <div class="status-value" id="best">—</div>
            </div>
          </div>

          <div class="focus-tip">Start from corners, then lock in strong curves and repeated line patterns.</div>
        </section>
      </main>
    </div>
  </div>

<script>
const images = {assets_json};
const products = {products_json};

const difficultyLabels = {{
  2: "Easy",
  3: "Casual",
  4: "Relaxed",
  5: "Standard",
  6: "Challenging",
  7: "Expert",
  8: "Master"
}};

const board = document.getElementById("board");
const imageSelect = document.getElementById("imageSelect");
const difficulty = document.getElementById("difficulty");
const gridBadge = document.getElementById("gridBadge");
const gridStat = document.getElementById("gridStat");
const difficultyName = document.getElementById("difficultyName");
const difficultyTag = document.getElementById("difficultyTag");
const movesEl = document.getElementById("moves");
const timeEl = document.getElementById("time");
const bestEl = document.getElementById("best");
const previewImg = document.getElementById("previewImg");
const previewName = document.getElementById("previewName");
const previewFrame = document.getElementById("previewFrame");
const previewWrap = document.getElementById("previewWrap");
const shuffleBtn = document.getElementById("shuffleBtn");
const resetBtn = document.getElementById("resetBtn");
const overlay = document.getElementById("overlay");
const overlayCopy = document.getElementById("overlayCopy");
const overlayMoves = document.getElementById("overlayMoves");
const overlayTime = document.getElementById("overlayTime");
const overlayGrid = document.getElementById("overlayGrid");
const finalImage = document.getElementById("finalImage");
const overlayImageWrap = document.getElementById("overlayImageWrap");
const againBtn = document.getElementById("againBtn");
const closeOverlayBtn = document.getElementById("closeOverlayBtn");
const shopBtn = document.getElementById("shopBtn");
const statusPill = document.getElementById("statusPill");

let grid = 4;
let arrangement = [];
let selectedIndex = null;
let dragFrom = null;
let currentImage = images[0]?.url || "";
let currentName = images[0]?.name || "Mandala";
let currentRatio = images[0]?.ratio || 1;
let moves = 0;
let seconds = 0;
let timerId = null;
let solved = false;
let sessionBest = null;

function safeProductUrl(index) {{
  if (!products.length) return "https://blululi.com";
  return products[index] || products[products.length - 1] || "https://blululi.com";
}}

function preloadImages() {{
  images.forEach((img) => {{
    const preloaded = new Image();
    preloaded.src = img.url;
  }});
}}

function populateImages() {{
  imageSelect.innerHTML = "";
  images.forEach((img, i) => {{
    const opt = document.createElement("option");
    opt.value = String(i);
    opt.textContent = img.name;
    imageSelect.appendChild(opt);
  }});
}}

function difficultyLabel() {{
  return difficultyLabels[grid] || "Standard";
}}

function updateGridLabels() {{
  const label = `${{grid}}×${{grid}}`;
  gridBadge.textContent = label;
  gridStat.textContent = label;
  overlayGrid.textContent = label;
  difficultyName.textContent = difficultyLabel();
  difficultyTag.textContent = difficultyLabel();
  board.style.setProperty("--grid-size", String(grid));
}}

function setBoardRatio(ratio) {{
  const safeRatio = Number.isFinite(ratio) && ratio > 0 ? ratio : 1;
  board.style.setProperty("--board-ratio", `${{safeRatio}} / 1`);
  previewFrame.style.setProperty("--preview-ratio", `${{safeRatio}} / 1`);
  overlayImageWrap.style.setProperty("--overlay-ratio", `${{safeRatio}} / 1`);
}}

function setPreview() {{
  const idx = Number(imageSelect.value || 0);
  const selected = images[idx] || images[0];
  currentImage = selected?.url || "";
  currentName = selected?.name || "Mandala";
  currentRatio = selected?.ratio || 1;
  previewImg.src = currentImage;
  previewName.textContent = currentName;
  shopBtn.href = safeProductUrl(idx);
  setBoardRatio(currentRatio);
}}

function resetStats() {{
  moves = 0;
  seconds = 0;
  movesEl.textContent = "0";
  timeEl.textContent = "0s";
  statusPill.textContent = "Game in progress";
}}

function updateBest() {{
  if (!sessionBest) {{
    bestEl.textContent = "—";
    return;
  }}
  bestEl.textContent = `${{sessionBest.seconds}}s`;
}}

function startTimer() {{
  stopTimer();
  timerId = window.setInterval(() => {{
    if (solved) return;
    seconds += 1;
    timeEl.textContent = `${{seconds}}s`;
  }}, 1000);
}}

function stopTimer() {{
  if (timerId !== null) {{
    clearInterval(timerId);
    timerId = null;
  }}
}}

function makeSolvedArrangement() {{
  return Array.from({{ length: grid * grid }}, (_, i) => i);
}}

function shuffleArray(arr) {{
  const out = [...arr];
  for (let i = out.length - 1; i > 0; i -= 1) {{
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }}
  return out;
}}

function makeShuffledArrangement() {{
  const solvedArr = makeSolvedArrangement();
  let arr = shuffleArray(solvedArr);
  if (arr.every((v, i) => v === i) && arr.length > 1) {{
    [arr[0], arr[1]] = [arr[1], arr[0]];
  }}
  return arr;
}}

function piecePosition(pieceId) {{
  const row = Math.floor(pieceId / grid);
  const col = pieceId % grid;
  return {{ row, col }};
}}

function renderBoard() {{
  board.innerHTML = "";

  arrangement.forEach((pieceId, boardIndex) => {{
    const tile = document.createElement("button");
    tile.type = "button";
    tile.className = "tile" + (solved ? " solved" : "");
    tile.dataset.boardIndex = String(boardIndex);
    tile.dataset.pieceId = String(pieceId);
    tile.draggable = !solved;
    tile.setAttribute("aria-label", `Puzzle tile ${{boardIndex + 1}}`);

    const pos = piecePosition(pieceId);
    const x = grid === 1 ? 0 : (pos.col / (grid - 1)) * 100;
    const y = grid === 1 ? 0 : (pos.row / (grid - 1)) * 100;

    tile.style.backgroundImage = `url("${{currentImage}}")`;
    tile.style.backgroundSize = `${{grid * 100}}% ${{grid * 100}}%`;
    tile.style.backgroundPosition = `${{x}}% ${{y}}%`;

    tile.addEventListener("click", () => onTileClick(boardIndex));

    tile.addEventListener("dragstart", () => {{
      if (solved) return;
      dragFrom = boardIndex;
      tile.classList.add("dragging");
    }});

    tile.addEventListener("dragend", () => {{
      tile.classList.remove("dragging");
      dragFrom = null;
    }});

    tile.addEventListener("dragover", (e) => {{
      if (!solved) e.preventDefault();
    }});

    tile.addEventListener("drop", (e) => {{
      e.preventDefault();
      if (solved) return;
      if (dragFrom === null || dragFrom === boardIndex) return;
      swapTiles(dragFrom, boardIndex);
      dragFrom = null;
    }});

    if (selectedIndex === boardIndex) {{
      tile.classList.add("selected");
    }}

    board.appendChild(tile);
  }});
}}

function pulseVibrate() {{
  if (navigator.vibrate) navigator.vibrate(8);
}}

function swapTiles(a, b) {{
  if (a === b || solved) return;
  [arrangement[a], arrangement[b]] = [arrangement[b], arrangement[a]];
  moves += 1;
  movesEl.textContent = String(moves);
  selectedIndex = null;
  pulseVibrate();
  window.requestAnimationFrame(() => {{
    renderBoard();
    checkSolved();
  }});
}}

function onTileClick(boardIndex) {{
  if (solved) return;

  if (selectedIndex === null) {{
    selectedIndex = boardIndex;
    renderBoard();
    return;
  }}

  if (selectedIndex === boardIndex) {{
    selectedIndex = null;
    renderBoard();
    return;
  }}

  swapTiles(selectedIndex, boardIndex);
}}

function closeOverlay() {{
  overlay.classList.remove("show");
}}

function maybeUpdateBest() {{
  if (!sessionBest || seconds < sessionBest.seconds) {{
    sessionBest = {{ seconds, moves, grid, name: currentName }};
  }}
  updateBest();
}}

function checkSolved() {{
  const ok = arrangement.every((pieceId, idx) => pieceId === idx);
  if (!ok) return;

  solved = true;
  stopTimer();
  maybeUpdateBest();
  renderBoard();
  finalImage.src = currentImage;
  overlayMoves.textContent = String(moves);
  overlayTime.textContent = `${{seconds}}s`;
  overlayGrid.textContent = `${{grid}}×${{grid}}`;
  overlayCopy.textContent = `You completed “${{currentName}}” in ${{moves}} moves and ${{seconds}} seconds.`;
  shopBtn.href = safeProductUrl(Number(imageSelect.value || 0));
  statusPill.textContent = "Completed";
  overlay.classList.add("show");
  pulseVibrate();
}}

function newGame() {{
  solved = false;
  selectedIndex = null;
  closeOverlay();
  arrangement = makeShuffledArrangement();
  updateGridLabels();
  setPreview();
  resetStats();
  renderBoard();
  startTimer();
}}

function reshuffleCurrentGame() {{
  solved = false;
  selectedIndex = null;
  closeOverlay();
  arrangement = makeShuffledArrangement();
  resetStats();
  renderBoard();
  startTimer();
}}

difficulty.addEventListener("input", () => {{
  grid = Number(difficulty.value);
  updateGridLabels();
}});

difficulty.addEventListener("change", () => {{
  grid = Number(difficulty.value);
  newGame();
}});

imageSelect.addEventListener("change", () => {{
  newGame();
}});

shuffleBtn.addEventListener("click", () => {{
  reshuffleCurrentGame();
}});

resetBtn.addEventListener("click", () => {{
  solved = false;
  selectedIndex = null;
  closeOverlay();
  arrangement = makeSolvedArrangement();
  updateGridLabels();
  setPreview();
  resetStats();
  renderBoard();
  startTimer();
  statusPill.textContent = "Solved preview";
}});

againBtn.addEventListener("click", () => {{
  reshuffleCurrentGame();
}});

closeOverlayBtn.addEventListener("click", () => {{
  closeOverlay();
}});

const ro = new ResizeObserver(() => {{
  if (arrangement.length) renderBoard();
}});
ro.observe(board);

window.addEventListener("resize", () => {{
  if (arrangement.length) renderBoard();
}});

preloadImages();
populateImages();
imageSelect.value = "0";
grid = Number(difficulty.value);
updateGridLabels();
setPreview();
updateBest();
newGame();
</script>
</body>
</html>
"""

st.components.v1.html(components_html, height=1280, scrolling=True)
