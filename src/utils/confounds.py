# utils/confounds.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def residualize_features(X: pd.DataFrame, confounds: pd.DataFrame) -> pd.DataFrame:
    """
    Remove linear effects of confounds from each feature column in X.
    - X: features (samples × features)
    - confounds: DataFrame with categorical or numeric confound cols
    Returns: residualized copy of X
    """
    Z = pd.get_dummies(confounds, drop_first=True)
    X_res = X.copy()
    lr = LinearRegression()
    for col in X.columns:
        lr.fit(Z, X[col].values)
        X_res[col] = X[col].values - lr.predict(Z)
    return X_res

def combat_batch_correct(X: pd.DataFrame, batch: pd.Series) -> pd.DataFrame:
    """
    Wrapper for ComBat batch correction.
    Requires pycombat / neurocombat if installed.
    If not available, returns X unchanged.
    """
    try:
        from pycombat import Combat
        Xc = Combat().fit_transform(X.values, batch.values)
        return pd.DataFrame(Xc, index=X.index, columns=X.columns)
    except Exception:
        print("[confounds] ComBat not available, returning uncorrected X")
        return X