from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import video, progress, reviews, user  # Ajout du routeur user

app = FastAPI(title="Elimu Backend")

# Configuration des CORS : autorise uniquement les domaines spécifiés
ALLOWED_ORIGINS = [
    "https://mon-site.com",
    "https://app.mon-site.com",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, PUT, etc.)
    allow_headers=["Content-Type", "Authorization"],
)

# Inclusion des routes avec préfixes pour une meilleure organisation
app.include_router(video.router, prefix="/videos", tags=["Videos"])
app.include_router(progress.router, prefix="/progress", tags=["Progression"])
app.include_router(reviews.router, prefix="", tags=["Reviews"])
app.include_router(user.router, prefix="/users", tags=["Users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
