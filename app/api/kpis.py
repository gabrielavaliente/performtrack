from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db, KPIRecord
from app.models.schemas import KPICreate, KPIOut
from typing import List

router = APIRouter()

@router.post("/calculate", response_model=KPIOut)
def calcular_kpi(kpi: KPICreate, db: Session = Depends(get_db)):
    porcentaje = (kpi.valor_actual / kpi.valor_meta) * 100 if kpi.valor_meta > 0 else 0
    nuevo_kpi = KPIRecord(**kpi.model_dump(), porcentaje=round(porcentaje, 2))
    db.add(nuevo_kpi)
    db.commit()
    db.refresh(nuevo_kpi)
    return nuevo_kpi

@router.get("/employee/{employee_id}", response_model=List[KPIOut])
def kpis_empleado(employee_id: str, db: Session = Depends(get_db)):
    return db.query(KPIRecord).filter(KPIRecord.empleado_id == employee_id).all()