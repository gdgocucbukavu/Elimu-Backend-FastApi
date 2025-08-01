from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import video, progress, reviews, user

app = FastAPI(title="Elimu Backend")

# Maintenant on autorise aussi localhost:4200 (Angular dev) et, si besoin, l'URL de ton front en production
ALLOWED_ORIGINS = [
    "http://localhost:4200",                        # Angular en dev
    "https://mon-site.com",                         # front en prod
    "https://app.mon-site.com",                     # autre domaine prod
    # si tu déploies ton front ailleurs, ajoute-le ici

   "https://elimu-gdgocucb.firebaseapp.com/",
    "https://elimu-gdgocucb.web.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],   # tu peux élargir à "*" pour ne rien bloquer
)

app.include_router(video.router, prefix="/videos", tags=["Videos"])
app.include_router(progress.router, prefix="/progress", tags=["Progression"])
app.include_router(reviews.router, prefix="", tags=["Reviews"])
app.include_router(user.router, prefix="/users", tags=["Users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
