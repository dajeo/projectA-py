from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from starlette.websockets import WebSocketDisconnect

from config import ALGORITHM, JWT_OPTIONS, SECRET_KEY
from quark.database import get_db
from quark.models import User
from quark.schemas import TokenData, UserInDb, UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_date: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_date:
        expire = datetime.utcnow() + expires_date
    else:
        expire = datetime.utcnow() + timedelta(weeks=52)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, tel: str) -> UserInDb | None:
    user = db.query(User).filter(User.tel == tel).first()
    if user is not None:
        user_dict = dict(id=user.id, tel=user.tel, email=user.email, type=user.type_id, org=user.org_id, password=user.password)
        return UserInDb(**user_dict)


def authenticate_user(db: Session, tel: str, password: str) -> UserInDb | None:
    user = get_user(db, tel)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options=JWT_OPTIONS)
        tel: str = payload.get("sub")
        if tel is None:
            raise credentials_exception
        token_data = TokenData(tel=tel)
    except JWTError:
        raise credentials_exception
    user = get_user(db, token_data.tel)
    if user is None:
        raise credentials_exception
    return user


async def get_current_ws_user(db: Session = Depends(get_db), token: str | None = Query(default=None)) -> UserResponse:
    if not token:
        raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION, reason="Token not valid.")
    return await get_current_user(db, token)
