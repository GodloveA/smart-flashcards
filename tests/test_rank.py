from src.rank import dedupe_cards

def test_dedupe():
    cards = [
        {"Front": "What is TCP?", "Back": "Transport protocol", "Tag": "net"},
        {"Front": "What is TCP", "Back": "Transport protocol", "Tag": "net"},
        {"Front": "Explain UDP.", "Back": "Connectionless protocol", "Tag": "net"},
    ]
    out = dedupe_cards(cards, sim_threshold=0.8)
    assert len(out) == 2
