import math
import random
from pathlib import Path
import time

import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(layout="wide")

# =========================
# CONFIG
# =========================
PRODUCTS = [
    "https://blululi.com/products/colorful-mandala-tote-bag-vibrant-boho-all-over-print-beach-market-tote",
    "https://blululi.com/collections/wall-art/products/mandala-art-drawn-by-hand-vertical-framed-poster-mindfulness-yoga-purple-mandala",
    "https://blululi.com/collections/t-shirts/products/rainbow-mandala-womens-t-shirt-colorful-art-1",
]

IMAGE_TITLES = {
    "web_purple": "Purple Mandala Serenity",
    "web_multicolor": "Multicolor Mandala Radiance",
    "web_orange_yellow": "Orange Yellow Mandala Sunrise",
}

ASSETS_DIR = Path("assets")
GRID_OPTIONS = [3, 4, 5]

# =========================
# HELPERS
# =========================
def load_image(path):
    img = Image.open(path).convert("RGB")
    img = ImageOps.exif_transpose(img)
    img = img.resize((900, 900))
    return img

def split_image(path, grid):
    img = load_image(path)
    size = 900 // grid
    tiles = []

    for r in range(grid):
        for c in range(grid):
            tiles.append(img.crop((c*size, r*size, (c+1)*size, (r+1)*size)))
    return tiles

def shuffled_order(n):
    order = list(range(n))
    while True:
        random.shuffle(order)
        if order != list(range(n)):
            return order

# =========================
# STATE
# =========================
if "image_key" not in st.session_state:
    st.session_state.image_key = list(IMAGE_TITLES.keys())[0]
    st.session_state.grid = 3
    st.session_state.order = None
    st.session_state.moves = 0
    st.session_state.start = None
    st.session_state.completed = False

# =========================
# GAME INIT
# =========================
def new_game():
    n = st.session_state.grid ** 2
    st.session_state.order = shuffled_order(n)
    st.session_state.moves = 0
    st.session_state.start = None
    st.session_state.completed = False

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("Setup")

    st.session_state.image_key = st.selectbox(
        "Design",
        list(IMAGE_TITLES.keys()),
        format_func=lambda x: IMAGE_TITLES[x]
    )

    st.session_state.grid = st.selectbox("Difficoltà", GRID_OPTIONS)

    if st.button("Nuova partita"):
        new_game()

# auto init
if st.session_state.order is None:
    new_game()

# =========================
# LOAD
# =========================
image_path = ASSETS_DIR / f"{st.session_state.image_key}.jpg"
tiles = split_image(image_path, st.session_state.grid)

# =========================
# UI
# =========================
st.title("🧩 Puzzle")

cols = st.columns(st.session_state.grid)
idx = 0

for r in range(st.session_state.grid):
    cols = st.columns(st.session_state.grid)
    for c in range(st.session_state.grid):
        tile_id = st.session_state.order[idx]

        with cols[c]:
            st.image(tiles[tile_id], use_container_width=True)

            if st.button("Swap", key=idx):
                if st.session_state.start is None:
                    st.session_state.start = time.time()

                if "selected" not in st.session_state:
                    st.session_state.selected = idx
                else:
                    i = st.session_state.selected
                    j = idx
                    st.session_state.order[i], st.session_state.order[j] = (
                        st.session_state.order[j],
                        st.session_state.order[i],
                    )
                    st.session_state.selected = None
                    st.session_state.moves += 1

        idx += 1

# =========================
# CHECK
# =========================
if st.session_state.order == list(range(len(tiles))):
    st.session_state.completed = True

# =========================
# METRICS
# =========================
if st.session_state.start:
    elapsed = int(time.time() - st.session_state.start)
else:
    elapsed = 0

st.write(f"⏱ Tempo: {elapsed}s")
st.write(f"🔁 Mosse: {st.session_state.moves}")

# =========================
# CONVERSION
# =========================
if st.session_state.completed:
    st.success("🎉 Hai sbloccato questo design!")

    product_url = PRODUCTS[0]

    st.markdown("### 👉 Ottieni questo design")
    st.markdown(f"[Vai al prodotto]({product_url})")
