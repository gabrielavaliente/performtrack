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

function mostrarMensajeOKR(elementId, tipo, texto) {
  const el = document.getElementById(elementId);
  if (!el) return;
  el.textContent = texto;
  el.className = `form-message ${tipo} visible`;
  setTimeout(() => {
    el.className = 'form-message';
  }, 4000);
}

document.getElementById("goalForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const pesoVal = Number(document.getElementById("pesoGoal").value);

  if (pesoVal < 0 || pesoVal > 100) {
    mostrarMensajeOKR("goalFormMsg", "error", "El peso debe estar entre 0 y 100.");
    return;
  }

  const descripcion = document.getElementById("descripcionGoal").value;

  const payload = {
    empleado_id: document.getElementById("empleadoIdGoal").value,
    descripcion: descripcion,
    objetivo_okr: descripcion,
    peso: pesoVal
  };

  try {
    const res = await fetch(`${API}/goals/`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => null);
      const detalle = errData?.detail?.[0]?.msg || errData?.detail || "Error al crear OKR.";
      mostrarMensajeOKR("goalFormMsg", "error", detalle);
      return;
    }

    mostrarMensajeOKR("goalFormMsg", "success", "OKR creado correctamente.");
    e.target.reset();

  } catch (err) {
    mostrarMensajeOKR("goalFormMsg", "error", "Error de red. Verifica tu conexión.");
    console.error(err);
  }
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
  const val = Number(progreso);

  if (val < 0 || val > 100) {
    mostrarMensajeOKR("goalUpdateMsg", "error", "El progreso debe estar entre 0 y 100.");
    return;
  }

  try {
    const res = await fetch(`${API}/goals/${id}/progress?progreso=${encodeURIComponent(val)}`, {
      method: 'PUT'
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => null);
      const detalle = errData?.detail || "Error al actualizar progreso.";
      mostrarMensajeOKR("goalUpdateMsg", "error", detalle);
      return;
    }

    mostrarMensajeOKR("goalUpdateMsg", "success", "Progreso actualizado correctamente.");

    const empleadoId = document.getElementById('empleadoBuscar').value;
    if (empleadoId) cargarObjetivosEmpleado(empleadoId);

  } catch (err) {
    mostrarMensajeOKR("goalUpdateMsg", "error", "Error de red al actualizar progreso.");
    console.error(err);
  }
}

// buscar objetivos por empleado
document.getElementById('buscarObjetivosBtn').addEventListener('click', (e) => {
  e.preventDefault();
  const id = document.getElementById('empleadoBuscar').value;
  if (!id) {
    mostrarMensajeOKR("goalUpdateMsg", "error", "Ingresa el ID del empleado.");
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