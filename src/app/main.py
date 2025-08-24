from fastapi import FastAPI
from app.routers.explain import router as explain_router
from app.routers.core import router as core_router

app = FastAPI(title="Multi-Omics API")
app.include_router(explain_router)
app.include_router(core_router)
