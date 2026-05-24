from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db, EmployeeGoal
from app.models.schemas import GoalCreate, GoalOut
from typing import List

router = APIRouter()

@router.post("/", response_model=GoalOut)
def crear_objetivo(goal: GoalCreate, db: Session = Depends(get_db)):
    nuevo = EmployeeGoal(**goal.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/employee/{employee_id}", response_model=List[GoalOut])
def objetivos_empleado(employee_id: str, db: Session = Depends(get_db)):
    return db.query(EmployeeGoal).filter(EmployeeGoal.empleado_id == employee_id).all()

@router.put("/{id}/progress")
def actualizar_progreso(id: int, progreso: float, db: Session = Depends(get_db)):
    goal = db.query(EmployeeGoal).filter(EmployeeGoal.id == id).first()
    goal.progreso = progreso
    db.commit()
    return {"mensaje": "Progreso actualizado", "progreso": progreso}