from typing import Union

from src.app.domain.ports.common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)
from src.app.domain.models.teacher import Teacher
from src.app.domain.schemas import teacher as teacher_schema
from src.app.domain.ports.use_cases.teacher import TeacherServiceInterface
from src.app.domain.ports.unit_of_works.teacher import TeacherUnitOfWorkInterface


class TeacherService(TeacherServiceInterface):
    def __init__(self, uow: TeacherUnitOfWorkInterface):
        self.uow = uow

    def _create(
            self, teacher: teacher_schema.TeacherCreate
    ) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            with self.uow:
                teacher_ = self.uow.teachers.get_by_code(code=teacher.teacher_code)
                if teacher_ is None:
                    new_teacher = Teacher(
                        names=teacher.names,
                        last_names=teacher.last_names,
                        email=teacher.email,
                        picture_url=teacher.picture_url,
                        teacher_code=teacher.teacher_code,
                        password=teacher.password,
                        is_superuser=False
                    )
                    self.uow.teachers.add(new_teacher)
                self.uow.commit()
                teacher_ = teacher_ or self.uow.teachers.get_by_code(teacher.teacher_code)
                teacher_output = teacher_schema.TeacherPublic(
                    id=teacher_.id,
                    names=teacher_.names,
                    last_names=teacher_.last_names,
                    email=teacher_.email,
                    picture_url=teacher_.picture_url,
                    teacher_code=teacher_.teacher_code,
                    is_active=teacher_.is_active
                )
                return ResponseSuccess(teacher_output)
        except Exception as e:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)
