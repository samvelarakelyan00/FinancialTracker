from fastapi import APIRouter
from .endpoints.operation_routes import op_router as operation_router
from .endpoints.user_auth_router import router as user_auth_router
from .endpoints.reports_router import router as reports_router


router = APIRouter()

router.include_router(operation_router)
router.include_router(user_auth_router)
router.include_router(reports_router)
