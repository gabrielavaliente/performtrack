from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db, EvaluationForm
from app.models.schemas import EvaluationFormCreate, EvaluationFormOut
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

@router.get("/{id}", response_model=EvaluationFormOut)
def obtener_evaluacion(id: int, db: Session = Depends(get_db)):
    return db.query(EvaluationForm).filter(EvaluationForm.id == id).first()

@router.put("/{id}/assign")
def asignar_empleados(id: int, empleados: List[str]):
    return {"mensaje": f"Empleados asignados a evaluacion {id}", "empleados": empleados}