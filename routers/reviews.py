from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from schemas import ReviewCreate, ReviewResponse
from crud import add_review, get_reviews_for_video, get_average_rating
from database import get_db

router = APIRouter()

@router.post("/reviews/", response_model=ReviewResponse)
def create_review(review_data: ReviewCreate, db: Session = Depends(get_db)):
    """
    Ajoute un avis à une vidéo.
    """
    try:
        review = add_review(db, review_data)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de l'ajout de l'avis"
            )
        return review
    except Exception as e:
        # On peut logger l'exception ici pour le debug (ex: logger.error(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur interne est survenue lors de la création de l'avis"
        )

@router.get("/reviews/{video_id}", response_model=List[ReviewResponse])
def list_reviews(video_id: int, db: Session = Depends(get_db)):
    """
    Récupère les avis d'une vidéo.
    """
    try:
        reviews = get_reviews_for_video(db, video_id)
        if reviews is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aucun avis trouvé pour cette vidéo"
            )
        return reviews
    except Exception as e:
        # Log de l'exception si nécessaire
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des avis"
        )

@router.get("/videos/{video_id}/rating", response_model=float)
def video_rating(video_id: int, db: Session = Depends(get_db)):
    """
    Renvoie la note moyenne d'une vidéo.
    """
    try:
        rating = get_average_rating(db, video_id)
        if rating is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vidéo introuvable ou pas d'avis pour cette vidéo"
            )
        return rating
    except Exception as e:
        # Log de l'exception si besoin
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du calcul de la note moyenne"
        )
