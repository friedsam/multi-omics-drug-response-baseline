from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np
import shap
from app.models.registry import load_model

router = APIRouter(prefix="/explain", tags=["explain"])

class ExplainRequest(BaseModel):
    features: dict   # {feature_name: value}
    top_k: int = 10

@router.post("")
def explain(req: ExplainRequest):
    model, feature_names = load_model()  # you’ll save these after training
    x = np.array([[req.features.get(f, 0.0) for f in feature_names]])

    try:
        explainer = shap.TreeExplainer(model)
        sv = explainer.shap_values(x)
        vals = sv[1][0] if isinstance(sv, list) else sv[0]
    except Exception:
        explainer = shap.KernelExplainer(model.predict, np.zeros((1, len(feature_names))))
        vals = explainer.shap_values(x)[0]

    contrib = sorted(zip(feature_names, vals), key=lambda z: abs(z[1]), reverse=True)[:req.top_k]
    return {"top_features": [{"name": n, "contribution": float(v)} for n, v in contrib]}