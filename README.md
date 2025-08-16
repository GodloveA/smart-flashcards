# Smart Flashcards from Lecture Notes

Turn raw notes into **Anki-ready flashcards** in seconds. Paste notes or upload a .txt/.md file → extract keyphrases → generate cloze/Q&A cards → edit → export CSV.

## Features
- RAKE keyphrase extraction
- Cloze (“fill-in-the-blank”) and simple Q&A generation
- Semantic dedupe using TF-IDF cosine similarity
- Streamlit UI with in-place editing
- CLI export for automation

## Quickstart (Windows, VS Code)
```powershell
# 1) Clone or create the folder, then:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2) Run the app
streamlit run web/app.py

# 3) (optional) CLI export
python generate.py --in data\sample_notes.txt --out cards.csv
