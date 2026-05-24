from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.database import get_db, KPIRecord
from app.services.report_gen import generate_pdf_report, generate_excel_report
import tempfile
import os

router = APIRouter()

@router.get("/pdf/{employee_id}")
def reporte_pdf(employee_id: str, db: Session = Depends(get_db)):
    kpis = db.query(KPIRecord).filter(KPIRecord.empleado_id == employee_id).all()
    path = os.path.join(tempfile.gettempdir(), f"reporte_{employee_id}.pdf")
    generate_pdf_report(employee_id, kpis, path)
    return FileResponse(path, media_type="application/pdf", filename=f"reporte_{employee_id}.pdf")

@router.get("/excel/{employee_id}")
def reporte_excel(employee_id: str, db: Session = Depends(get_db)):
    kpis = db.query(KPIRecord).filter(KPIRecord.empleado_id == employee_id).all()
    path = os.path.join(tempfile.gettempdir(), f"reporte_{employee_id}.xlsx")
    generate_excel_report(employee_id, kpis, path)
    return FileResponse(path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=f"reporte_{employee_id}.xlsx")