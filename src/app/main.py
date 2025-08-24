from fastapi import FastAPI
from src.app.routers.explain import router as explain_router

app = FastAPI(title="Multi-Omics API")
app.include_router(explain_router)
app.include_router(core_router)
