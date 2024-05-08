import csv
from typing import Any
from io import StringIO

from fastapi import HTTPException, status, Depends

from sqlalchemy.orm.session import Session

from services.operation import OperationsService
from schemas.operations_schemas import OperationCreate
from database import get_session
from models.models import Operation


class ReportsService:
    def __init__(self, operations_service: OperationsService = Depends()):
        self.operation_service = operations_service

    def import_from_csv(self, user_id: int, file: Any):
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames=[
                'date',
                'kind',
                'amount',
                'description'
            ]
        )

        operations = []
        next(reader)
        for row in reader:
            operation_data = OperationCreate.parse_obj(row)
            if operation_data.description == '':
                operation_data.description = None
            operations.append(operation_data)

        self.operation_service.create_many_operations(
            user_id=user_id,
            operations_data=operations
        )

    def export_to_csv(self, user_id: int):
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                'date',
                'kind',
                'amount',
                'description'
            ],
            extrasaction='ignore'
        )

        operations = self.operation_service.get_operations(user_id)

        writer.writeheader()
        for operation in operations:
            operation_data = OperationCreate.from_orm(operation)
            writer.writerow(operation_data.dict())

        output.seek(0)

        return output
