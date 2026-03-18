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
        background: #eff3ff !important;
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


def _to_asset(path: Path, max_dim: int = 1800, quality: int = 90) -> dict:
    with Image.open(path) as src:
        src = src.convert("RGB")
        width, height = src.size
        ratio = width / height if height else 1
        preview = src.copy()
        preview.thumbnail((max_dim, max_dim))
        buf = io.BytesIO()
        preview.save(buf, format="JPEG", quality=quality, optimize=True)

    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    name = IMAGE_TITLES.get(path.stem, path.stem.replace("_", " ").replace("-", " ").title())
    return {
        "name": name,
        "url": f"data:image/jpeg;base64,{encoded}",
        "width": width,
        "height": height,
        "ratio": ratio,
    }


assets = [_to_asset(p) for p in image_paths]
assets_json = json.dumps(assets)

components_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>Blululi Puzzle Studio</title>
<style>
  :root {{
    --bg: #eef3ff;
    --panel: rgba(255,255,255,.82);
    --line: rgba(76, 92, 160, .14);
    --text: #172033;
    --muted: #68738f;
    --accent: #6d28d9;
    --accent2: #8b5cf6;
    --good: #16a34a;
    --shadow: 0 18px 44px rgba(18, 24, 40, .10);
    --radius-xl: 28px;
    --radius-lg: 22px;
    --radius-md: 16px;
    --safe-top: env(safe-area-inset-top, 0px);
    --safe-bottom: env(safe-area-inset-bottom, 0px);
  }}

  * {{ box-sizing: border-box; }}
  * {{ -webkit-tap-highlight-color: transparent; }}

  html, body {{
    margin: 0;
    min-height: 100%;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: var(--text);
    background:
      radial-gradient(circle at top left, rgba(139,92,246,.13), transparent 26%),
      radial-gradient(circle at bottom right, rgba(99,102,241,.10), transparent 28%),
      linear-gradient(180deg, #f8faff 0%, #eef3ff 100%);
  }}

  body {{
    padding: 14px 14px calc(20px + var(--safe-bottom));
  }}

  .app {{
    width: min(1440px, 100%);
    margin: 0 auto;
    border-radius: 30px;
    overflow: hidden;
    background: rgba(255,255,255,.52);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,.72);
    box-shadow: var(--shadow);
  }}

  .topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: calc(14px + var(--safe-top)) 18px 14px;
    border-bottom: 1px solid var(--line);
    background: linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.70));
  }}

  .brand {{ display: flex; align-items: center; gap: 12px; }}
  .brand-badge {{
    width: 42px; height: 42px; border-radius: 14px;
    display: grid; place-items: center; color: white; font-size: 1.2rem;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    box-shadow: 0 12px 24px rgba(109,40,217,.24);
  }}
  .brand-name {{ font-weight: 900; letter-spacing: -.02em; }}
  .brand-sub {{ color: var(--muted); font-size: .88rem; }}

  .shell {{
    display: grid;
    grid-template-columns: 340px minmax(0, 1fr);
    gap: 16px;
    padding: 16px;
  }}

  .card {{
    border-radius: var(--radius-lg);
    background: var(--panel);
    border: 1px solid rgba(255,255,255,.78);
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 28px rgba(17,24,39,.07);
  }}

  .sidebar {{ display: grid; gap: 14px; align-content: start; }}
  .pad {{ padding: 18px; }}
  .hero {{ padding: 20px; }}

  .eyebrow {{
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 12px; border-radius: 999px;
    background: rgba(109,40,217,.08); color: var(--accent);
    font-size: .76rem; font-weight: 900; text-transform: uppercase; letter-spacing: .12em;
    margin-bottom: 14px;
  }}

  .headline {{ margin: 0 0 10px 0; font-size: clamp(1.6rem, 3vw, 2.4rem); line-height: 1.03; font-weight: 950; letter-spacing: -.04em; }}
  .sub {{ margin: 0; color: var(--muted); line-height: 1.6; }}

  .control {{ display: grid; gap: 8px; margin-bottom: 14px; }}
  .label {{ font-size: .78rem; font-weight: 900; color: var(--muted); text-transform: uppercase; letter-spacing: .1em; }}
  .helper {{ color: var(--muted); font-size: .9rem; line-height: 1.5; }}

  select, input[type="range"] {{ width: 100%; }}
  select {{
    appearance: none; border: 1px solid rgba(17,24,39,.08); border-radius: 16px;
    background: rgba(255,255,255,.97); color: var(--text);
    padding: 14px 15px; font-size: .98rem; outline: none;
  }}
  input[type="range"] {{ accent-color: var(--accent); }}

  .range-row {{ display: flex; align-items: center; gap: 12px; }}
  .range-value {{
    min-width: 88px; text-align: center; padding: 10px 12px; border-radius: 14px;
    background: rgba(255,255,255,.96); border: 1px solid rgba(17,24,39,.08); font-weight: 900;
  }}
  .difficulty-copy {{ display: flex; justify-content: space-between; gap: 8px; color: var(--muted); font-size: .84rem; }}

  .btn-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  button {{
    appearance: none; border: 0; border-radius: 16px; padding: 13px 16px;
    font-size: .96rem; font-weight: 900; cursor: pointer;
    transition: transform .14s ease, box-shadow .14s ease, opacity .14s ease;
  }}
  button:hover {{ transform: translateY(-1px); }}
  button:active {{ transform: translateY(0); }}
  .btn-primary {{ color: white; background: linear-gradient(135deg, var(--accent), var(--accent2)); box-shadow: 0 14px 24px rgba(109,40,217,.22); }}
  .btn-secondary {{ color: var(--text); background: rgba(255,255,255,.96); border: 1px solid rgba(17,24,39,.08); }}

  .preview {{ border-radius: 20px; overflow: hidden; background: white; border: 1px solid rgba(17,24,39,.06); }}
  .preview-box {{ width: 100%; aspect-ratio: var(--preview-ratio, 1 / 1); background: #fff; display: grid; place-items: center; }}
  .preview-box img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
  .preview-meta {{ padding: 14px; display: flex; justify-content: space-between; gap: 10px; color: var(--muted); font-size: .9rem; }}

  .mini-item {{ border-radius: 16px; padding: 12px 14px; border: 1px solid rgba(17,24,39,.06); background: rgba(255,255,255,.80); display: flex; gap: 10px; }}
  .mini-icon {{ width: 32px; height: 32px; border-radius: 12px; display: grid; place-items: center; background: rgba(109,40,217,.08); flex: 0 0 auto; }}
  .mini-copy strong {{ display: block; margin-bottom: 4px; }}
  .mini-copy span {{ color: var(--muted); font-size: .9rem; line-height: 1.45; }}

  .workspace {{
    display: grid;
    grid-template-columns: 280px minmax(0, 1fr);
    gap: 14px;
    align-items: start;
  }}

  .tray-card, .board-card {{ padding: 16px; }}
  .section-head {{ display: flex; justify-content: space-between; gap: 12px; align-items: start; margin-bottom: 12px; }}
  .section-title {{ font-size: 1.06rem; font-weight: 950; letter-spacing: -.02em; }}
  .section-note {{ color: var(--muted); font-size: .92rem; margin-top: 4px; }}
  .pill {{ border-radius: 999px; padding: 10px 14px; background: rgba(255,255,255,.92); border: 1px solid rgba(17,24,39,.08); font-size: .85rem; font-weight: 900; white-space: nowrap; }}

  .tray {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    min-height: 120px;
  }}

  .tray-empty {{
    color: var(--muted); font-size: .92rem; border: 1px dashed rgba(17,24,39,.12);
    border-radius: 16px; padding: 18px; text-align: center; background: rgba(255,255,255,.54);
  }}

  .board-wrap {{ display: grid; gap: 12px; }}
  .board-shell {{
    width: min(980px, 100%);
    margin: 0 auto;
    aspect-ratio: var(--board-ratio, 1 / 1);
    background: rgba(255,255,255,.94);
    border: 1px solid rgba(109,40,217,.10);
    border-radius: 24px;
    padding: 8px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.94), 0 18px 36px rgba(17,24,39,.06);
    position: relative;
    overflow: hidden;
  }}

  .ghost {{
    position: absolute; inset: 8px; border-radius: 18px; overflow: hidden;
    opacity: .18; pointer-events: none;
  }}
  .ghost img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}

  .board {{
    position: absolute; inset: 8px;
    display: grid; gap: 4px;
    z-index: 2;
  }}

  .slot {{
    position: relative; border-radius: 10px;
    background: rgba(109,40,217,.04);
    border: 1px dashed rgba(109,40,217,.12);
    overflow: hidden;
    min-width: 0; min-height: 0;
  }}
  .slot.correct {{ border-style: solid; border-color: rgba(22,163,74,.18); background: rgba(22,163,74,.05); }}
  .slot.selected {{ box-shadow: inset 0 0 0 3px rgba(109,40,217,.92); }}

  .piece {{
    width: 100%; height: 100%; border: 0; outline: 0; padding: 0; margin: 0;
    border-radius: 8px; overflow: hidden; cursor: grab; position: relative;
    background-repeat: no-repeat; background-color: rgba(255,255,255,.86);
    transition: transform .12s ease, box-shadow .12s ease, opacity .12s ease;
  }}
  .piece:hover {{ box-shadow: 0 10px 18px rgba(17,24,39,.12); transform: translateY(-1px); }}
  .piece.dragging {{ opacity: .72; cursor: grabbing; transform: scale(.98); }}
  .piece.selected {{ box-shadow: inset 0 0 0 3px rgba(109,40,217,.96); }}
  .piece.correct {{ cursor: default; }}

  .piece::after {{
    content: attr(data-hint);
    position: absolute; right: 6px; bottom: 6px;
    min-width: 20px; height: 20px; padding: 0 6px;
    border-radius: 999px; display: grid; place-items: center;
    background: rgba(17,24,39,.62); color: white;
    font-size: .68rem; font-weight: 900; letter-spacing: .02em;
  }}

  .status-row {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }}
  .status-card {{ border-radius: 18px; padding: 14px; background: rgba(255,255,255,.88); border: 1px solid rgba(17,24,39,.06); }}
  .status-label {{ font-size: .74rem; text-transform: uppercase; letter-spacing: .09em; color: var(--muted); font-weight: 800; margin-bottom: 6px; }}
  .status-value {{ font-size: 1.04rem; font-weight: 950; }}

  .focus-tip {{ text-align: center; color: var(--muted); font-size: .93rem; }}

  .overlay {{ position: fixed; inset: 0; display: none; align-items: center; justify-content: center; background: rgba(15,23,42,.54); backdrop-filter: blur(8px); padding: 20px; z-index: 99; }}
  .overlay.show {{ display: flex; }}
  .overlay-box {{ width: min(620px, 94%); background: rgba(255,255,255,.98); border-radius: 28px; padding: 26px; text-align: center; box-shadow: 0 30px 60px rgba(0,0,0,.18); border: 1px solid rgba(255,255,255,.88); }}
  .overlay-badge {{ display: inline-flex; padding: 8px 12px; border-radius: 999px; background: rgba(22,163,74,.10); color: #15803d; font-size: .78rem; font-weight: 900; text-transform: uppercase; letter-spacing: .1em; margin-bottom: 14px; }}
  .overlay-title {{ margin: 0 0 10px 0; font-size: 1.8rem; font-weight: 950; letter-spacing: -.03em; }}
  .overlay-copy {{ margin: 0 0 18px 0; color: var(--muted); line-height: 1.6; font-size: 1rem; }}
  .overlay-image-wrap {{ width: min(360px, 100%); margin: 0 auto 18px; aspect-ratio: var(--board-ratio, 1 / 1); border-radius: 20px; overflow: hidden; box-shadow: 0 18px 30px rgba(17,24,39,.14); background: #fff; }}
  .overlay-image-wrap img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
  .overlay-stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 18px; }}
  .overlay-stat {{ border-radius: 18px; padding: 12px; background: rgba(248,250,252,1); border: 1px solid rgba(17,24,39,.06); }}
  .overlay-stat small {{ display: block; color: var(--muted); font-weight: 800; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 4px; }}
  .overlay-stat strong {{ font-size: 1rem; font-weight: 950; }}
  .overlay-actions {{ display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }}

  @media (max-width: 1180px) {{
    .shell {{ grid-template-columns: 1fr; }}
    .workspace {{ grid-template-columns: 1fr; }}
  }}

  @media (max-width: 760px) {{
    body {{ padding: 0; }}
    .app {{ width: 100%; border-radius: 0; border: 0; box-shadow: none; background: transparent; }}
    .topbar {{ padding: calc(12px + var(--safe-top)) 14px 12px; }}
    .shell {{ padding: 10px; gap: 10px; }}
    .btn-row {{ grid-template-columns: 1fr; }}
    .status-row, .overlay-stats {{ grid-template-columns: 1fr 1fr; }}
    .tray {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
  }}
</style>
</head>
<body>
  <div class="app">
    <div class="topbar">
      <div class="brand">
        <div class="brand-badge">🧩</div>
        <div>
          <div class="brand-name">Blululi Puzzle Studio</div>
          <div class="brand-sub">UX-first puzzle for detailed and low-contrast mandalas.</div>
        </div>
      </div>
    </div>

    <div class="shell">
      <aside class="sidebar">
        <section class="card hero">
          <div class="eyebrow">Better puzzle logic</div>
          <h1 class="headline">No more impossible white tiles.</h1>
          <p class="sub">Pieces live in a tray, the board keeps the real image ratio, and a soft ghost guide makes low-contrast mandalas solvable without ruining the artwork.</p>
        </section>

        <section class="card pad">
          <div class="control">
            <label class="label" for="imageSelect">Choose artwork</label>
            <select id="imageSelect"></select>
            <div class="helper">The board preserves the original aspect ratio of each mandala.</div>
          </div>

          <div class="control">
            <label class="label" for="difficulty">Difficulty</label>
            <div class="range-row">
              <input id="difficulty" type="range" min="2" max="8" value="4" />
              <div class="range-value" id="gridBadge">4×4</div>
            </div>
            <div class="difficulty-copy">
              <span id="difficultyName">Relaxed</span>
              <span>drag from tray or tap to place</span>
            </div>
          </div>

          <div class="btn-row">
            <button class="btn-primary" id="shuffleBtn">New Puzzle</button>
            <button class="btn-secondary" id="resetBtn">Reset</button>
          </div>
        </section>

        <section class="card preview">
          <div class="preview-box" id="previewBox">
            <img id="previewImg" alt="Selected artwork preview" />
          </div>
          <div class="preview-meta">
            <strong id="previewName">Mandala</strong>
            <span id="previewRatio">1:1</span>
          </div>
        </section>

        <section class="card pad">
          <div class="mini-item">
            <div class="mini-icon">💡</div>
            <div class="mini-copy">
              <strong>Why this works better</strong>
              <span>Swap puzzles break on white backgrounds. A tray + target board + subtle ghost guide keeps the experience clean and actually playable.</span>
            </div>
          </div>
        </section>
      </aside>

      <main class="workspace">
        <section class="card tray-card">
          <div class="section-head">
            <div>
              <div class="section-title">Piece tray</div>
              <div class="section-note">Drag pieces to the board. On mobile, tap a piece then tap a slot.</div>
            </div>
            <div class="pill" id="trayCount">0 pieces</div>
          </div>
          <div id="tray" class="tray"></div>
        </section>

        <section class="card board-card">
          <div class="section-head">
            <div>
              <div class="section-title">Build the mandala</div>
              <div class="section-note">Low-opacity guide under the board helps distinguish empty or low-detail areas.</div>
            </div>
            <div class="pill" id="statusPill">Ready</div>
          </div>

          <div class="board-wrap">
            <div class="board-shell" id="boardShell">
              <div class="ghost"><img id="ghostImg" alt="Ghost guide" /></div>
              <div class="board" id="board"></div>
            </div>

            <div class="status-row">
              <div class="status-card">
                <div class="status-label">Grid</div>
                <div class="status-value" id="gridStat">4×4</div>
              </div>
              <div class="status-card">
                <div class="status-label">Placed</div>
                <div class="status-value" id="placedStat">0</div>
              </div>
              <div class="status-card">
                <div class="status-label">Moves</div>
                <div class="status-value" id="movesStat">0</div>
              </div>
              <div class="status-card">
                <div class="status-label">Time</div>
                <div class="status-value" id="timeStat">0s</div>
              </div>
            </div>

            <div class="focus-tip">Each piece has a tiny position cue. That solves the white-background problem without adding visual chaos.</div>
          </div>
        </section>
      </main>
    </div>
  </div>

  <div id="overlay" class="overlay">
    <div class="overlay-box">
      <div class="overlay-badge">Puzzle complete</div>
      <h2 class="overlay-title">Mandala completed ✨</h2>
      <p class="overlay-copy" id="overlayCopy"></p>
      <div class="overlay-image-wrap" id="overlayImageWrap">
        <img id="finalImage" alt="Completed artwork" />
      </div>
      <div class="overlay-stats">
        <div class="overlay-stat"><small>Moves</small><strong id="overlayMoves">0</strong></div>
        <div class="overlay-stat"><small>Time</small><strong id="overlayTime">0s</strong></div>
        <div class="overlay-stat"><small>Grid</small><strong id="overlayGrid">4×4</strong></div>
      </div>
      <div class="overlay-actions">
        <button class="btn-primary" id="againBtn">Play Again</button>
        <button class="btn-secondary" id="closeOverlayBtn">Close</button>
      </div>
    </div>
  </div>

<script>
const images = {assets_json};

const difficultyLabels = {{
  2: "Easy",
  3: "Casual",
  4: "Relaxed",
  5: "Standard",
  6: "Challenging",
  7: "Expert",
  8: "Master"
}};

const imageSelect = document.getElementById("imageSelect");
const difficulty = document.getElementById("difficulty");
const gridBadge = document.getElementById("gridBadge");
const gridStat = document.getElementById("gridStat");
const difficultyName = document.getElementById("difficultyName");
const previewBox = document.getElementById("previewBox");
const previewImg = document.getElementById("previewImg");
const previewName = document.getElementById("previewName");
const previewRatio = document.getElementById("previewRatio");
const ghostImg = document.getElementById("ghostImg");
const tray = document.getElementById("tray");
const board = document.getElementById("board");
const boardShell = document.getElementById("boardShell");
const trayCount = document.getElementById("trayCount");
const statusPill = document.getElementById("statusPill");
const placedStat = document.getElementById("placedStat");
const movesStat = document.getElementById("movesStat");
const timeStat = document.getElementById("timeStat");
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

let grid = 4;
let currentIndex = 0;
let trayPieces = [];
let boardSlots = [];
let selectedPieceId = null;
let dragPieceId = null;
let moves = 0;
let seconds = 0;
let timerId = null;
let solved = false;

function ratioText(ratio) {{
  if (!Number.isFinite(ratio) || ratio <= 0) return "1:1";
  if (Math.abs(ratio - 1) < 0.06) return "1:1";
  if (ratio > 1) return `${{ratio.toFixed(2)}}:1`;
  return `1:${{(1 / ratio).toFixed(2)}}`;
}}

function currentImage() {{
  return images[currentIndex] || images[0];
}}

function pieceHint(pieceId) {{
  const row = Math.floor(pieceId / grid) + 1;
  const col = (pieceId % grid) + 1;
  return `${{row}}·${{col}}`;
}}

function shuffleArray(arr) {{
  const copy = [...arr];
  for (let i = copy.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }}
  return copy;
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

function updateImageMeta() {{
  const img = currentImage();
  previewImg.src = img.url;
  ghostImg.src = img.url;
  finalImage.src = img.url;
  previewName.textContent = img.name;
  previewRatio.textContent = ratioText(img.ratio);
  previewBox.style.setProperty("--preview-ratio", `${{img.width}} / ${{img.height}}`);
  boardShell.style.setProperty("--board-ratio", `${{img.width}} / ${{img.height}}`);
  overlayImageWrap.style.setProperty("--board-ratio", `${{img.width}} / ${{img.height}}`);
}}

function updateGridLabels() {{
  const label = `${{grid}}×${{grid}}`;
  gridBadge.textContent = label;
  gridStat.textContent = label;
  overlayGrid.textContent = label;
  difficultyName.textContent = difficultyLabel();
  board.style.gridTemplateColumns = `repeat(${{grid}}, 1fr)`;
  board.style.gridTemplateRows = `repeat(${{grid}}, 1fr)`;
}}

function resetStats() {{
  moves = 0;
  seconds = 0;
  solved = false;
  movesStat.textContent = "0";
  timeStat.textContent = "0s";
  placedStat.textContent = "0";
  statusPill.textContent = "In progress";
}}

function startTimer() {{
  stopTimer();
  timerId = window.setInterval(() => {{
    if (solved) return;
    seconds += 1;
    timeStat.textContent = `${{seconds}}s`;
  }}, 1000);
}}

function stopTimer() {{
  if (timerId !== null) {{
    clearInterval(timerId);
    timerId = null;
  }}
}}

function closeOverlay() {{
  overlay.classList.remove("show");
}}

function openOverlay() {{
  overlayMoves.textContent = String(moves);
  overlayTime.textContent = `${{seconds}}s`;
  overlayGrid.textContent = `${{grid}}×${{grid}}`;
  overlayCopy.textContent = `You completed “${{currentImage().name}}” in ${{moves}} moves and ${{seconds}} seconds.`;
  overlay.classList.add("show");
}}

function pulseVibrate() {{
  if (navigator.vibrate) navigator.vibrate(8);
}}

function newGame() {{
  closeOverlay();
  selectedPieceId = null;
  dragPieceId = null;
  const total = grid * grid;
  trayPieces = shuffleArray(Array.from({{ length: total }}, (_, i) => i));
  boardSlots = Array.from({{ length: total }}, () => null);
  updateImageMeta();
  updateGridLabels();
  resetStats();
  render();
  startTimer();
}}

function resetGame() {{
  closeOverlay();
  selectedPieceId = null;
  dragPieceId = null;
  const total = grid * grid;
  trayPieces = Array.from({{ length: total }}, (_, i) => i);
  boardSlots = Array.from({{ length: total }}, () => null);
  updateImageMeta();
  updateGridLabels();
  resetStats();
  render();
  startTimer();
}}

function findPieceLocation(pieceId) {{
  const trayIndex = trayPieces.indexOf(pieceId);
  if (trayIndex !== -1) return {{ area: "tray", index: trayIndex }};
  const boardIndex = boardSlots.indexOf(pieceId);
  if (boardIndex !== -1) return {{ area: "board", index: boardIndex }};
  return null;
}}

function removePiece(pieceId) {{
  const loc = findPieceLocation(pieceId);
  if (!loc) return;
  if (loc.area === "tray") trayPieces.splice(loc.index, 1);
  else boardSlots[loc.index] = null;
}}

function placePiece(pieceId, slotIndex) {{
  if (solved) return;
  const existing = boardSlots[slotIndex];
  removePiece(pieceId);
  if (existing !== null) trayPieces.push(existing);
  boardSlots[slotIndex] = pieceId;
  selectedPieceId = null;
  moves += 1;
  pulseVibrate();
  render();
  checkSolved();
}}

function returnPieceToTray(pieceId) {{
  if (solved) return;
  const loc = findPieceLocation(pieceId);
  if (!loc || loc.area !== "board") return;
  boardSlots[loc.index] = null;
  trayPieces.push(pieceId);
  selectedPieceId = null;
  moves += 1;
  render();
}}

function onPieceTap(pieceId) {{
  if (solved) return;
  selectedPieceId = selectedPieceId === pieceId ? null : pieceId;
  render();
}}

function onSlotTap(slotIndex) {{
  if (solved) return;
  const pieceId = selectedPieceId;
  if (pieceId === null) return;
  placePiece(pieceId, slotIndex);
}}

function onTrayTap() {{
  if (solved || selectedPieceId === null) return;
  const loc = findPieceLocation(selectedPieceId);
  if (loc && loc.area === "board") returnPieceToTray(selectedPieceId);
}}

function placedCount() {{
  return boardSlots.filter(v => v !== null).length;
}}

function renderPiece(pieceId, square = true) {{
  const img = currentImage();
  const piece = document.createElement("button");
  piece.type = "button";
  piece.className = "piece";
  piece.dataset.pieceId = String(pieceId);
  piece.dataset.hint = pieceHint(pieceId);
  piece.draggable = !solved;
  piece.setAttribute("aria-label", `Piece ${{pieceHint(pieceId)}}`);

  const row = Math.floor(pieceId / grid);
  const col = pieceId % grid;

  piece.style.backgroundImage = `url("${{img.url}}")`;
  piece.style.backgroundSize = `${{grid * 100}}% ${{grid * 100}}%`;
  piece.style.backgroundPosition = `${{(grid === 1 ? 0 : col / (grid - 1)) * 100}}% ${{(grid === 1 ? 0 : row / (grid - 1)) * 100}}%`;
  if (!square) piece.style.aspectRatio = `${{img.width / grid}} / ${{img.height / grid}}`;

  if (selectedPieceId === pieceId) piece.classList.add("selected");

  piece.addEventListener("click", () => onPieceTap(pieceId));
  piece.addEventListener("dragstart", () => {{
    if (solved) return;
    dragPieceId = pieceId;
    piece.classList.add("dragging");
  }});
  piece.addEventListener("dragend", () => {{
    dragPieceId = null;
    piece.classList.remove("dragging");
  }});

  return piece;
}}

function renderTray() {{
  tray.innerHTML = "";
  trayCount.textContent = `${{trayPieces.length}} piece${{trayPieces.length === 1 ? "" : "s"}}`;

  if (!trayPieces.length) {{
    const empty = document.createElement("div");
    empty.className = "tray-empty";
    empty.textContent = "Tray empty. Finish the board.";
    tray.appendChild(empty);
    return;
  }}

  trayPieces.forEach(pieceId => {{
    const piece = renderPiece(pieceId, false);
    tray.appendChild(piece);
  }});

  tray.onclick = (event) => {{
    if (event.target === tray) onTrayTap();
  }};

  tray.addEventListener("dragover", (event) => {{
    if (!solved) event.preventDefault();
  }});
  tray.addEventListener("drop", (event) => {{
    event.preventDefault();
    if (solved || dragPieceId === null) return;
    const loc = findPieceLocation(dragPieceId);
    if (loc && loc.area === "board") returnPieceToTray(dragPieceId);
    dragPieceId = null;
  }});
}}

function renderBoard() {{
  board.innerHTML = "";
  board.style.gridTemplateColumns = `repeat(${{grid}}, 1fr)`;
  board.style.gridTemplateRows = `repeat(${{grid}}, 1fr)`;

  boardSlots.forEach((pieceId, slotIndex) => {{
    const slot = document.createElement("div");
    slot.className = "slot";
    if (pieceId === slotIndex && pieceId !== null) slot.classList.add("correct");
    if (selectedPieceId !== null && pieceId === null) slot.classList.add("selected");

    slot.addEventListener("click", () => onSlotTap(slotIndex));
    slot.addEventListener("dragover", (event) => {{
      if (!solved) event.preventDefault();
    }});
    slot.addEventListener("drop", (event) => {{
      event.preventDefault();
      if (solved || dragPieceId === null) return;
      placePiece(dragPieceId, slotIndex);
      dragPieceId = null;
    }});

    if (pieceId !== null) {{
      const piece = renderPiece(pieceId, true);
      if (pieceId === slotIndex) piece.classList.add("correct");
      slot.appendChild(piece);
    }}

    board.appendChild(slot);
  }});
}}

function render() {{
  movesStat.textContent = String(moves);
  placedStat.textContent = String(placedCount());
  renderTray();
  renderBoard();
}}

function checkSolved() {{
  const done = boardSlots.every((pieceId, index) => pieceId === index);
  if (!done) return;
  solved = true;
  stopTimer();
  statusPill.textContent = "Completed";
  render();
  openOverlay();
  pulseVibrate();
}}

imageSelect.addEventListener("change", () => {{
  currentIndex = Number(imageSelect.value || 0);
  newGame();
}});

difficulty.addEventListener("input", () => {{
  grid = Number(difficulty.value);
  updateGridLabels();
}});

difficulty.addEventListener("change", () => {{
  grid = Number(difficulty.value);
  newGame();
}});

shuffleBtn.addEventListener("click", newGame);
resetBtn.addEventListener("click", resetGame);
againBtn.addEventListener("click", newGame);
closeOverlayBtn.addEventListener("click", closeOverlay);

populateImages();
imageSelect.value = "0";
currentIndex = 0;
grid = Number(difficulty.value);
newGame();
</script>
</body>
</html>
"""

st.components.v1.html(components_html, height=1320, scrolling=True)
