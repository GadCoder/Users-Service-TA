from fastapi.encoders import jsonable_encoder

from src.app.domain.schemas.student import StudentCreate


def test_create_student(app, client, get_fake_container, get_student_model_dict):
    student = StudentCreate(**get_student_model_dict)
    with app.container.student_service.override(get_fake_container.fake_student_service):
        response = client.post("/student/create/", json=jsonable_encoder(student))
        assert response.status_code == 200
        assert response.json() == {
            "names": "Obi Wan",
            "last_names": "Kenobi",
            "email": "obiwan.kenobi@unmsm.edu.pe",
            "picture_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSrgDyPBG3GS6YXRsMQJmghtYYQVKa_RSk3Q&s",
            "id": 1,
            "student_code": "20200093",
            "is_active": True
        }


def test_get_student(app, client, get_fake_container, get_student_model_dict):
    student = StudentCreate(**get_student_model_dict)
    with app.container.student_service.override(get_fake_container.fake_student_service):
        response = client.post("/student/create/", json=jsonable_encoder(student))
        assert response.status_code == 200
        response = client.get("/student/get-by-code/?student_code=20200093")
        assert response.status_code == 200
        assert response.json()["student_code"] == "20200093"
