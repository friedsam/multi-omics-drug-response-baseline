# utils/conformal.py
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.base import clone

def split_conformal_regressor(base_model, X, y, X_test, alpha: float = 0.1, random_state: int = 0):
    """
    Return predictions and prediction intervals.
    - alpha = miscoverage rate (0.1 -> 90% intervals)
    """
    X_tr, X_cal, y_tr, y_cal = train_test_split(X, y, test_size=0.2, random_state=random_state)
    model = clone(base_model).fit(X_tr, y_tr)
    err = np.abs(y_cal - model.predict(X_cal))
    q = np.quantile(err, 1 - alpha)
    y_pred = model.predict(X_test)
    return y_pred, (y_pred - q, y_pred + q)

def split_conformal_classifier(base_model, X, y, X_test, alpha: float = 0.1, random_state: int = 0):
    """
    Return predictions + prediction sets.
    """
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_tr, X_cal, y_tr, y_cal = train_test_split(X, y_enc, test_size=0.2, random_state=random_state, stratify=y_enc)
    model = clone(base_model).fit(X_tr, y_tr)

    P_cal = model.predict_proba(X_cal)
    scores = 1 - P_cal[np.arange(len(y_cal)), y_cal]
    q = np.quantile(scores, 1 - alpha)

    P_test = model.predict_proba(X_test)
    sets = (1 - P_test) <= q  # bool matrix: which labels are in each set
    preds = P_test.argmax(axis=1)
    return le.inverse_transform(preds), sets, le