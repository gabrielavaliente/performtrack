from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_objetivo():
    response = client.post("/goals/", json={
        "empleado_id": "emp001",
        "descripcion": "Aumentar ventas 20%",
        "objetivo_okr": "Crecimiento comercial",
        "peso": 30.0
    })
    assert response.status_code == 200

def test_objetivos_empleado():
    response = client.get("/goals/employee/emp001")
    assert response.status_code == 200
    assert isinstance(response.json(), list)