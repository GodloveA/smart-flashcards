from src.chunk import split_sentences

def test_split_basic():
    text = "Hello world. This is a test! Short. This one is definitely long enough to be included."
    sents = split_sentences(text)
    assert any("Hello world." in s for s in sents)
    assert not any(s.strip() == "Short." for s in sents)
