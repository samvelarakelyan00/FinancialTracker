import datetime

from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from pydantic import ValidationError
from fastapi.security.oauth2 import OAuth2PasswordBearer

# SqlAlchemy
from sqlalchemy.orm.session import Session


from passlib.hash import bcrypt
from jose import jwt, JWTError

# Own
# from core import settings
from schemas.auth_schemas import UserOut, Token, UserCreate, LoginForm
from database import get_session
from models import models


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/user_auth_router/login')


def get_current_user(token: str = Depends(oauth2_schema)):
    return AuthService.verify_token(token)


class AuthService:
    @classmethod
    def hash_password(cls, plain_password: str) -> str:
        return bcrypt.hash(plain_password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str):
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def verify_token(cls, token: str):
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credentials",
            headers={
                "WWW-Authenticated": 'Bearer'
            }
        )
        try:
            payload = jwt.decode(
                token,
                "secret",
                algorithms=["HS256"]
            )
        except JWTError:
            raise exception

        user_data = payload.get('user')

        try:
            user = UserOut.parse_obj(user_data)
        except ValidationError:
            raise exception

        return user

    @classmethod
    def create_token(cls, user):
        user_data = UserOut.from_orm(user)

        now = datetime.datetime.utcnow()

        payload = {
            "exp": now + datetime.timedelta(minutes=1000),
            "user": user_data.dict()
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreate):
        user = models.User(
            username=user_data.username,
            email=user_data.email,
            password=self.hash_password(user_data.password)
        )
        self.session.add(user)
        self.session.commit()

        return "OK"

    def authenticate_user(self, login_data: LoginForm):
        email = login_data.email
        password = login_data.password

        user = self.session.query(models.User).filter_by(email=email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with email '{email}' was not found!")

        password_from_db = user.__dict__.get('password')

        if not self.verify_password(password, password_from_db):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Wrong password: '{password}'")

        return self.create_token(user)

















