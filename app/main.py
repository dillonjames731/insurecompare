import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.upload import router as upload_router

app = FastAPI(title="InsureCompare API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(upload_router)

FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.isdir(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True),name="frontend")
