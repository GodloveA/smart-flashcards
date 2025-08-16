import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path: sys.path.insert(0, ROOT)

import io
import pandas as pd
import streamlit as st

from src.chunk import split_sentences
from src.keyphrases import extract_keyphrases
from src.qg import make_cards
from src.rank import score_cards, dedupe_cards

st.set_page_config(page_title="Smart Flashcards", page_icon="🃏", layout="centered")

st.title("🃏 Smart Flashcards from Lecture Notes")
st.caption("Paste notes or upload a .txt/.md file → generate editable flashcards → export CSV")

with st.sidebar:
    st.header("⚙️ Settings")
    max_phrases = st.slider("Max keyphrases", 5, 100, 30, 5)
    max_cards = st.slider("Max cards", 5, 100, 40, 5)
    dedupe_thresh = st.slider("Deduplicate threshold", 0.50, 0.99, 0.85, 0.01)
    tag = st.text_input("Default tag", value="notes")

uploaded = st.file_uploader("Upload a .txt or .md file", type=["txt", "md"])
text_default = """Paste your notes here, or upload a file from the control above.

Tips:
- Keep sentences reasonably short (8–40 words).
- Headings and bullets are fine; the app will filter noisy lines.
- Try the sample in data/sample_notes.txt for a quick demo.
"""
text = st.text_area("Notes", value=text_default, height=220)

col1, col2 = st.columns(2)
with col1:
    gen_btn = st.button("✨ Generate Cards", type="primary")
with col2:
    clear_btn = st.button("Clear")

if clear_btn:
    st.experimental_rerun()

if gen_btn:
    if uploaded is not None:
        # Uploaded file takes precedence
        text = uploaded.read().decode("utf-8", errors="ignore")

    if not text or text.strip() == "":
        st.error("Please provide some notes (paste or upload).")
        st.stop()

    with st.spinner("Processing…"):
        sents = split_sentences(text)
        phrases = extract_keyphrases(text, max_phrases=max_phrases)
        cards = make_cards(sents, phrases, tag=tag, max_cards=max_cards)
        cards = score_cards(cards, total_sents=len(sents))
        cards = dedupe_cards(cards, sim_threshold=dedupe_thresh)

        df = pd.DataFrame(cards)[["Front", "Back", "Tag"]]
        st.success(f"Generated {len(df)} cards")

        edited = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            key="editor",
            column_config={
                "Front": st.column_config.TextColumn(width="large"),
                "Back": st.column_config.TextColumn(width="large"),
                "Tag": st.column_config.TextColumn(width="medium"),
            },
        )

        csv_bytes = edited.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download CSV",
            data=csv_bytes,
            file_name="cards.csv",
            mime="text/csv",
        )

        with st.expander("Preview first 5 cards"):
            st.table(edited.head(5))
