import abc
from typing import Union, Any, Coroutine

from src.app.domain.schemas import student as student_schema
from src.app.domain.ports.unit_of_works.student import StudentUnitOfWorkInterface
from src.app.domain.ports.common.responses import ResponseFailure, ResponseSuccess


class StudentServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: StudentUnitOfWorkInterface):
        self.uow = uow

    async def create(self, student: student_schema.StudentCreate) -> ResponseSuccess | ResponseFailure:
        return await self._create(student)

    def get_by_code(self, student_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        return self._get_by_code(student_code)

    @abc.abstractmethod
    async def _create(
            self, user: student_schema.StudentCreate
    ) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_code(self, student_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError
