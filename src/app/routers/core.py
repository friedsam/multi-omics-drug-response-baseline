from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

class PredictReq(BaseModel):
    features: dict
    masks: dict | None = None

@router.post("/predict")
def predict(req: PredictReq):
    risk = float(sum(req.features.values())) / max(len(req.features), 1)
    top = sorted(req.features.items(), key=lambda kv: abs(kv[1]), reverse=True)[:3]
    return {
        "risk_score": risk,
        "top_features": [{"name": k, "contribution": float(v)} for k, v in top],
    }