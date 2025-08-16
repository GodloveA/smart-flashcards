# Smart Flashcards from Lecture Notes

A small tool that turns class notes into flashcards you can import into Anki. Paste text or upload a .txt/.md file—the app finds key terms, builds fill-in-the-blank or Q&A cards, lets you edit them, and exports a CSV.

## What it does
- Finds important terms (RAKE keyphrase extraction).
- Creates cloze (fill-in-the-blank) and simple Q&A cards.
- Removes near-duplicate cards using TF-IDF similarity.
- Simple Streamlit web UI with in-place editing.
- Command-line script for batch export.

## Get started (Windows + VS Code)
```powershell
# 1) Create and activate a virtual environment, then install deps
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2) Run the web app
streamlit run web/app.py

# 3) Optional: generate a CSV from a file via CLI
python generate.py --in data\sample_notes.txt --out cards.csv
