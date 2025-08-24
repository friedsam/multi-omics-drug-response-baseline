from pathlib import Path
import joblib

ARTIFACT_DIR = Path("artifacts")
MODEL_FILE = ARTIFACT_DIR / "model.joblib"
FEATS_FILE = ARTIFACT_DIR / "features.joblib"

def save_model(model, feature_names):
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_FILE)
    joblib.dump(feature_names, FEATS_FILE)

def load_model():
    return joblib.load(MODEL_FILE), joblib.load(FEATS_FILE)