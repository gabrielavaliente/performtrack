from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import openpyxl
import os

def generate_pdf_report(employee_id: str, kpis: list, output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Reporte de Desempeno - Empleado {employee_id}", styles["Title"]))

    data = [["KPI", "Valor Actual", "Meta", "% Logro"]]
    for kpi in kpis:
        data.append([kpi.kpi_nombre, str(kpi.valor_actual), str(kpi.valor_meta), f"{kpi.porcentaje}%"])

    tabla = Table(data)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(tabla)
    doc.build(story)

def generate_excel_report(employee_id: str, kpis: list, output_path: str):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Evaluacion de Desempeno"
    ws.append(["Empleado ID", "KPI", "Valor Actual", "Meta", "% Logro"])
    for kpi in kpis:
        ws.append([employee_id, kpi.kpi_nombre, kpi.valor_actual, kpi.valor_meta, kpi.porcentaje])
    wb.save(output_path)