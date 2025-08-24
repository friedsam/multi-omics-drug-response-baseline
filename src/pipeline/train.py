
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingRegressor
from utils.confounds import residualize_features
from pipeline.data_loader import load_by_track

def train_one_run(cfg: dict):
    # 1) data
    path = cfg.get("path") or f"data/{cfg['track']}/"
    df = load_by_track(cfg["track"], path)

    # 2) split features/labels
    y = df["y"].values
    X = df.drop(columns=["sample_id","y"]).copy()
    conf_cols = cfg["confounds"].get("confound_cols", [])
    conf_df = df[conf_cols] if conf_cols else pd.DataFrame(index=df.index)

    # 3) optional deconfounding (linear residualization baseline)
    if cfg["confounds"].get("use_residualize", False) and not conf_df.empty:
        X = residualize_features(X, conf_df)

    # 4) train/val split
    X_train, X_test, y_train, y_test = train_test_split(X.values, y, test_size=0.2, random_state=42, stratify=None if cfg["endpoint"]=="regression" else y)

    # 5) model by endpoint
    if cfg["endpoint"] == "binary":
        model = LogisticRegression(max_iter=200)
        model.fit(X_train, y_train)
        y_prob = model.predict_proba(X_test)[:,1]
        metric = roc_auc_score(y_test, y_prob)
        return {"metric_name":"auroc", "metric": float(metric)}
    else:
        model = GradientBoostingRegressor()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metric = r2_score(y_test, y_pred)
        return {"metric_name":"r2", "metric": float(metric)}