# utils/ood.py
from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Iterator, Tuple
from sklearn.covariance import EmpiricalCovariance

def leave_tissue_out_splits(df: pd.DataFrame, tissue_col: str = "tissue"
) -> Iterator[Tuple[str, np.ndarray, np.ndarray]]:
    """
    Yield (held_out_tissue, train_idx, test_idx) for each unique tissue.
    train_idx/test_idx are integer index arrays usable to slice df / X / y.
    """
    tissues = pd.Index(df[tissue_col].astype(str).unique())
    for t in tissues:
        test_idx = np.where(df[tissue_col].astype(str).values == t)[0]
        train_idx = np.where(df[tissue_col].astype(str).values != t)[0]
        if len(test_idx) == 0 or len(train_idx) == 0:
            continue
        yield str(t), train_idx, test_idx

def mahalanobis_scores(X_train: np.ndarray, X_test: np.ndarray) -> np.ndarray:
    """
    Fit an empirical Gaussian model on X_train and return Mahalanobis distance
    for each row in X_test. Larger = more OOD-like.
    """
    if not isinstance(X_train, np.ndarray): X_train = np.asarray(X_train)
    if not isinstance(X_test, np.ndarray):  X_test  = np.asarray(X_test)
    cov = EmpiricalCovariance().fit(X_train)
    # sklearn returns squared distances; keep sqrt for interpretability
    d2 = cov.mahalanobis(X_test)
    return np.sqrt(d2)

def ood_threshold_from_train(X_train: np.ndarray, quantile: float = 0.95) -> float:
    """
    Convenience: compute a distance threshold using train self-distances
    (leave-one-out approximation) to flag OOD at a chosen quantile.
    """
    if not isinstance(X_train, np.ndarray): X_train = np.asarray(X_train)
    cov = EmpiricalCovariance().fit(X_train)
    d2_self = cov.mahalanobis(X_train)  # squared
    return float(np.sqrt(np.quantile(d2_self, quantile)))