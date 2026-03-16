import base64
import io
import json
from pathlib import Path

import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Blululi Puzzle Studio",
    page_icon="🧩",
    layout="wide",
)

st.markdown(
    """
    <style>
    header, footer { visibility: hidden !important; }
    [data-testid="stToolbar"],
    [data-testid="stHeader"],
    [data-testid="stStatusWidget"],
    [data-testid="stDecoration"] {
        display: none !important;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
    }

    [data-testid="stAppViewBlockContainer"],
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }

    iframe {
        border: 0 !important;
        display: block !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

IMAGE_FOLDER = Path("images")
HTML_FILE = Path("puzzle_app.html")


PRODUCTS = [
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
    "https://blululi.com/products/colorful-mandala-tote-bag-vibrant-boho-all-over-print-beach-market-tote",
    "https://blululi.com/products/colorful-mandala-tote-bag-boho-psychedelic-all-over-print",
]


def image_to_data_uri(path: Path, max_dim: int = 1200, quality: int = 85) -> dict[str, str]:
    with Image.open(path) as src:
        img = src.convert("RGB")
        img.thumbnail((max_dim, max_dim))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)

    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    return {
        "name": path.stem.replace("_", " ").replace("-", " ").title(),
        "url": f"data:image/jpeg;base64,{encoded}",
    }


def build_assets(folder: Path) -> list[dict[str, str]]:
    valid_suffixes = {".png", ".jpg", ".jpeg", ".webp"}
    image_paths = sorted(p for p in folder.iterdir() if p.suffix.lower() in valid_suffixes)
    return [image_to_data_uri(p) for p in image_paths]


if not IMAGE_FOLDER.exists() or not IMAGE_FOLDER.is_dir():
    st.error("Folder ./images not found")
    st.stop()

if not HTML_FILE.exists():
    st.error("Missing puzzle_app.html")
    st.stop()

assets = build_assets(IMAGE_FOLDER)

if not assets:
    st.error("No images found inside ./images")
    st.stop()

html_template = HTML_FILE.read_text(encoding="utf-8")
html = (
    html_template
    .replace("__ASSETS_JSON__", json.dumps(assets))
    .replace("__PRODUCTS_JSON__", json.dumps(PRODUCTS))
)

st.components.v1.html(
    html,
    height=1600,
    scrolling=True,
)
