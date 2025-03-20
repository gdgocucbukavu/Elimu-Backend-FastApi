import requests
from config import YOUTUBE_API_KEY
from urllib.parse import urlparse, parse_qs


def extract_video_id(youtube_url: str) -> str:
    """
    Extrait l'ID de la vidéo depuis une URL YouTube.
    Fonctionne avec les formats :
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """
    parsed_url = urlparse(youtube_url)

    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")

    if "youtube.com" in parsed_url.netloc:
        # Récupère l'ID dans les paramètres de l'URL (ex: ?v=VIDEO_ID)
        return parse_qs(parsed_url.query).get("v", [None])[0]

    return None  # Si l'URL n'est pas valide


def get_youtube_video_data(video_input: str) -> dict:
    """
    Récupère les informations d'une vidéo YouTube en utilisant son URL ou directement son ID.

    Si l'entrée est une URL, l'ID sera extrait automatiquement.
    Sinon, on considère que l'entrée est directement un ID.
    """
    # Vérification si l'entrée ressemble à une URL YouTube
    if "youtube.com" in video_input or "youtu.be" in video_input:
        video_id = extract_video_id(video_input)
        if not video_id:
            print("Erreur : URL YouTube invalide.")
            return None
    else:
        video_id = video_input  # Considère que l'entrée est directement un ID

    # Construction de l'URL pour appeler l'API YouTube
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={YOUTUBE_API_KEY}"
    response = requests.get(url).json()

    print("Réponse API YouTube :", response)  # DEBUG

    if "error" in response:
        print("Erreur API YouTube :", response["error"])
        return None

    if "items" not in response or not response["items"]:
        print(f"Aucune vidéo trouvée pour l'ID {video_id}")
        return None

    video_data = response["items"][0]
    snippet = video_data["snippet"]
    stats = video_data.get("statistics", {})

    return {
        "video_id": video_id,
        "title": snippet.get("title", "Titre inconnu"),
        "description": snippet.get("description", "Pas de description"),
        "publication_date": snippet.get("publishedAt", ""),
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0))
    }



# Exemple d'utilisation
url_video = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_info = get_youtube_video_data(url_video)
print(video_info)

