from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./performtrack.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EvaluationForm(Base):
    __tablename__ = "evaluation_forms"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    periodo = Column(String)
    estado = Column(String)
    creado_en = Column(DateTime, default=datetime.datetime.utcnow)

class EmployeeGoal(Base):
    __tablename__ = "employee_goals"
    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(String)
    descripcion = Column(String)
    objetivo_okr = Column(String)
    peso = Column(Float)
    progreso = Column(Float, default=0.0)

class KPIRecord(Base):
    __tablename__ = "kpi_records"
    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(String)
    form_id = Column(Integer)
    kpi_nombre = Column(String)
    valor_actual = Column(Float)
    valor_meta = Column(Float)
    porcentaje = Column(Float)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()