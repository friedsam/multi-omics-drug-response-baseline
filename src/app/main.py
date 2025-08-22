
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI(title="Multi-Omics Drug Response Baseline API", version="0.1.0")

class PredictRequest(BaseModel):
    features: Dict[str, float]
    masks: Optional[Dict[str, int]] = None  # 1 if observed else 0

class PredictResponse(BaseModel):
    risk_score: float
    top_features: List[str]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # Dummy scoring: mean of provided features
    vals = list(req.features.values())
    score = float(sum(vals)/len(vals)) if vals else 0.5
    # Top features: largest absolute values
    top = sorted(req.features.items(), key=lambda kv: abs(kv[1]), reverse=True)[:5]
    return PredictResponse(risk_score=score, top_features=[k for k,_ in top])
