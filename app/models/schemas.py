from pydantic import BaseModel, Field  

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
    peso: float = Field(..., ge=0, le=100, description="Peso del objetivo (0-100)")

class GoalOut(GoalCreate):
    id: int
    progreso: float = Field(default=0.0, ge=0, le=100)
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