from typing import Union

from src.app.domain.ports.common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)
from src.app.domain.ports.unit_of_works.students import StudentUnitOfWorkInterface
from src.app.domain.ports.use_cases.students import StudentServiceInterface
from src.app.domain.schemas import student as student_schema
from src.app.domain.models.student import Student


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
                    student_code=student_.student_code
                )
                return ResponseSuccess(student_output)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)
