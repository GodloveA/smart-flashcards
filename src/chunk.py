import re
import nltk

_PUNKT = "tokenizers/punkt"
def _ensure_punkt():
    try:
        nltk.data.find(_PUNKT)
    except LookupError:
        nltk.download("punkt", quiet=True)

def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()

def split_sentences(text: str) -> list[str]:
    """Lightweight sentence splitter using NLTK punkt."""
    _ensure_punkt()
    from nltk.tokenize import sent_tokenize
    normalized = normalize_whitespace(text)
    sents = [s.strip() for s in sent_tokenize(normalized) if s.strip()]
    filtered = [s for s in sents if 2 <= len(s.split()) <= 40]
    return filtered
