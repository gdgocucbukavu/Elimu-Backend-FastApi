from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import video, progress

app = FastAPI(title="Elimu Backend")

""" Sécurité de CROS (mettre jour les origines autoriséesen production)
par exemple 'ALLOWED_ORIGINS = ["http://localhost:3000",
                   "https://site.com"]'
                   donc on ne va pas autorisé toute les origines
                   """

# Configuration des CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines (à restreindre en prod)
    allow_credentials=True,
    #Pourquoi autoriser toutes les méthodes, pourquoi oas restreindre juste les
    # nécessaires et même pour led headers
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

# Inclusion des routes
app.include_router(video.router, prefix="/videos", tags=["Videos"])
app.include_router(progress.router, prefix="/progress", tags=["Progression"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
