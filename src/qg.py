from __future__ import annotations
from typing import List, Dict, Tuple
import re

def _first_sentence_containing(phrase: str, sentences: List[str]) -> tuple[int, str] | None:
    pattern = re.compile(rf"\b{re.escape(phrase)}\b", flags=re.IGNORECASE)
    for idx, s in enumerate(sentences):
        if pattern.search(s):
            return idx, s
    return None

def _make_cloze(sentence: str, phrase: str) -> str:
    pattern = re.compile(re.escape(phrase), flags=re.IGNORECASE)
    return pattern.sub("_____", sentence, count=1)

def make_cards(
    sentences: List[str],
    keyphrases: List[Tuple[str, float]],
    tag: str = "auto",
    max_cards: int = 50,
) -> List[Dict[str, str | float | int]]:
    """
    Build cards as dicts: {Front, Back, Tag, phrase_score, sent_idx}
    - Prefers cloze if phrase appears in a sentence.
    - Falls back to simple Q/A otherwise.
    """
    cards: List[Dict[str, str | float | int]] = []
    for phrase, score in keyphrases[:max_cards]:
        found = _first_sentence_containing(phrase, sentences)
        if found:
            idx, s = found
            front = _make_cloze(s, phrase)
            back = phrase
            cards.append({
                "Front": front,
                "Back": back,
                "Tag": tag,
                "phrase_score": score,
                "sent_idx": idx,
            })
        else:
            q = f"What is {phrase}?"
            context = sentences[0] if sentences else ""
            cards.append({
                "Front": q,
                "Back": context,
                "Tag": tag,
                "phrase_score": score * 0.5,  # penalize fallback
                "sent_idx": len(sentences) // 2 if sentences else 0,
            })
    return cards
