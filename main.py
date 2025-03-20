from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import video, progress

app = FastAPI(title="Elimu Backend")

# Configuration des CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines (à restreindre en prod)
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

# Inclusion des routes
app.include_router(video.router, prefix="/videos", tags=["Videos"])
app.include_router(progress.router, prefix="/progress", tags=["Progression"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
