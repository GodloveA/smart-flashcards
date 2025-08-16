import pandas as pd
from pathlib import Path

def export_csv(cards, out_path: str) -> str:
    df = pd.DataFrame(cards)[["Front", "Back", "Tag"]]
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False, encoding="utf-8")
    return str(out.resolve())
