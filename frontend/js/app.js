// Navegación entre secciones
const titles = {
  dashboard: { title: "Dashboard", subtitle: "Resumen general del sistema" },
  evaluaciones: { title: "Evaluaciones", subtitle: "Gestiona formularios de evaluación" },
  okr: { title: "OKRs", subtitle: "Objetivos y resultados clave" },
  kpis: { title: "KPIs", subtitle: "Indicadores de desempeño" },
  reportes: { title: "Reportes", subtitle: "Genera reportes por empleado" }
};

document.querySelectorAll(".nav-link").forEach(link => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const section = link.dataset.section;

    document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
    document.querySelectorAll(".section-page").forEach(s => s.classList.remove("active"));

    link.classList.add("active");
    document.getElementById(section).classList.add("active");

    document.getElementById("page-title").textContent = titles[section].title;
    document.getElementById("page-subtitle").textContent = titles[section].subtitle;
  });
});

const API = "";

async function cargarEvaluaciones() {
  const res = await fetch(`${API}/evaluations/`);
  const data = await res.json();

  document.getElementById("totalEvaluaciones").textContent = data.length;

  if (data.length === 0) {
    document.getElementById("evaluacionesList").innerHTML = "<p>No hay evaluaciones registradas.</p>";
    return;
  }

  const html = `
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Período</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        ${data.map(e => `
          <tr>
            <td>${e.id}</td>
            <td>${e.nombre}</td>
            <td>${e.periodo}</td>
            <td>${e.estado}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;

  document.getElementById("evaluacionesList").innerHTML = html;
}

document.getElementById("evaluationForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    nombre: document.getElementById("nombre").value,
    periodo: document.getElementById("periodo").value,
    estado: document.getElementById("estado").value
  };

  const res = await fetch(`${API}/evaluations/`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    alert("Error al crear evaluación");
    return;
  }

  e.target.reset();
  cargarEvaluaciones();
});

document.getElementById("goalForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const descripcion = document.getElementById("descripcionGoal").value;

  const payload = {
    empleado_id: document.getElementById("empleadoIdGoal").value,
    descripcion: descripcion,
    objetivo_okr: descripcion,
    peso: Number(document.getElementById("pesoGoal").value)
  };

  const res = await fetch(`${API}/goals/`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    alert("Error al crear OKR");
    return;
  }

  alert("OKR creado correctamente");
  e.target.reset();
});

document.getElementById("kpiForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    empleado_id: document.getElementById("empleadoIdKpi").value,
    form_id: Number(document.getElementById("formIdKpi").value),
    kpi_nombre: document.getElementById("kpiNombre").value,
    valor_actual: Number(document.getElementById("valorActual").value),
    valor_meta: Number(document.getElementById("valorMeta").value)
  };

  const res = await fetch(`${API}/kpis/calculate`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    alert("Error al calcular KPI");
    return;
  }

  const data = await res.json();

  const box = document.getElementById("kpiResult");
  box.style.display = "block";
  box.textContent = `KPI calculado: ${data.porcentaje}% de cumplimiento`;

  e.target.reset();
});

function descargarPDF() {
  const id = document.getElementById("empleadoReporte").value;
  if (!id) {
    alert("Ingresa el ID del empleado");
    return;
  }

  window.open(`${API}/reports/pdf/${id}`, "_blank");
}

function descargarExcel() {
  const id = document.getElementById("empleadoReporte").value;
  if (!id) {
    alert("Ingresa el ID del empleado");
    return;
  }

  window.open(`${API}/reports/excel/${id}`, "_blank");
}

cargarEvaluaciones();