# FastAPI
from fastapi import APIRouter, Depends

# Own
from schemas.auth_schemas import (
    UserCreate,
    Token,
    LoginForm
)

from services import auth as auth_service


router = APIRouter(
    prefix='/auth',
    tags=["User Auth"]
)


@router.post("/sign-up")
def sign_up(user_data: UserCreate,
            service: auth_service.AuthService = Depends()):

    return service.register_new_user(user_data)


# @router.post("/login", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends(),
#           service: auth_service.AuthService = Depends()):
#
#     return service.authenticate_user(form_data)


@router.post("/login", response_model=Token)
def login(login_data: LoginForm,
          service: auth_service.AuthService = Depends()):

    return service.authenticate_user(login_data)