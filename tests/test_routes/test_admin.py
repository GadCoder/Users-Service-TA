from fastapi.encoders import jsonable_encoder

from src.app.domain.schemas.admin import AdminCreate


def test_create_admin(app, client, get_fake_container, get_admin_model_dict):
    admin = AdminCreate(**get_admin_model_dict)
    with app.container.admin_service.override(get_fake_container.fake_admin_service):
        response = client.post("/admin/create/", json=jsonable_encoder(admin))
        assert response.status_code == 200
        assert response.json()["names"] == "Yoda"
        assert response.json()["last_names"] == ""
        assert response.json()["email"] == "yoda@unmsm.edu.pe"
        assert response.json()["is_superuser"] == True
        assert response.json()["is_active"] == True


def test_get_admin(app, client, get_fake_container, get_admin_model_dict):
    admin = AdminCreate(**get_admin_model_dict)
    with app.container.admin_service.override(get_fake_container.fake_admin_service):
        response = client.post("/admin/create/", json=jsonable_encoder(admin))
        assert response.status_code == 200
        response = client.get("/admin/get-by-email/?email=yoda@unmsm.edu.pe")
        assert response.status_code == 200
        assert response.json()["email"] == "yoda@unmsm.edu.pe"
