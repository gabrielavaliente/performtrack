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

def test_crear_objetivo_peso_negativo():
    response = client.post("/goals/", json={
        "empleado_id": "emp001",
        "descripcion": "Objetivo inválido",
        "objetivo_okr": "Test",
        "peso": -10.0
    })
    assert response.status_code == 422

def test_crear_objetivo_peso_mayor_100():
    response = client.post("/goals/", json={
        "empleado_id": "emp001",
        "descripcion": "Objetivo inválido",
        "objetivo_okr": "Test",
        "peso": 150.0
    })
    assert response.status_code == 422

def test_actualizar_progreso_valido():
    crear = client.post("/goals/", json={
        "empleado_id": "emp_test",
        "descripcion": "Objetivo para progreso",
        "objetivo_okr": "Test progreso",
        "peso": 50.0
    })
    id_creado = crear.json()["id"]

    response = client.put(f"/goals/{id_creado}/progress?progreso=75")
    assert response.status_code == 200
    assert response.json()["progreso"] == 75

def test_actualizar_progreso_negativo():
    crear = client.post("/goals/", json={
        "empleado_id": "emp_test",
        "descripcion": "Objetivo para progreso negativo",
        "objetivo_okr": "Test",
        "peso": 50.0
    })
    id_creado = crear.json()["id"]

    response = client.put(f"/goals/{id_creado}/progress?progreso=-5")
    assert response.status_code == 400

def test_actualizar_progreso_objetivo_no_existente():
    response = client.put("/goals/999999/progress?progreso=50")
    assert response.status_code == 404
    assert response.json()["detail"] == "Objetivo no encontrado"