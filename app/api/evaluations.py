from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db, EvaluationForm
from app.models.schemas import EvaluationFormCreate, EvaluationFormOut
from app.services.minthcm import MintHCMClient
from app.core.config import MINTHCM_BASE_URL, MINTHCM_USERNAME, MINTHCM_PASSWORD
from typing import List

router = APIRouter()

@router.post("/", response_model=EvaluationFormOut)
def crear_evaluacion(form: EvaluationFormCreate, db: Session = Depends(get_db)):
    nueva = EvaluationForm(**form.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=List[EvaluationFormOut])
def listar_evaluaciones(db: Session = Depends(get_db)):
    return db.query(EvaluationForm).all()

@router.get("/employees/from-minthcm")
def obtener_empleados_de_minthcm():
    client = MintHCMClient(
        base_url=MINTHCM_BASE_URL,
        username=MINTHCM_USERNAME,
        password=MINTHCM_PASSWORD
    )
    empleados = client.get_employees()
    return empleados

@router.get("/{id}", response_model=EvaluationFormOut)
def obtener_evaluacion(id: int, db: Session = Depends(get_db)):
    evaluation = db.query(EvaluationForm).filter(EvaluationForm.id == id).first()

    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")

    return evaluation

@router.put("/{id}/assign")
def asignar_empleados(id: int, empleados: List[str]):
    return {"mensaje": f"Empleados asignados a evaluacion {id}", "empleados": empleados}