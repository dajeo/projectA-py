from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config import ACCESS_TOKEN_EXPIRE_WEEKS
from quark.database import get_db

from quark.schemas import Token
from quark.utils import authenticate_user, create_access_token

router = APIRouter(prefix="/auth")


@router.post("/token", response_model=Token)
async def authorize(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(weeks=ACCESS_TOKEN_EXPIRE_WEEKS)
    access_token = create_access_token(
        {"sub": user.tel}, access_token_expires
    )
    return {"access_token": access_token, "account_type": user.type, "token_type": "bearer"}
