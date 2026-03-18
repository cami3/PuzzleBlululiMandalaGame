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
ASSETS_DIR = Path("assets")
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


def render_game_board() -> None:
    puzzle: PuzzleState = st.session_state.puzzle
    tiles_img = get_tiles_for_current_puzzle()

    st.markdown('<div class="section-title">2. Risolvi il puzzle</div>', unsafe_allow_html=True)

    top_left, top_mid, top_right = st.columns([1.2, 1, 1])
    with top_left:
        st.markdown(
            f"""
            <div class="glass">
                <div><strong>Artwork:</strong> {IMAGE_TITLES[puzzle.image_key]}</div>
                <div class="small-note">Seleziona una tessera e poi un'altra per scambiarle.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_mid:
        st.metric("Moves", puzzle.moves)
    with top_right:
        percent = int(progress_ratio(puzzle) * 100)
        st.metric("Completamento", f"{percent}%")

    st.progress(progress_ratio(puzzle))

    controls1, controls2, controls3, controls4 = st.columns(4)
    with controls1:
        if st.button("💡 Hint", use_container_width=True):
            auto_place_one_tile(puzzle)
            if puzzle.solved:
                st.balloons()
            st.rerun()
    with controls2:
        if st.button("🔀 Reshuffle", use_container_width=True):
            start_new_game(puzzle.image_key, puzzle.grid_size)
            st.rerun()
    with controls3:
        if st.button("👁️ Toggle Preview", use_container_width=True):
            st.session_state.show_preview = not st.session_state.show_preview
            st.rerun()
    with controls4:
        if st.button("✅ Solve Demo", use_container_width=True):
            puzzle.tiles = list(range(len(puzzle.tiles)))
            puzzle.solved = True
            st.balloons()
            st.rerun()

    game_col, preview_col = st.columns([1.35, 0.9])

    with game_col:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        cols_per_row = puzzle.grid_size
        index = 0
        for _ in range(puzzle.grid_size):
            row_cols = st.columns(cols_per_row, gap="small")
            for col in row_cols:
                tile_id = puzzle.tiles[index]
                with col:
                    st.image(
                        tiles_img[tile_id],
                        use_container_width=True,
                        clamp=True,
                    )
                    btn_label = f"Tile {index + 1}"
                    if st.button(btn_label, key=f"tile_btn_{index}", use_container_width=True):
                        if puzzle.selected_idx is None:
                            puzzle.selected_idx = index
                        else:
                            if puzzle.selected_idx != index:
                                swap_tiles(puzzle, puzzle.selected_idx, index)
                                if puzzle.solved:
                                    st.balloons()
                            else:
                                puzzle.selected_idx = None
                        st.rerun()
                    st.markdown(
                        f'<div class="tile-label">{tile_caption(index, puzzle.selected_idx)}</div>',
                        unsafe_allow_html=True,
                    )
                index += 1
        st.markdown("</div>", unsafe_allow_html=True)

    with preview_col:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### Preview di riferimento")
        if st.session_state.show_preview:
            st.image(crop_square(load_image(puzzle.image_key)), use_container_width=True)
        else:
            st.info("Preview nascosta. Ottimo per aumentare la sfida e il focus.")
        st.markdown(
            f"""
            <div class="small-note">
                Hint usati: {puzzle.hints_used}<br>
                Difficoltà: {puzzle.grid_size}x{puzzle.grid_size}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_conversion_section() -> None:
    puzzle: PuzzleState = st.session_state.puzzle
    if not puzzle.solved:
        return

    st.markdown('<div class="section-title">3. Reward + conversione prodotto</div>', unsafe_allow_html=True)

    recommendations = get_product_recommendations(puzzle.image_key, max_items=3)
    primary = recommendations[0]

    st.success("Puzzle completato. Questo è il momento perfetto per mostrare il prodotto collegato al design appena ricostruito.")

    hero_left, hero_right = st.columns([1.15, 0.85])
    with hero_left:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown(f"### Hai sbloccato: {IMAGE_TITLES[puzzle.image_key]}")
        st.write(
            "L'utente ha appena investito attenzione sul pattern. Ora il CTA ha molto più senso perché il design è già diventato memorabile."
        )
        st.markdown(
            f'<a class="cta" href="{primary}" target="_blank">🛍️ Scopri il prodotto abbinato</a>',
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
        st.caption("Suggerimento CRO: mostra un micro-copy di reward come ‘Hai completato il design — ora indossalo / portalo con te’. ")
        st.markdown("</div>", unsafe_allow_html=True)

    with hero_right:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### Perché converte meglio")
        st.markdown(
            """
            - forte continuità tra gioco e shopping
            - CTA basata su un'immagine appena vista e ricomposta
            - picco emotivo subito dopo il completamento
            - possibilità di cross-sell con prodotti affini
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Prodotti consigliati")
    cols = st.columns(3)
    card_text = [
        "Best match diretto con l'artwork appena completato.",
        "Seconda opzione per utenti che preferiscono una categoria diversa.",
        "Cross-sell leggero per aumentare il valore medio dell'esperienza.",
    ]
    for idx, (col, url) in enumerate(zip(cols, recommendations)):
        with col:
            st.markdown(
                f"""
                <div class="product-card">
                    <div class="product-title">{pretty_slug(url)}</div>
                    <div class="product-copy">{card_text[idx]}</div>
                    <a class="cta" href="{url}" target="_blank">Apri prodotto</a>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_dev_notes() -> None:
    with st.expander("Note tecniche / implementazione"):
        st.markdown(
            textwrap.dedent(
                """
                ### Architettura consigliata

                - `assets/` contiene le immagini con il nome esatto della chiave (`web_purple.jpg`, `web_multicolor.png`, ecc.)
                - `app.py` contiene logica UI, stato del puzzle, split delle immagini e CTA prodotto
                - mapping `IMAGE_PRODUCT_MAP` collega ogni artwork a una URL principale di conversione

                ### Migliorie ad alto impatto

                1. **Tracking eventi**
                   - `puzzle_started`
                   - `hint_used`
                   - `puzzle_completed`
                   - `product_cta_clicked`

                2. **Reward reale**
                   - codice sconto dopo il completamento
                   - accesso a una collezione dedicata
                   - meccanica “completa 3 puzzle e sblocca bundle”

                3. **Ottimizzazioni UX**
                   - timer soft opzionale
                   - animazione di completamento
                   - progress state persistente per sessione
                   - pagina mobile-first con immagini compresse

                4. **Per produzione**
                   - aggiungi analytics (GA4 / Meta Pixel / PostHog)
                   - usa CDN o immagini ottimizzate
                   - collega il CTA a UTM diversi per artwork e difficulty
                   - A/B test tra `Solve + CTA diretto` e `Solve + coupon + CTA`
                """
            )
        )


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
        render_game_board()
        render_conversion_section()

    render_dev_notes()


if __name__ == "__main__":
    main()
