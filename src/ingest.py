from pathlib import Path

def read_text_from_path(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No such file: {path}")
    if p.suffix.lower() in {".txt", ".md"}:
        return p.read_text(encoding="utf-8", errors="ignore")
    return p.read_text(encoding="utf-8", errors="ignore")
