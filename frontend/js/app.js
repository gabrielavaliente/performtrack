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

const API = window.location.origin;

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

// OKR: listar objetivos por empleado
async function cargarObjetivosEmpleado(employeeId) {
  try {
    const res = await fetch(`${API}/goals/employee/${encodeURIComponent(employeeId)}`);
    if (!res.ok) {
      document.getElementById("goalsList").innerHTML = '<p>Error al obtener objetivos.</p>';
      return;
    }

    const data = await res.json();
    if (!data || data.length === 0) {
      document.getElementById("goalsList").innerHTML = '<p>No se encontraron objetivos para el empleado.</p>';
      return;
    }

    const html = `
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Empleado</th>
            <th>Descripción</th>
            <th>Peso</th>
            <th>Progreso</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          ${data.map(g => `
            <tr>
              <td>${g.id}</td>
              <td>${g.empleado_id}</td>
              <td>${g.descripcion}</td>
              <td>${g.peso}</td>
              <td>
                <input id="progreso-${g.id}" type="number" min="0" max="100" value="${g.progreso ?? 0}" style="width:80px;padding:6px;border-radius:6px;border:1px solid #ddd;" />
              </td>
              <td>
                <button data-id="${g.id}" class="btn-update-progreso">Actualizar</button>
              </td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    `;

    document.getElementById("goalsList").innerHTML = html;

    // attach listeners to update buttons
    document.querySelectorAll('.btn-update-progreso').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const id = btn.dataset.id;
        const val = document.getElementById(`progreso-${id}`).value;
        await actualizarProgreso(id, val);
      });
    });

  } catch (err) {
    document.getElementById("goalsList").innerHTML = '<p>Error de red al obtener objetivos.</p>';
    console.error(err);
  }
}

async function actualizarProgreso(id, progreso) {
  try {
    const res = await fetch(`${API}/goals/${id}/progress?progreso=${encodeURIComponent(progreso)}`, {
      method: 'PUT'
    });

    if (!res.ok) {
      alert('Error al actualizar progreso');
      return;
    }

    const text = await res.text();
    alert('Progreso actualizado');
    // Optionally refresh the list if the empleado id is in the search input
    const empleadoId = document.getElementById('empleadoBuscar').value;
    if (empleadoId) cargarObjetivosEmpleado(empleadoId);
  } catch (err) {
    alert('Error de red al actualizar progreso');
    console.error(err);
  }
}

// buscar objetivos por empleado
document.getElementById('buscarObjetivosBtn').addEventListener('click', (e) => {
  e.preventDefault();
  const id = document.getElementById('empleadoBuscar').value;
  if (!id) {
    alert('Ingresa el ID del empleado');
    return;
  }
  cargarObjetivosEmpleado(id);
});

// KPIs: listar KPIs por empleado
async function cargarKpisEmpleado(employeeId) {
  try {
    const res = await fetch(`${API}/kpis/employee/${encodeURIComponent(employeeId)}`);
    if (!res.ok) {
      document.getElementById('kpisList').innerHTML = '<p>Error al obtener KPIs.</p>';
      return;
    }

    const data = await res.json();
    if (!data || data.length === 0) {
      document.getElementById('kpisList').innerHTML = '<p>No se encontraron KPIs para el empleado.</p>';
      return;
    }

    const html = `
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Empleado</th>
            <th>KPI</th>
            <th>Valor actual</th>
            <th>Valor meta</th>
            <th>%</th>
          </tr>
        </thead>
        <tbody>
          ${data.map(k => `
            <tr>
              <td>${k.id}</td>
              <td>${k.empleado_id}</td>
              <td>${k.kpi_nombre}</td>
              <td>${k.valor_actual}</td>
              <td>${k.valor_meta}</td>
              <td>${k.porcentaje}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;

    document.getElementById('kpisList').innerHTML = html;
  } catch (err) {
    document.getElementById('kpisList').innerHTML = '<p>Error de red al obtener KPIs.</p>';
    console.error(err);
  }
}

document.getElementById('buscarKpisBtn').addEventListener('click', (e) => {
  e.preventDefault();
  const id = document.getElementById('empleadoBuscarKpi').value;
  if (!id) {
    alert('Ingresa el ID del empleado');
    return;
  }
  cargarKpisEmpleado(id);
});