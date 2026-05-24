from pydantic import BaseModel

class EvaluationFormCreate(BaseModel):
    nombre: str
    periodo: str
    estado: str

class EvaluationFormOut(EvaluationFormCreate):
    id: int
    class Config:
        from_attributes = True

class GoalCreate(BaseModel):
    empleado_id: str
    descripcion: str
    objetivo_okr: str
    peso: float

class GoalOut(GoalCreate):
    id: int
    progreso: float
    class Config:
        from_attributes = True

class KPICreate(BaseModel):
    empleado_id: str
    form_id: int
    kpi_nombre: str
    valor_actual: float
    valor_meta: float

class KPIOut(KPICreate):
    id: int
    porcentaje: float
    class Config:
        from_attributes = True