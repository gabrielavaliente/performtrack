from fastapi import FastAPI
from app.api import evaluations, goals, kpis, reports

app = FastAPI(title="PerformTrack", version="1.0.0")

app.include_router(evaluations.router, prefix="/evaluations", tags=["Evaluaciones"])
app.include_router(goals.router, prefix="/goals", tags=["OKRs"])
app.include_router(kpis.router, prefix="/kpis", tags=["KPIs"])
app.include_router(reports.router, prefix="/reports", tags=["Reportes"])

@app.get("/")
def root():
    return {"mensaje": "PerformTrack API funcionando"}