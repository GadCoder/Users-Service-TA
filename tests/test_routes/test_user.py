from fastapi.encoders import jsonable_encoder

from src.app.domain.schemas.user import UserCreate


def test_create_teacher(app, client, get_fake_container, get_teacher_model_dict):
    teacher = UserCreate(**get_teacher_model_dict)
    with app.container.user_service.override(get_fake_container.fake_user_service):
        response = client.post("/user/create/", json=jsonable_encoder(teacher))
        assert response.status_code == 200
        assert response.json() == {
            "names": "Qui-Gon",
            "last_names": "Jinn",
            "email": "qui-gon.jinn@unmsm.edu.pe",
            "picture_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGev6l0BBewv1l3G3PZ2g-X8D9B3oP3uiWy5tGjjmV6d36VPG6Ua4tVVeQH86wlrIrKyg&usqp=CAU",
            "id": 1,
            "code": "20200055",
            "is_teacher": True,
            "is_active": True
        }


def test_get_teacher(app, client, get_fake_container, get_teacher_model_dict):
    user = UserCreate(**get_teacher_model_dict)
    with app.container.user_service.override(get_fake_container.fake_user_service):
        response = client.post("/user/create/", json=jsonable_encoder(user))
        assert response.status_code == 200
        response = client.get("/user/get-by-code/?user_code=20200055")
        assert response.status_code == 200
        assert response.json()["code"] == "20200055"
