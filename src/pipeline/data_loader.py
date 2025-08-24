# pipeline/data_loader.py
from pathlib import Path
import pandas as pd

REQ = ["sample_id", "tissue", "batch", "y"]

def load_tcga(path: str) -> pd.DataFrame:
    """TCGA loader (RNA-seq + clinical + labels)."""
    p = Path(path)
    expr = pd.read_csv(p / "expression.csv")
    clin = pd.read_csv(p / "clinical.csv")
    lab  = pd.read_csv(p / "labels.csv")
    df = expr.merge(clin, on="sample_id").merge(lab, on="sample_id")
    if "batch" not in df: df["batch"] = "none"
    for c in REQ:
        if c not in df: raise ValueError(f"[tcga] missing {c}")
    return df

def load_gdsc(path: str) -> pd.DataFrame:
    """GDSC loader (features + meta + response)."""
    p = Path(path)
    feats = pd.read_csv(p / "features.csv")
    meta  = pd.read_csv(p / "meta.csv")
    resp  = pd.read_csv(p / "response.csv")
    df = feats.merge(meta, on="sample_id").merge(resp, on="sample_id")
    if "batch" not in df: df["batch"] = "none"
    for c in REQ:
        if c not in df: raise ValueError(f"[gdsc] missing {c}")
    return df

def load_ctrp(path: str) -> pd.DataFrame:
    """CTRP loader (same schema as GDSC)."""
    return load_gdsc(path)

def load_lincs(path: str) -> pd.DataFrame:
    """LINCS loader (signatures + meta + response)."""
    p = Path(path)
    sig  = pd.read_csv(p / "signatures.csv")
    meta = pd.read_csv(p / "meta.csv")
    resp = pd.read_csv(p / "response.csv")
    df = sig.merge(meta, on="sample_id").merge(resp, on="sample_id")
    if "batch" not in df: df["batch"] = "none"
    for c in REQ:
        if c not in df: raise ValueError(f"[lincs] missing {c}")
    return df

def load_by_track(track: str, path: str) -> pd.DataFrame:
    """Dispatch loader by track name."""
    track = track.lower()
    if track == "tcga":  return load_tcga(path)
    if track == "gdsc":  return load_gdsc(path)
    if track == "ctrp":  return load_ctrp(path)
    if track == "lincs": return load_lincs(path)
    raise ValueError(f"Unknown track: {track}")