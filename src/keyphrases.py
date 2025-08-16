from __future__ import annotations
from typing import List, Tuple

import nltk
from rake_nltk import Rake

def _ensure_nltk():
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)

def extract_keyphrases(text: str, max_phrases: int = 30) -> List[Tuple[str, float]]:
    """Return list of (phrase, score) from RAKE, highest first."""
    _ensure_nltk()
    r = Rake(min_length=1, max_length=3)  # 1–3 word phrases
    r.extract_keywords_from_text(text)
    scored = r.get_ranked_phrases_with_scores()
    top = scored[:max_phrases]
    return [(phrase.strip(), float(score)) for score, phrase in top if phrase.strip()]
