from fastapi import FastAPI
from routers import video, progress

app = FastAPI(title="Elimu Backend")

app.include_router(video.router, prefix="/videos", tags=["Videos"])
app.include_router(progress.router, prefix="/progress", tags=["Progression"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
