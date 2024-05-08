# Standard
from typing import Optional, List

# FastAPI
from fastapi import Depends, HTTPException, status

# SqlAlchemy
from sqlalchemy.orm import Session

# Own
from database import get_session
from models.models import Operation
from schemas.operations_schemas import (
    OperationOut,
    OperationKind,
    OperationCreate,
    OperationUpdate)


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_operation_by_id(self, user_id: int, operation_id: int):
        operation = (self.session.query(Operation).
                     filter_by(
                            operation_id=operation_id,
                            user_id=user_id
                            )
                     .first()
                     )

        if operation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Operation with is '{operation_id}' was not found!")

        return operation

    def get_operations(self, user_id: int) -> List[Operation]:
        all_operations = self.session.query(Operation).filter_by(user_id=user_id).all()

        return all_operations

    def get_operation_by_id(self, user_id: int, operation_id: int):
        return self._get_operation_by_id(user_id, operation_id)

    def get_operations_by_kind(self, user_id: int, kind: Optional[OperationKind] = None):
        all_operations_query = self.session.query(Operation).filter_by(user_id=user_id)

        if not (kind is None):
            all_operations_query = all_operations_query.filter_by(kind=kind)

        all_operations = all_operations_query.all()

        return all_operations

    def create_operation(self, user_id: int, operation_data: OperationCreate) -> Operation:
        operation = Operation(
            **operation_data.dict(),
            user_id=user_id
        )
        self.session.add(operation)
        self.session.commit()

        return operation

    def create_many_operations(self, user_id: int, operations_data: List[OperationCreate]):
        operations = [
            OperationCreate(
                **operation_data.dict(),
                user_id=user_id
            )
            for operation_data in operations_data
        ]

        self.session.add_all(operations)
        self.session.commit()

        return operations

    def update_operation(self, user_id: int, operation_id: int, operation_data: OperationUpdate):
        operation = self._get_operation_by_id(user_id, operation_id)
        for field, value in operation_data:
            setattr(operation, field, value)
        self.session.commit()

        return operation

    def delete_operation(self, user_id: int, operation_id: int):
        operation = self._get_operation_by_id(user_id, operation_id)

        self.session.delete(operation)
        self.session.commit()
