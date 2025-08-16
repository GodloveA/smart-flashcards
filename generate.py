import argparse
from src.ingest import read_text_from_path
from src.chunk import split_sentences
from src.keyphrases import extract_keyphrases
from src.qg import make_cards
from src.rank import score_cards, dedupe_cards
from src.exporter import export_csv

def main():
    ap = argparse.ArgumentParser(description="Generate flashcards from notes.")
    ap.add_argument("--in", dest="in_path", required=True, help="Input .txt/.md")
    ap.add_argument("--out", dest="out_path", required=True, help="Output CSV path")
    ap.add_argument("--max_phrases", type=int, default=30)
    ap.add_argument("--max_cards", type=int, default=50)
    ap.add_argument("--dedupe", type=float, default=0.85, help="Cosine sim threshold (0-1)")
    args = ap.parse_args()

    text = read_text_from_path(args.in_path)
    sents = split_sentences(text)
    phrases = extract_keyphrases(text, max_phrases=args.max_phrases)
    cards = make_cards(sents, phrases, tag="cli", max_cards=args.max_cards)
    cards = score_cards(cards, total_sents=len(sents))
    cards = dedupe_cards(cards, sim_threshold=args.dedupe)
    out = export_csv(cards, args.out_path)
    print(f"✅ Wrote {len(cards)} cards to {out}")

if __name__ == "__main__":
    main()
