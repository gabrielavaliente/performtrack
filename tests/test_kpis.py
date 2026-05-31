from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_calcular_kpi():
    response = client.post("/kpis/calculate", json={
        "empleado_id": "emp001",
        "form_id": 1,
        "kpi_nombre": "Ventas Mensuales",
        "valor_actual": 80,
        "valor_meta": 100
    })
    assert response.status_code == 200
    assert response.json()["porcentaje"] == 80.0

def test_kpis_empleado():
    response = client.get("/kpis/employee/emp001")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_calcular_kpi_cumplimiento_completo():
    response = client.post("/kpis/calculate", json={
        "empleado_id": "emp002",
        "form_id": 1,
        "kpi_nombre": "Asistencia",
        "valor_actual": 100,
        "valor_meta": 100
    })
    assert response.status_code == 200
    assert response.json()["porcentaje"] == 100.0

def test_calcular_kpi_cumplimiento_parcial():
    response = client.post("/kpis/calculate", json={
        "empleado_id": "emp003",
        "form_id": 1,
        "kpi_nombre": "Productividad",
        "valor_actual": 50,
        "valor_meta": 200
    })
    assert response.status_code == 200
    assert response.json()["porcentaje"] == 25.0

def test_kpis_empleado_sin_registros():
    response = client.get("/kpis/employee/emp_inexistente_xyz")
    assert response.status_code == 200
    assert response.json() == []

def test_calcular_kpi_campos_faltantes():
    response = client.post("/kpis/calculate", json={
        "empleado_id": "emp001",
        "kpi_nombre": "Sin form_id ni valores"
    })
    assert response.status_code == 422