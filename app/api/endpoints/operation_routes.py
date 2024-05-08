# FastAPI
from fastapi import APIRouter, Depends, status, Response

# Own
from services import operation as operation_service
from schemas.operations_schemas import (
    OperationKind,
    OperationCreate,
    OperationUpdate)

from services.auth import get_current_user
from models.models import User


op_router = APIRouter(
    prefix='/operations',
    tags=['User Operations']
)


@op_router.get("")
def get_operations(service: operation_service.OperationsService = Depends(),
                   get_current_user: User = Depends(get_current_user)):
    return service.get_operations(user_id=get_current_user.user_id)


@op_router.get("/by-kind")
def get_operations_by_kind(kind: OperationKind = None,
                           get_current_user: User = Depends(get_current_user),
                           service: operation_service.OperationsService = Depends()):
    return service.get_operations_by_kind(user_id=get_current_user.user_id, kind=kind)


@op_router.get("/{operation_id}")
def get_operation_by_id(operation_id: int,
                        get_current_user: User = Depends(get_current_user),
                        service: operation_service.OperationsService = Depends()):

    return service.get_operation_by_id(user_id=get_current_user.user_id, operation_id=operation_id)


@op_router.post("/create-operation")
def create_operation(
        operation_data: OperationCreate,
        get_current_user: User = Depends(get_current_user),
        service: operation_service.OperationsService = Depends()):

    return service.create_operation(user_id=get_current_user.user_id, operation_data=operation_data)


@op_router.put("/update/{operation_id}")
def update_operation(
        operation_id: int,
        operation_data: OperationUpdate,
        get_current_user: User = Depends(get_current_user),
        service: operation_service.OperationsService = Depends()):

    return service.update_operation(user_id=get_current_user.user_id,
                                    operation_id=operation_id,
                                    operation_data=operation_data)


@op_router.delete("/delete/{operation_id}")
def delete_operation(operation_id: int,
                     get_current_user: User = Depends(get_current_user),
                     service: operation_service.OperationsService = Depends()):

    service.delete_operation(user_id=get_current_user.user_id,
                             operation_id=operation_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
