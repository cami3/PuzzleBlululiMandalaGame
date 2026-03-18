import os
import random
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import streamlit as st
from PIL import Image, ImageOps, ImageDraw

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Blululi Puzzle Experience",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

products = [
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

IMAGE_PRODUCT_MAP = {key: url for key, url in zip(IMAGE_TITLES.keys(), products)}
ASSETS_DIR = Path("images")
SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]

# =========================
# STYLING
# =========================
CUSTOM_CSS = """
<style>
:root {
    --bg: #0b1020;
    --panel: rgba(255,255,255,0.07);
    --panel-2: rgba(255,255,255,0.10);
    --stroke: rgba(255,255,255,0.12);
    --text: #f7f8fb;
    --muted: #c9d0ea;
    --accent: #9b8cff;
    --accent-2: #3dd9b4;
    --warm: #ffb86b;
}

.stApp {
    background:
        radial-gradient(circle at 20% 0%, rgba(155,140,255,0.28), transparent 28%),
        radial-gradient(circle at 100% 10%, rgba(61,217,180,0.18), transparent 30%),
        linear-gradient(180deg, #0b1020 0%, #111833 100%);
    color: var(--text);
}

.block-container {
    padding-top: 1.25rem;
    padding-bottom: 2rem;
    max-width: 1320px;
}

h1, h2, h3, h4, p, label, div, span {
    color: var(--text);
}

.hero {
    padding: 1.4rem 1.5rem;
    border: 1px solid var(--stroke);
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border-radius: 24px;
    box-shadow: 0 16px 50px rgba(0,0,0,0.25);
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 2.25rem;
    line-height: 1.05;
    font-weight: 800;
    margin-bottom: .45rem;
}

.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    max-width: 840px;
}

.glass {
    background: var(--panel);
    border: 1px solid var(--stroke);
    border-radius: 22px;
    padding: 1rem 1rem 0.9rem 1rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
}

.stat-pill {
    display: inline-block;
    padding: .45rem .7rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1px solid var(--stroke);
    margin-right: .35rem;
    margin-bottom: .35rem;
    font-size: .9rem;
}

.product-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.04));
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 1rem;
    min-height: 180px;
}

.product-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: .5rem;
}

.product-copy {
    color: var(--muted);
    font-size: .95rem;
    line-height: 1.45;
    margin-bottom: .9rem;
}

.cta {
    display: inline-block;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    color: white !important;
    text-decoration: none;
    font-weight: 700;
    padding: .78rem 1rem;
    border-radius: 14px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.22);
}

.small-note {
    color: var(--muted);
    font-size: 0.85rem;
}

.tile-label {
    text-align: center;
    font-size: .83rem;
    color: var(--muted);
    margin-top: .35rem;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 800;
    margin-bottom: .8rem;
}

div[data-testid="stButton"] > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.12);
    background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.05));
    color: white;
    font-weight: 700;
    min-height: 44px;
}

div[data-testid="stButton"] > button:hover {
    border-color: rgba(155,140,255,0.65);
    box-shadow: 0 0 0 1px rgba(155,140,255,0.3) inset;
}

div[data-testid="stSelectbox"],
div[data-testid="stRadio"],
div[data-testid="stSlider"] {
    background: transparent;
}

[data-testid="stImage"] img {
    border-radius: 18px;
}

hr {
    border-color: rgba(255,255,255,0.10);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =========================
# DATA STRUCTURES
# =========================
@dataclass
class PuzzleState:
    image_key: str
    grid_size: int
    tiles: List[int]
    moves: int = 0
    selected_idx: Optional[int] = None
    solved: bool = False
    hints_used: int = 0


# =========================
# HELPERS
# =========================
def init_session() -> None:
    defaults = {
        "puzzle": None,
        "show_preview": True,
        "image_cache": {},
        "product_clicked": False,
        "session_started": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def pretty_slug(url: str) -> str:
    slug = url.rstrip("/").split("/")[-1].replace("-", " ").strip()
    return slug[:1].upper() + slug[1:]


def image_path_for_key(image_key: str) -> Optional[Path]:
    for ext in SUPPORTED_EXTENSIONS:
        candidate = ASSETS_DIR / f"{image_key}{ext}"
        if candidate.exists():
            return candidate
    return None


def available_images() -> List[str]:
    return [key for key in IMAGE_TITLES.keys() if image_path_for_key(key) is not None]


def load_image(image_key: str) -> Image.Image:
    cache: Dict[str, Image.Image] = st.session_state.image_cache
    if image_key in cache:
        return cache[image_key]

    path = image_path_for_key(image_key)
    if path is None:
        img = Image.new("RGB", (1080, 1080), "#1f2747")
        draw = ImageDraw.Draw(img)
        draw.text((60, 80), f"Missing asset:\n{image_key}", fill="white")
        cache[image_key] = img
        return img

    img = Image.open(path).convert("RGB")
    img = ImageOps.exif_transpose(img)
    cache[image_key] = img
    return img


def crop_square(img: Image.Image, size: int = 1080) -> Image.Image:
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    cropped = img.crop((left, top, left + side, top + side))
    return cropped.resize((size, size))


def split_image_into_tiles(img: Image.Image, grid_size: int) -> List[Image.Image]:
    img = crop_square(img)
    tile_size = img.size[0] // grid_size
    tiles = []
    for r in range(grid_size):
        for c in range(grid_size):
            left = c * tile_size
            top = r * tile_size
            tile = img.crop((left, top, left + tile_size, top + tile_size))
            tiles.append(tile)
    return tiles


def shuffled_order(n: int) -> List[int]:
    base = list(range(n))
    shuffled = base[:]
    while shuffled == base:
        random.shuffle(shuffled)
    return shuffled


def start_new_game(image_key: str, grid_size: int) -> None:
    tile_count = grid_size * grid_size
    st.session_state.puzzle = PuzzleState(
        image_key=image_key,
        grid_size=grid_size,
        tiles=shuffled_order(tile_count),
    )
    st.session_state.product_clicked = False
    st.session_state.session_started = True


def get_tiles_for_current_puzzle() -> List[Image.Image]:
    puzzle: PuzzleState = st.session_state.puzzle
    return split_image_into_tiles(load_image(puzzle.image_key), puzzle.grid_size)


def is_solved(puzzle: PuzzleState) -> bool:
    return puzzle.tiles == list(range(len(puzzle.tiles)))


def swap_tiles(puzzle: PuzzleState, a: int, b: int) -> None:
    puzzle.tiles[a], puzzle.tiles[b] = puzzle.tiles[b], puzzle.tiles[a]
    puzzle.moves += 1
    puzzle.selected_idx = None
    puzzle.solved = is_solved(puzzle)


def auto_place_one_tile(puzzle: PuzzleState) -> None:
    if puzzle.solved:
        return

    for idx, tile_value in enumerate(puzzle.tiles):
        if idx != tile_value:
            correct_idx = puzzle.tiles.index(idx)
            swap_tiles(puzzle, idx, correct_idx)
            puzzle.hints_used += 1
            puzzle.moves = max(0, puzzle.moves - 1)
            break


def get_product_recommendations(image_key: str, max_items: int = 3) -> List[str]:
    all_urls = products[:]
    primary = IMAGE_PRODUCT_MAP.get(image_key)
    recommendations = [primary] if primary else []
    for url in all_urls:
        if url not in recommendations:
            recommendations.append(url)
    return recommendations[:max_items]


def progress_ratio(puzzle: PuzzleState) -> float:
    correct = sum(1 for idx, tile in enumerate(puzzle.tiles) if idx == tile)
    return correct / len(puzzle.tiles)


def tile_border(idx: int, selected_idx: Optional[int]) -> int:
    return 8 if selected_idx == idx else 0


def tile_caption(idx: int, selected_idx: Optional[int]) -> str:
    if selected_idx == idx:
        return "Selected"
    return "Tap to select"


# =========================
# UI SECTIONS
# =========================
def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Mandala Puzzle Experience</div>
            <div class="hero-sub">
                Trasforma la curiosità in acquisto: un mini-game immersivo che fa scoprire l'artwork,
                aumenta il tempo speso sulla pagina e converte il completamento del puzzle in click al prodotto.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_setup_panel() -> Tuple[str, int]:
    st.markdown('<div class="section-title">1. Scegli il puzzle</div>', unsafe_allow_html=True)
    valid_images = available_images()
    fallback_keys = list(IMAGE_TITLES.keys())
    options = valid_images if valid_images else fallback_keys

    c1, c2, c3 = st.columns([1.3, 1, 1])
    with c1:
        selected_image = st.selectbox(
            "Artwork",
            options=options,
            format_func=lambda k: IMAGE_TITLES.get(k, k),
            key="selected_image_key",
        )
    with c2:
        difficulty = st.selectbox(
            "Difficoltà",
            options=[2, 3, 4],
            format_func=lambda x: {2: "Easy · 2x2", 3: "Medium · 3x3", 4: "Hard · 4x4"}[x],
            key="grid_size_choice",
        )
    with c3:
        st.markdown("<div style='height: 1.85rem'></div>", unsafe_allow_html=True)
        start = st.button("🎮 Start / Restart Game", use_container_width=True)
        if start:
            start_new_game(selected_image, difficulty)
            st.rerun()

    return selected_image, difficulty


def render_preview_and_stats(image_key: str, grid_size: int) -> None:
    img = crop_square(load_image(image_key))
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown(f"### {IMAGE_TITLES.get(image_key, image_key)}")
        st.image(img, use_container_width=True)
        st.caption("Preview dell'immagine intera. Durante il gioco puoi nasconderla per rendere l'esperienza più sfidante.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### UX e conversione")
        st.markdown(
            """
            <span class="stat-pill">Puzzle visuale</span>
            <span class="stat-pill">Reward finale</span>
            <span class="stat-pill">CTA contestuale</span>
            <span class="stat-pill">Cross-sell leggero</span>
            <span class="stat-pill">Nessun attrito</span>
            """,
            unsafe_allow_html=True,
        )
        st.write(
            """
            Flusso consigliato:
            1. l'utente sceglie un mandala,
            2. completa il puzzle,
            3. riceve una ricompensa visiva e scopre il prodotto coordinato,
            4. può cliccare subito sul CTA con forte match estetico.
            """
        )
        st.write(f"Grid corrente: **{grid_size}x{grid_size}**")
        st.markdown("</div>", unsafe_allow_html=True)

import streamlit.components.v1 as components

def render_real_puzzle(image_url, grid=3):
    html = f"""
    <style>
    #puzzle-container {{
        width: 100%;
        max-width: 500px;
        margin: auto;
    }}
    canvas {{
        width: 100%;
        border-radius: 16px;
        cursor: grab;
    }}
    </style>

    <div id="puzzle-container">
        <canvas id="puzzleCanvas"></canvas>
    </div>

    <script>
    const canvas = document.getElementById("puzzleCanvas");
    const ctx = canvas.getContext("2d");

    const gridSize = {grid};
    let pieces = [];
    let selected = null;

    const img = new Image();
    img.src = "{image_url}";

    img.onload = () => {{
        canvas.width = img.width;
        canvas.height = img.height;

        const pieceW = img.width / gridSize;
        const pieceH = img.height / gridSize;

        for (let y = 0; y < gridSize; y++) {{
            for (let x = 0; x < gridSize; x++) {{
                pieces.push({{
                    x: x,
                    y: y,
                    correctX: x,
                    correctY: y
                }});
            }}
        }}

        shuffle(pieces);
        draw();
    }};

    function shuffle(array) {{
        for (let i = array.length - 1; i > 0; i--) {{
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }}
    }}

    function draw() {{
        const pieceW = canvas.width / gridSize;
        const pieceH = canvas.height / gridSize;

        pieces.forEach((p, i) => {{
            const sx = p.correctX * pieceW;
            const sy = p.correctY * pieceH;

            const dx = (i % gridSize) * pieceW;
            const dy = Math.floor(i / gridSize) * pieceH;

            ctx.drawImage(img, sx, sy, pieceW, pieceH, dx, dy, pieceW, pieceH);
        }});
    }}

    canvas.addEventListener("click", (e) => {{
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const pieceW = canvas.width / gridSize;
        const pieceH = canvas.height / gridSize;

        const col = Math.floor(x / pieceW);
        const row = Math.floor(y / pieceH);

        const index = row * gridSize + col;

        if (selected === null) {{
            selected = index;
        }} else {{
            [pieces[selected], pieces[index]] = [pieces[index], pieces[selected]];
            selected = null;
            ctx.clearRect(0,0,canvas.width,canvas.height);
            draw();
        }}
    }});
    </script>
    """
    components.html(html, height=520)


# =========================
# MAIN
# =========================
def main() -> None:
    init_session()
    render_header()

    selected_image, difficulty = render_setup_panel()
    render_preview_and_stats(selected_image, difficulty)
    st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)

    if st.session_state.puzzle is None:
        st.info("Premi Start per iniziare il puzzle. Se le immagini sono locali, mettile nella cartella `assets/`.")
    else:
        render_real_puzzle(
    image_url="https://tuo-cdn.com/web_purple.jpg",
    grid=3
)



if __name__ == "__main__":
    main()
