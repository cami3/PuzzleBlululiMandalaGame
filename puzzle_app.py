from __future__ import annotations

import csv
import random
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

import streamlit as st
from PIL import Image, ImageDraw


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Mandala Puzzle Shop",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)

ASSETS_DIR = Path("assets")
DATA_DIR = Path("data")
EVENTS_FILE = DATA_DIR / "events.csv"

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


# =========================
# STYLES
# =========================

st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(180deg, #0f1020 0%, #15172d 100%);
        }
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1250px;
        }
        .hero {
            padding: 1.4rem 1.6rem;
            border-radius: 22px;
            background:
                radial-gradient(circle at top right, rgba(170,120,255,0.28), transparent 30%),
                radial-gradient(circle at bottom left, rgba(255,160,80,0.18), transparent 30%),
                linear-gradient(135deg, #1a1d38 0%, #111428 100%);
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 12px 40px rgba(0,0,0,0.22);
            margin-bottom: 1rem;
        }
        .hero h1 {
            margin: 0;
            font-size: 2.2rem;
            line-height: 1.1;
        }
        .hero p {
            margin-top: 0.55rem;
            color: #cfd3ea;
            font-size: 1rem;
        }
        .soft-card {
            border-radius: 20px;
            padding: 1rem 1.1rem;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
        }
        .cta-card {
            border-radius: 22px;
            padding: 1.1rem 1.2rem;
            background: linear-gradient(135deg, rgba(128,95,255,0.20), rgba(255,145,77,0.14));
            border: 1px solid rgba(255,255,255,0.10);
        }
        .small-muted {
            color: #aab1d6;
            font-size: 0.93rem;
        }
        .title-pill {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.10);
            font-size: 0.85rem;
            color: #d8defd;
            margin-bottom: 0.75rem;
        }
        .reward {
            padding: 0.85rem 1rem;
            border-radius: 16px;
            background: rgba(67, 201, 133, 0.12);
            border: 1px solid rgba(67, 201, 133, 0.35);
            color: #dffaea;
            font-weight: 600;
        }
        .warn {
            padding: 0.85rem 1rem;
            border-radius: 16px;
            background: rgba(255, 193, 7, 0.08);
            border: 1px solid rgba(255, 193, 7, 0.30);
            color: #fff1c1;
            font-weight: 500;
        }
        .grid-note {
            font-size: 0.92rem;
            color: #b8bedf;
            margin-top: 0.2rem;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.3rem;
        }
        .stButton > button {
            border-radius: 14px;
            min-height: 44px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# DATA MODEL
# =========================

@dataclass
class CatalogItem:
    key: str
    title: str
    image_path: Path
    product_url: str


# =========================
# HELPERS
# =========================

def ensure_dirs() -> None:
    DATA_DIR.mkdir(exist_ok=True, parents=True)


def append_utm(url: str, source: str = "streamlit", medium: str = "puzzle", campaign: str = "mandala_game") -> str:
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query))
    query.update(
        {
            "utm_source": source,
            "utm_medium": medium,
            "utm_campaign": campaign,
        }
    )
    return urlunparse(parsed._replace(query=urlencode(query)))


def product_name_from_url(url: str) -> str:
    slug = url.rstrip("/").split("/")[-1]
    slug = slug.replace("-", " ")
    return slug.title()


def find_image_file(image_key: str) -> Optional[Path]:
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        candidate = ASSETS_DIR / f"{image_key}{ext}"
        if candidate.exists():
            return candidate
    return None


def build_catalog() -> List[CatalogItem]:
    catalog: List[CatalogItem] = []

    product_pool = list(products)
    if not product_pool:
        raise ValueError("La lista 'products' è vuota.")

    keys = list(IMAGE_TITLES.keys())
    for idx, key in enumerate(keys):
        img_path = find_image_file(key)
        if img_path is None:
            # Salta in modo robusto se manca un'immagine
            continue

        # Associazione semplice: per indice, con fallback circolare
        product_url = product_pool[idx % len(product_pool)]

        catalog.append(
            CatalogItem(
                key=key,
                title=IMAGE_TITLES[key],
                image_path=img_path,
                product_url=product_url,
            )
        )

    return catalog


def init_state(catalog: List[CatalogItem]) -> None:
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]

    if "catalog" not in st.session_state:
        st.session_state.catalog = catalog

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "rounds_played" not in st.session_state:
        st.session_state.rounds_played = 0

    if "clickouts" not in st.session_state:
        st.session_state.clickouts = 0

    if "current_item" not in st.session_state:
        st.session_state.current_item = random.choice(catalog)

    if "revealed_tiles" not in st.session_state:
        st.session_state.revealed_tiles = set()

    if "solved" not in st.session_state:
        st.session_state.solved = False

    if "attempted" not in st.session_state:
        st.session_state.attempted = False

    if "used_hint" not in st.session_state:
        st.session_state.used_hint = False

    if "last_guess" not in st.session_state:
        st.session_state.last_guess = None


def reset_round(catalog: List[CatalogItem]) -> None:
    st.session_state.current_item = random.choice(catalog)
    st.session_state.revealed_tiles = set()
    st.session_state.solved = False
    st.session_state.attempted = False
    st.session_state.used_hint = False
    st.session_state.last_guess = None


def log_event(event_type: str, payload: Dict[str, str | int | float]) -> None:
    ensure_dirs()
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": st.session_state.session_id,
        "event_type": event_type,
        **payload,
    }

    file_exists = EVENTS_FILE.exists()
    with open(EVENTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def create_masked_puzzle(
    image_path: Path,
    rows: int,
    cols: int,
    revealed_tiles: set[int],
    overlay_alpha: int = 210,
) -> Image.Image:
    img = Image.open(image_path).convert("RGBA")

    # Uniforma l'immagine per una resa migliore
    target_width = 900
    ratio = target_width / img.width
    target_height = int(img.height * ratio)
    img = img.resize((target_width, target_height), Image.LANCZOS)

    tile_w = img.width / cols
    tile_h = img.height / rows

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    total_tiles = rows * cols
    for tile_index in range(total_tiles):
        if tile_index in revealed_tiles:
            continue
        r = tile_index // cols
        c = tile_index % cols

        x1 = int(c * tile_w)
        y1 = int(r * tile_h)
        x2 = int((c + 1) * tile_w)
        y2 = int((r + 1) * tile_h)

        draw.rectangle([x1, y1, x2, y2], fill=(8, 10, 22, overlay_alpha))
        draw.rounded_rectangle(
            [x1 + 4, y1 + 4, x2 - 4, y2 - 4],
            radius=14,
            outline=(255, 255, 255, 90),
            width=2,
        )

    composed = Image.alpha_composite(img, overlay)
    return composed.convert("RGB")


def reveal_random_tiles(rows: int, cols: int, count: int = 1) -> None:
    total_tiles = rows * cols
    all_tiles = set(range(total_tiles))
    hidden = list(all_tiles - st.session_state.revealed_tiles)
    if not hidden:
        return

    for tile in random.sample(hidden, min(count, len(hidden))):
        st.session_state.revealed_tiles.add(tile)


def build_options(correct_title: str, all_titles: List[str], n_options: int = 4) -> List[str]:
    wrong = [t for t in all_titles if t != correct_title]
    sampled_wrong = random.sample(wrong, k=min(n_options - 1, len(wrong)))
    options = sampled_wrong + [correct_title]
    random.shuffle(options)
    return options


def score_for_round(total_tiles: int, revealed_count: int, used_hint: bool) -> int:
    hidden_left = max(total_tiles - revealed_count, 0)
    base = 40 + hidden_left * 8
    if used_hint:
        base -= 20
    return max(base, 10)


def get_discount_code(score: int) -> str:
    if score >= 600:
        return "MANDALA20"
    if score >= 300:
        return "MANDALA15"
    return "MANDALA10"


# =========================
# LOAD
# =========================

ensure_dirs()
catalog = build_catalog()

if not catalog:
    st.error(
        "Non ho trovato immagini valide nella cartella `assets/`."
        " Aggiungi i file con gli stessi nomi delle chiavi di IMAGE_TITLES."
    )
    st.stop()

init_state(catalog)


# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.markdown("## ⚙️ Game settings")

    difficulty = st.selectbox(
        "Difficulty",
        options=["Easy", "Medium", "Hard"],
        index=1,
    )

    if difficulty == "Easy":
        rows, cols = 3, 3
    elif difficulty == "Medium":
        rows, cols = 4, 4
    else:
        rows, cols = 5, 5

    total_tiles = rows * cols

    st.markdown("---")
    st.markdown("### 📈 Session stats")
    st.metric("Score", st.session_state.score)
    st.metric("Rounds", st.session_state.rounds_played)
    st.metric("Product clicks", st.session_state.clickouts)

    st.markdown("---")
    st.markdown(
        """
        **Conversion logic**
        - puzzle + reveal progress
        - reward finale
        - CTA prodotto collegata all'opera
        - tracking click su CSV locale
        """
    )

    if st.button("🔄 New round", use_container_width=True):
        reset_round(catalog)
        st.rerun()


# =========================
# HERO
# =========================

st.markdown(
    """
    <div class="hero">
        <div class="title-pill">Puzzle Commerce Experience</div>
        <h1>Scopri l’opera. Vinci il reveal. Vai al prodotto.</h1>
        <p>
            Un mini-game pensato per aumentare attenzione, tempo sulla pagina e click verso il catalogo.
            Più risolvi velocemente, più alto è il reward.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

top1, top2, top3 = st.columns(3)
with top1:
    st.metric("Difficulty", difficulty)
with top2:
    revealed = len(st.session_state.revealed_tiles)
    st.metric("Tiles revealed", f"{revealed}/{total_tiles}")
with top3:
    hidden_left = total_tiles - len(st.session_state.revealed_tiles)
    st.metric("Mystery left", hidden_left)

st.markdown("")


# =========================
# CURRENT ROUND
# =========================

item: CatalogItem = st.session_state.current_item
all_titles = [c.title for c in catalog]

left, right = st.columns([1.35, 1], gap="large")

with left:
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.subheader("🧩 Puzzle Board")

    puzzle_img = create_masked_puzzle(
        image_path=item.image_path,
        rows=rows,
        cols=cols,
        revealed_tiles=st.session_state.revealed_tiles,
    )
    st.image(puzzle_img, use_container_width=True)
    st.markdown(
        '<div class="grid-note">Scopri tessere e poi indovina il titolo corretto.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("#### Reveal tiles")

    # Griglia pulsanti per scoprire singole tessere
    for r in range(rows):
        cols_ui = st.columns(cols)
        for c in range(cols):
            idx = r * cols + c
            label = "✓" if idx in st.session_state.revealed_tiles else f"{idx + 1}"
            disabled = idx in st.session_state.revealed_tiles or st.session_state.solved
            with cols_ui[c]:
                if st.button(label, key=f"tile_{idx}", disabled=disabled, use_container_width=True):
                    st.session_state.revealed_tiles.add(idx)
                    log_event(
                        "tile_revealed",
                        {
                            "image_key": item.key,
                            "image_title": item.title,
                            "tile_index": idx,
                            "difficulty": difficulty,
                        },
                    )
                    st.rerun()

    reveal_col1, reveal_col2 = st.columns(2)
    with reveal_col1:
        if st.button("✨ Reveal 2 random tiles", use_container_width=True, disabled=st.session_state.solved):
            reveal_random_tiles(rows, cols, count=2)
            st.session_state.used_hint = True
            log_event(
                "hint_used",
                {
                    "image_key": item.key,
                    "image_title": item.title,
                    "difficulty": difficulty,
                },
            )
            st.rerun()

    with reveal_col2:
        if st.button("👀 Reveal all", use_container_width=True, disabled=st.session_state.solved):
            st.session_state.revealed_tiles = set(range(total_tiles))
            st.session_state.used_hint = True
            log_event(
                "reveal_all",
                {
                    "image_key": item.key,
                    "image_title": item.title,
                    "difficulty": difficulty,
                },
            )
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.subheader("🎯 Guess the artwork")

    options = build_options(item.title, all_titles, n_options=4)

    guess = st.radio(
        "Which title matches the image?",
        options=options,
        index=None,
        key=f"guess_{item.key}_{len(st.session_state.revealed_tiles)}",
    )

    submit_col1, submit_col2 = st.columns(2)

    with submit_col1:
        submitted = st.button("Submit answer", use_container_width=True, disabled=st.session_state.solved)

    with submit_col2:
        skip_round = st.button("Skip round", use_container_width=True)

    if skip_round:
        log_event(
            "round_skipped",
            {
                "image_key": item.key,
                "image_title": item.title,
                "difficulty": difficulty,
            },
        )
        reset_round(catalog)
        st.rerun()

    if submitted:
        if not guess:
            st.warning("Seleziona una risposta prima di inviare.")
        else:
            st.session_state.attempted = True
            st.session_state.last_guess = guess

            if guess == item.title:
                points = score_for_round(
                    total_tiles=total_tiles,
                    revealed_count=len(st.session_state.revealed_tiles),
                    used_hint=st.session_state.used_hint,
                )
                st.session_state.score += points
                st.session_state.rounds_played += 1
                st.session_state.solved = True

                log_event(
                    "round_solved",
                    {
                        "image_key": item.key,
                        "image_title": item.title,
                        "difficulty": difficulty,
                        "points": points,
                        "revealed_tiles": len(st.session_state.revealed_tiles),
                        "used_hint": int(st.session_state.used_hint),
                    },
                )

                st.success(f"Corretto. Hai guadagnato {points} punti.")
                st.balloons()
            else:
                st.error("Non è il titolo giusto. Scopri altre tessere e riprova.")
                log_event(
                    "wrong_guess",
                    {
                        "image_key": item.key,
                        "image_title": item.title,
                        "difficulty": difficulty,
                        "guess": guess,
                    },
                )

    if st.session_state.solved:
        tracked_url = append_utm(
            item.product_url,
            source="streamlit",
            medium="puzzle",
            campaign=item.key,
        )
        reward_code = get_discount_code(st.session_state.score)

        st.markdown("---")
        st.markdown('<div class="cta-card">', unsafe_allow_html=True)
        st.markdown("### ✅ Puzzle solved")
        st.markdown(f"**Artwork:** {item.title}")
        st.markdown(f"**Suggested product:** {product_name_from_url(item.product_url)}")

        st.markdown(
            f'<div class="reward">Reward unlocked: use code <code>{reward_code}</code> at checkout</div>',
            unsafe_allow_html=True,
        )
        st.markdown("")

        cta_col1, cta_col2 = st.columns([1, 1])

        with cta_col1:
            if st.link_button("🛍️ Shop this design", tracked_url, use_container_width=True):
                st.session_state.clickouts += 1
                log_event(
                    "product_click",
                    {
                        "image_key": item.key,
                        "image_title": item.title,
                        "product_url": tracked_url,
                        "difficulty": difficulty,
                    },
                )

        with cta_col2:
            if st.button("➡️ Next puzzle", use_container_width=True):
                reset_round(catalog)
                st.rerun()

        st.markdown(
            """
            <p class="small-muted">
                Questo blocco è il cuore conversionale: reward immediato, associazione opera-prodotto,
                CTA unica e tracking della visita.
            </p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("---")
        st.markdown(
            """
            <div class="warn">
                Suggerimento: meno tessere scopri, più alto sarà il punteggio finale.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# PRODUCT STRIP
# =========================

st.markdown("")
st.subheader("🛒 More products you can push after the game")

sample_products = random.sample(products, k=min(4, len(products)))
prod_cols = st.columns(len(sample_products))

for i, url in enumerate(sample_products):
    with prod_cols[i]:
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.markdown(f"**{product_name_from_url(url)}**")
        tracked = append_utm(url, source="streamlit", medium="post_game_strip", campaign="catalog_strip")
        st.caption("Extra catalog exposure after engagement")
        if st.link_button("Open product", tracked, use_container_width=True):
            st.session_state.clickouts += 1
            log_event(
                "catalog_strip_click",
                {
                    "product_url": tracked,
                },
            )
        st.markdown("</div>", unsafe_allow_html=True)


# =========================
# FOOTER / DEBUG
# =========================

with st.expander("Advanced notes for optimization"):
    st.markdown(
        """
        **Cose da testare per aumentare conversioni:**
        - reward progressivo: 10%, 15%, 20%
        - uscita verso prodotto singolo vs collezione
        - reveal automatico dopo pochi secondi
        - leaderboard o streak
        - pixel / analytics esterni
        - email capture dopo il primo puzzle risolto
        - A/B test su CTA e copy
        """
    )

    st.markdown(
        f"""
        **Session ID:** `{st.session_state.session_id}`  
        **Tracking file:** `{EVENTS_FILE}`
        """
    )
