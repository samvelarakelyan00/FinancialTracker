from datetime import date
from decimal import Decimal
from typing import Optional
from enum import Enum

from pydantic import BaseModel


class OperationKind(str, Enum):
    INCOME = "income"
    OUTCOME = "outcome"


class OperationBase(BaseModel):
    date: date
    kind: OperationKind
    amount: Decimal
    description: Optional[str]

    class Config:
        from_attributes = True


class OperationOut(OperationBase):
    operation_id: int


class OperationCreate(OperationBase):
    pass


class OperationUpdate(OperationBase):
    pass
