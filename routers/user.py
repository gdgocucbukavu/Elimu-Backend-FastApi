from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse
from models import User
from database import SessionLocal
from crud import create_user, get_user, update_user, delete_user

router = APIRouter()

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserResponse, tags=["Users"])
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel utilisateur.
    """
    # Vérifier si l'email est déjà enregistré
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    return create_user(db, user.dict())


@router.get("/{user_id}", response_model=UserResponse, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Récupère un utilisateur par son ID.
    """
    return get_user(db, user_id)


@router.put("/{user_id}", response_model=UserResponse, tags=["Users"])
def update_existing_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    """
    Met à jour les informations d'un utilisateur.
    """
    # Ici, on utilise le schéma UserCreate pour simplifier,
    # mais il est conseillé de définir un schéma dédié pour la mise à jour (avec tous les champs optionnels).
    update_data = user_update.dict(exclude_unset=True)
    return update_user(db, user_id, update_data)


@router.delete("/{user_id}", response_model=UserResponse, tags=["Users"])
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    """
    Supprime un utilisateur de la base de données.
    """
    return delete_user(db, user_id)
