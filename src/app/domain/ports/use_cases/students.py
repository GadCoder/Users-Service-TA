import abc
from typing import Union

from src.app.domain.ports.common.responses import ResponseFailure, ResponseSuccess
from src.app.domain.ports.unit_of_works.students import StudentUnitOfWorkInterface

from src.app.domain.schemas import student as student_schema


class StudentServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: StudentUnitOfWorkInterface):
        self.uow = uow

    def create(self, student: student_schema.StudentCreate) -> Union[ResponseSuccess, ResponseFailure]:
        return self._create(student)

    @abc.abstractmethod
    def _create(
            self, user: student_schema.StudentCreate
    ) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError
