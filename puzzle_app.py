import streamlit as st
import random
from PIL import Image

st.set_page_config(layout="centered")

# -------- DATI --------
IMAGE_TITLES = {
    "web_purple": "Purple Mandala Serenity",
    "web_multicolor": "Multicolor Mandala Radiance",
}

products = [
    "https://blululi.com/products/colorful-mandala-tote-bag-vibrant-boho-all-over-print-beach-market-tote",
    "https://blululi.com/collections/wall-art/products/mandala-art-drawn-by-hand-vertical-framed-poster-mindfulness-yoga-purple-mandala",
]

IMAGE_PRODUCT_MAP = {
    "web_purple": products[1],
    "web_multicolor": products[0],
}

# -------- INIT --------
if "tiles" not in st.session_state:
    st.session_state.tiles = []
    st.session_state.selected = None
    st.session_state.image = "web_purple"

# -------- FUNZIONI --------
def load_image(name):
    return Image.open(f"assets/{name}.jpg")

def split_image(img, grid=3):
    w, h = img.size
    tile_w = w // grid
    tiles = []

    for y in range(grid):
        for x in range(grid):
            crop = img.crop((x*tile_w, y*tile_w, (x+1)*tile_w, (y+1)*tile_w))
            tiles.append(crop)

    return tiles

def start_game():
    img = load_image(st.session_state.image)
    st.session_state.original_tiles = split_image(img)
    st.session_state.tiles = list(range(len(st.session_state.original_tiles)))
    random.shuffle(st.session_state.tiles)
    st.session_state.selected = None

def swap(a, b):
    st.session_state.tiles[a], st.session_state.tiles[b] = st.session_state.tiles[b], st.session_state.tiles[a]

def is_solved():
    return st.session_state.tiles == list(range(len(st.session_state.tiles)))

# -------- UI --------
st.title("🧩 Puzzle Mandala")

image_choice = st.selectbox(
    "Scegli immagine",
    list(IMAGE_TITLES.keys()),
    format_func=lambda x: IMAGE_TITLES[x]
)

st.session_state.image = image_choice

if st.button("Start"):
    start_game()

# -------- GAME --------
if st.session_state.tiles:

    grid = 3
    tiles = st.session_state.original_tiles

    idx = 0
    for r in range(grid):
        cols = st.columns(grid)
        for c in range(grid):
            tile_id = st.session_state.tiles[idx]

            with cols[c]:
                st.image(tiles[tile_id])

                if st.button("Select", key=idx):
                    if st.session_state.selected is None:
                        st.session_state.selected = idx
                    else:
                        swap(st.session_state.selected, idx)
                        st.session_state.selected = None
                        st.rerun()

            idx += 1

    if is_solved():
        st.success("Puzzle completato!")

        url = IMAGE_PRODUCT_MAP[st.session_state.image]

        st.markdown(f"[👉 Vai al prodotto]({url})")
