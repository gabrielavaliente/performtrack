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