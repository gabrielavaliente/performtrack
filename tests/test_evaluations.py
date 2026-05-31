from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_evaluacion():
    response = client.post("/evaluations/", json={
        "nombre": "Evaluacion Q2 2025",
        "periodo": "Q2",
        "estado": "activo"
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Evaluacion Q2 2025"

def test_listar_evaluaciones():
    response = client.get("/evaluations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obtener_evaluacion_existente():

    crear = client.post("/evaluations/", json={
        "nombre": "Evaluacion Test",
        "periodo": "Q1",
        "estado": "borrador"
    })
    id_creado = crear.json()["id"]

    response = client.get(f"/evaluations/{id_creado}")
    assert response.status_code == 200
    assert response.json()["id"] == id_creado

def test_obtener_evaluacion_no_existente():
    response = client.get("/evaluations/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Evaluación no encontrada"