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
    try:
        parsed_url = urlparse(youtube_url)

        if "youtu.be" in parsed_url.netloc:
            return parsed_url.path.lstrip("/")

        if "youtube.com" in parsed_url.netloc:
            # Récupère l'ID dans les paramètres de l'URL (ex: ?v=VIDEO_ID)
            return parse_qs(parsed_url.query).get("v", [None])[0]

        raise ValueError("URL YouTube invalide.")  # Lève une exception si l'URL ne correspond pas
    except Exception as e:
        raise ValueError(f"Erreur lors de l'extraction de l'ID de la vidéo : {e}")


def get_youtube_video_data(video_input: str) -> dict:
    """
    Récupère les informations d'une vidéo YouTube en utilisant son URL ou directement son ID.

    Si l'entrée est une URL, l'ID sera extrait automatiquement.
    Sinon, on considère que l'entrée est directement un ID.
    """
    try:
        # Vérification si l'entrée ressemble à une URL YouTube
        if "youtube.com" in video_input or "youtu.be" in video_input:
            video_id = extract_video_id(video_input)
        else:
            video_id = video_input  # Considère que l'entrée est directement un ID

        if not video_id:
            raise ValueError("Impossible d'extraire un ID de vidéo valide.")

        # Construction de l'URL pour appeler l'API YouTube
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={YOUTUBE_API_KEY}"

        try:
            response = requests.get(url, timeout=5)  # Timeout pour éviter un blocage infini
            response.raise_for_status()  # Vérifie si la requête a échoué
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Erreur lors de la requête API YouTube : {e}")

        if "error" in data:
            raise ValueError(f"Erreur API YouTube : {data['error']}")

        if "items" not in data or not data["items"]:
            raise ValueError(f"Aucune vidéo trouvée pour l'ID {video_id}")

        video_data = data["items"][0]
        snippet = video_data.get("snippet", {})
        stats = video_data.get("statistics", {})

        return {
            "video_id": video_id,
            "title": snippet.get("title", "Titre inconnu"),
            "description": snippet.get("description", "Pas de description"),
            "publication_date": snippet.get("publishedAt", ""),
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0))
        }

    except ValueError as ve:
        print(f"Erreur de validation : {ve}")
    except ConnectionError as ce:
        print(f"Erreur de connexion : {ce}")
    except Exception as e:
        print(f"Erreur inconnue : {e}")

    return None  # Retourne None en cas d'erreur


# Exemple d'utilisation
url_video = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_info = get_youtube_video_data(url_video)

if video_info:
    print(video_info)
else:
    print("Impossible de récupérer les données de la vidéo.")
