# PerformTrack — Módulo de Evaluación de Desempeño para MintHCM

Módulo desarrollado para Aplicaciones de Código Abierto — Grupo 7.

## Descripción
PerformTrack agrega a MintHCM un módulo de evaluación de desempeño con 
formularios configurables, objetivos OKR, cálculo automático de KPIs 
y reportes en PDF y Excel.

## Requisitos previos
Instalar antes de empezar:
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads) (marcar "Add Python to PATH")

## Paso 1 — Instalar MintHCM
```bash
git clone https://github.com/minthcm/MintHCM.git
cd MintHCM/docker
docker-compose up -d
```
Acceder en: http://localhost
Usuario: admin / Contraseña: minthcm

## Paso 2 — Clonar PerformTrack
```bash
git clone https://github.com/gabrielavaliente/performtrack.git
cd performtrack
```

## Paso 3 — Instalar dependencias
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Paso 4 — Correr el servidor
```bash
uvicorn app.main:app --reload
```

## Paso 5 — Acceder
- MintHCM: http://localhost
- PerformTrack API: http://127.0.0.1:8000/docs

## Tests
```bash
pytest tests/ -v
```

## Tecnologías
- Python + FastAPI
- SQLite
- ReportLab (PDF)
- openpyxl (Excel)
- GitHub Actions (CI/CD)
- Docker (MintHCM)