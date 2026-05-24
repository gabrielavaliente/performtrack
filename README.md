# PerformTrack — Módulo de Evaluación de Desempeño para MintHCM

Módulo desarrollado para Aplicaciones de Código Abierto — Grupo 7.

## Descripción
PerformTrack agrega a MintHCM un módulo de evaluación de desempeño con formularios configurables, objetivos OKR, cálculo automático de KPIs y reportes en PDF y Excel.

## Tecnologías
- Python 3.12 + FastAPI
- SQLite
- ReportLab (PDF)
- openpyxl (Excel)
- GitHub Actions (CI/CD)
- Docker (MintHCM)

## Instalación
```bash
git clone https://github.com/TU_USUARIO/performtrack.git
cd performtrack
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Documentación API
http://localhost:8000/docs

## Tests
```bash
pytest tests/ -v
```