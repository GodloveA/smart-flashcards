from __future__ import annotations
from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def score_cards(cards: List[Dict], total_sents: int) -> List[Dict]:
    """Combine phrase score and sentence position (earlier gets slight boost)."""
    for c in cards:
        pos = c.get("sent_idx", 0)
        position_bonus = 1.0 / (1.0 + (pos if total_sents == 0 else pos / max(1, total_sents)))
        c["score"] = float(c.get("phrase_score", 0.0) + 0.15 * position_bonus)
    return sorted(cards, key=lambda d: d["score"], reverse=True)

def dedupe_cards(cards: List[Dict], sim_threshold: float = 0.85) -> List[Dict]:
    """Remove near-duplicate 'Front' texts using TF-IDF cosine similarity."""
    if not cards:
        return []
    fronts = [c["Front"] for c in cards]
    vec = TfidfVectorizer(ngram_range=(1,2), min_df=1).fit_transform(fronts)
    sim = cosine_similarity(vec)
    keep = []
    removed = set()
    for i in range(len(cards)):
        if i in removed:
            continue
        keep.append(cards[i])
        for j in range(i+1, len(cards)):
            if sim[i, j] >= sim_threshold:
                removed.add(j)
    return keep
