# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import GuestHouseNameUpdate, UserCreate, UserResponse, Token
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.schemas.user import ForgotPassword, ResetPassword
from app.core.security import create_password_reset_token, verify_password_reset_token
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me/guesthouse-name", response_model=UserResponse)
def update_guesthouse_name(
    name_in: GuestHouseNameUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    guesthouse_name = " ".join(name_in.guesthouse_name.split())
    if not guesthouse_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Weka jina la guest house.",
        )

    user = db.query(User).filter(User.id == current_user.id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mtumiaji hakupatikana!",
        )
    user.guesthouse_name = guesthouse_name
    current_user.guesthouse_name = guesthouse_name
    db.commit()
    db.refresh(user)
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = UserRepository.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Barua pepe (email) hii tayari imesajiliwa kwenye mfumo!"
        )
    return UserRepository.create(db=db, user_in=user_in)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Kwenye OAuth2 form, username inabeba barua pepe (email)
    user = UserRepository.get_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Barua pepe au nenosiri sio sahihi!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(data: ForgotPassword, db: Session = Depends(get_db)):
    user = UserRepository.get_by_email(db, email=data.email)
    if not user:
        # Kwa usalama, tunatoa ujumbe wa mafanikio hata kama email haipo 
        # ili kuzuia watu wabaya wasichunguze nani yuko kwenye mfumo
        return {"message": "Kama email hii ipo, tumekutumia maagizo ya kubadilisha nenosiri."}
    
    # Tengeneza token ya siri
    reset_token = create_password_reset_token(user.email)
    
    # Kwenye mfumo wa kawaida, hapa ingetuma Email. 
    # Lakini kwa ajili ya majaribio ya API, tunairejesha kwenye Response ili uione moja kwa moja!
    return {
        "message": "Token ya kubadilisha nenosiri imetengenezwa kwa mafanikio.",
        "reset_token_kwa_majaribio": reset_token 
    }

@router.post("/reset-password")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    email = verify_password_reset_token(data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token si sahihi au muda wake umekwisha!"
        )
    
    user = UserRepository.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mtumiaji hakupatikana!"
        )
    
    UserRepository.update_password(db, user=user, new_password=data.new_password)
    return {"message": "Nenosiri limebadilishwa kwa mafanikio! Sasa unaweza kulogin."}