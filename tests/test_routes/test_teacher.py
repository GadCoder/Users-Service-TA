from fastapi.encoders import jsonable_encoder

from src.app.domain.schemas.teacher import TeacherCreate


def test_create_teacher(app, client, get_fake_container, get_teacher_model_dict):
    teacher = TeacherCreate(**get_teacher_model_dict)
    with app.container.teacher_service.override(get_fake_container.fake_teacher_service):
        response = client.post("/teacher/create/", json=jsonable_encoder(teacher))
        assert response.status_code == 200
        assert response.json() == {
            "names": "Qui-Gon",
            "last_names": "Jinn",
            "email": "qui-gon.jinn@unmsm.edu.pe",
            "picture_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGev6l0BBewv1l3G3PZ2g-X8D9B3oP3uiWy5tGjjmV6d36VPG6Ua4tVVeQH86wlrIrKyg&usqp=CAU",
            "id": 1,
            "teacher_code": "20200055",
            "is_active": True
        }


def test_get_teacher(app, client, get_fake_container, get_teacher_model_dict):
    teacher = TeacherCreate(**get_teacher_model_dict)
    with app.container.teacher_service.override(get_fake_container.fake_teacher_service):
        response = client.post("/teacher/create/", json=jsonable_encoder(teacher))
        assert response.status_code == 200
        response = client.get("/teacher/get-by-code/?teacher_code=20200055")
        assert response.status_code == 200
        assert response.json()["teacher_code"] == "20200055"
