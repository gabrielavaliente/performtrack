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