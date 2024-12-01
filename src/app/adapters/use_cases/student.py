from typing import Union

from src.app.domain.ports.common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)
from src.app.domain.models.student import Student
from src.app.domain.schemas import student as student_schema
from src.app.domain.ports.use_cases.student import StudentServiceInterface
from src.app.domain.ports.unit_of_works.student import StudentUnitOfWorkInterface
from src.app.domain.schemas.student import StudentPublic


def _handle_response_failure(
        student_code_: str = None, message: dict[str] = None
) -> ResponseFailure:
    if message:
        return ResponseFailure(ResponseTypes.RESOURCE_ERROR, message=message)
    return ResponseFailure(
        ResponseTypes.RESOURCE_ERROR,
        message={"detail": f"Student with code code {student_code_} not found"}
    )


class StudentService(StudentServiceInterface):
    def __init__(self, uow: StudentUnitOfWorkInterface):
        self.uow = uow

    def _create(
            self, student: student_schema.StudentCreate
    ) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            with self.uow:
                student_ = self.uow.students.get_by_code(student.student_code)
                if student_ is None:
                    new_student = Student(
                        names=student.names,
                        last_names=student.last_names,
                        email=student.email,
                        picture_url=student.picture_url,
                        student_code=student.student_code,
                        is_superuser=False
                    )
                    self.uow.students.add(new_student)
                self.uow.commit()
                student_ = student_ or self.uow.students.get_by_code(student.student_code)
                student_output = student_schema.StudentPublic(
                    id=student_.id,
                    names=student_.names,
                    last_names=student_.last_names,
                    email=student_.email,
                    picture_url=student_.picture_url,
                    student_code=student_.student_code,
                    is_active=student_.is_active
                )
                return ResponseSuccess(student_output)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)

    def _get_by_code(self, student_code: str) -> Union[ResponseSuccess, ResponseFailure]:
        with self.uow:
            student = self.uow.students.get_by_code(code=student_code)
            if student:
                return ResponseSuccess(
                    StudentPublic(
                        id=student.id,
                        names=student.names,
                        last_names=student.last_names,
                        email=student.email,
                        picture_url=student.picture_url,
                        student_code=student.student_code,
                        is_active=student.is_active
                    )
                )
            return _handle_response_failure(student_code)
