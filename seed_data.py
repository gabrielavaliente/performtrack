import os
import random
import json
import hashlib
from datetime import datetime, timedelta

import httpx

from app.db.database import SessionLocal, EvaluationForm, EmployeeGoal, KPIRecord


class MintSeeder:
	def __init__(self, base_url: str, username: str, password: str, timeout: float = 10.0):
		self.base_url = base_url.rstrip("/")
		self.api_url = f"{self.base_url}/service/v4_1/rest.php"
		self.timeout = timeout
		self.session_id = self._login(username, password)
		self.user_id = self._get_user_id(username) if self.session_id else ""

	def _login(self, username: str, password: str) -> str:
		pwd_hash = hashlib.md5(password.encode()).hexdigest()
		rest_data = json.dumps(
			{
				"user_auth": {"user_name": username, "password": pwd_hash},
				"application_name": "PerformTrackSeed",
			}
		)
		response = httpx.post(
			self.api_url,
			data={
				"method": "login",
				"input_type": "JSON",
				"response_type": "JSON",
				"rest_data": rest_data,
			},
			timeout=self.timeout,
		)
		data = response.json()
		return data.get("id", "")

	def _get_entry_list(self, module_name: str, query: str, select_fields: list[str]) -> dict:
		rest_data = json.dumps(
			{
				"session": self.session_id,
				"module_name": module_name,
				"query": query,
				"order_by": "",
				"offset": 0,
				"select_fields": select_fields,
				"link_name_to_fields_array": [],
				"max_results": 1,
				"deleted": 0,
			}
		)
		response = httpx.post(
			self.api_url,
			data={
				"method": "get_entry_list",
				"input_type": "JSON",
				"response_type": "JSON",
				"rest_data": rest_data,
			},
			timeout=self.timeout,
		)
		return response.json()

	def _get_user_id(self, username: str) -> str:
		data = self._get_entry_list("Users", f"users.user_name = '{username}'", ["id"])
		entries = data.get("entry_list") or []
		if not entries:
			return ""
		entry = entries[0]
		user_id = entry.get("id", "")
		if user_id:
			return user_id
		name_value_list = entry.get("name_value_list") or {}
		if isinstance(name_value_list, dict):
			value = name_value_list.get("id")
			if isinstance(value, dict):
				return value.get("value", "")
			if isinstance(value, str):
				return value
		return ""

	def get_project_ids(self, max_results: int = 50) -> list[str]:
		rest_data = json.dumps(
			{
				"session": self.session_id,
				"module_name": "Project",
				"query": "",
				"order_by": "",
				"offset": 0,
				"select_fields": ["id"],
				"link_name_to_fields_array": [],
				"max_results": max_results,
				"deleted": 0,
			}
		)
		response = httpx.post(
			self.api_url,
			data={
				"method": "get_entry_list",
				"input_type": "JSON",
				"response_type": "JSON",
				"rest_data": rest_data,
			},
			timeout=self.timeout,
		)
		data = response.json()
		entries = data.get("entry_list") or []
		project_ids: list[str] = []
		for entry in entries:
			entry_id = entry.get("id")
			if entry_id:
				project_ids.append(entry_id)
				continue
			name_value_list = entry.get("name_value_list") or {}
			if isinstance(name_value_list, dict):
				value = name_value_list.get("id")
				if isinstance(value, dict) and value.get("value"):
					project_ids.append(value["value"])
				elif isinstance(value, str):
					project_ids.append(value)
		return project_ids

	def get_employee_ids(self, max_results: int = 50) -> list[str]:
		rest_data = json.dumps(
			{
				"session": self.session_id,
				"module_name": "Employees",
				"query": "",
				"order_by": "",
				"offset": 0,
				"select_fields": ["id"],
				"link_name_to_fields_array": [],
				"max_results": max_results,
				"deleted": 0,
			}
		)
		response = httpx.post(
			self.api_url,
			data={
				"method": "get_entry_list",
				"input_type": "JSON",
				"response_type": "JSON",
				"rest_data": rest_data,
			},
			timeout=self.timeout,
		)
		data = response.json()
		entries = data.get("entry_list") or []
		employee_ids: list[str] = []
		for entry in entries:
			entry_id = entry.get("id")
			if entry_id:
				employee_ids.append(entry_id)
				continue
			name_value_list = entry.get("name_value_list") or {}
			if isinstance(name_value_list, dict):
				value = name_value_list.get("id")
				if isinstance(value, dict) and value.get("value"):
					employee_ids.append(value["value"])
				elif isinstance(value, str):
					employee_ids.append(value)
		return employee_ids

	def _set_entry(self, module_name: str, fields: dict) -> dict:
		name_value_list = [{"name": key, "value": value} for key, value in fields.items()]
		rest_data = json.dumps(
			{
				"session": self.session_id,
				"module_name": module_name,
				"name_value_list": name_value_list,
			}
		)
		response = httpx.post(
			self.api_url,
			data={
				"method": "set_entry",
				"input_type": "JSON",
				"response_type": "JSON",
				"rest_data": rest_data,
			},
			timeout=self.timeout,
		)
		return response.json()

	def _extract_id(self, data: dict) -> str:
		return data.get("id", "")

	def create_employee(self, fields: dict) -> tuple[str, dict]:
		data = self._set_entry("Employees", fields)
		return self._extract_id(data), data

	def create_project(self, fields: dict) -> tuple[str, dict]:
		data = self._set_entry("Project", fields)
		return self._extract_id(data), data

	def create_project_task(self, fields: dict) -> tuple[str, dict]:
		data = self._set_entry("ProjectTask", fields)
		return self._extract_id(data), data


def _rand_date_range(start_days: int, span_days: int) -> tuple[str, str]:
	start = datetime.utcnow().date() + timedelta(days=start_days)
	end = start + timedelta(days=span_days)
	return start.isoformat(), end.isoformat()


def _percent(actual: float, target: float) -> float:
	if target <= 0:
		return 0.0
	return round((actual / target) * 100.0, 2)


def main() -> None:
	random.seed(42)

	base_url = os.getenv("MINT_BASE_URL", "http://localhost")
	username = os.getenv("MINT_USERNAME", "admin")
	password = os.getenv("MINT_PASSWORD", "minthcm")

	employee_count = int(os.getenv("SEED_EMPLOYEES", "20"))
	project_count = int(os.getenv("SEED_PROJECTS", "10"))
	tasks_per_project = int(os.getenv("SEED_TASKS_PER_PROJECT", "5"))

	create_mint_data = os.getenv("SEED_MINT", "true").lower() == "true"
	create_performtrack_data = os.getenv("SEED_PERFORMTRACK", "true").lower() == "true"
	seed_employees = os.getenv("SEED_EMPLOYEES_ENABLED", "true").lower() == "true"
	seed_projects = os.getenv("SEED_PROJECTS_ENABLED", "true").lower() == "true"
	seed_tasks = os.getenv("SEED_TASKS_ENABLED", "true").lower() == "true"
	seed_evaluations = os.getenv("SEED_EVALUATIONS_ENABLED", "true").lower() == "true"
	seed_goals = os.getenv("SEED_GOALS_ENABLED", "true").lower() == "true"
	seed_kpis = os.getenv("SEED_KPIS_ENABLED", "true").lower() == "true"
	use_mint_employees = os.getenv("SEED_USE_MINT_EMPLOYEES", "true").lower() == "true"
	mint_employee_limit = int(os.getenv("SEED_MINT_EMPLOYEE_LIMIT", str(employee_count)))
	verbose = os.getenv("SEED_VERBOSE", "false").lower() == "true"

	employees_created: list[str] = []
	projects_created: list[str] = []

	mint = None
	if create_mint_data:
		mint = MintSeeder(base_url=base_url, username=username, password=password)
		if not mint.session_id:
			print("MintHCM login failed. Skipping MintHCM seed.")
			mint = None

	if mint:
		if not mint.user_id:
			print("No user id found for assigned_user_id. Projects/tasks will be unassigned.")

		project_ids_for_tasks: list[str] = []
		if seed_projects:
			project_ids_for_tasks = []
		else:
			project_ids_for_tasks = mint.get_project_ids(max_results=project_count)
			if not project_ids_for_tasks:
				print("No existing projects found. Project tasks will be skipped.")

		employee_seed = [
			{"first": "Ana", "last": "Gomez", "department": "HR", "title": "HR Specialist"},
			{"first": "Luis", "last": "Perez", "department": "IT", "title": "Systems Analyst"},
			{"first": "Maria", "last": "Lopez", "department": "Finance", "title": "Accountant"},
			{"first": "Jorge", "last": "Ramos", "department": "Sales", "title": "Account Executive"},
			{"first": "Sofia", "last": "Vega", "department": "Operations", "title": "Operations Lead"},
			{"first": "Pedro", "last": "Torres", "department": "IT", "title": "DevOps Engineer"},
			{"first": "Lucia", "last": "Diaz", "department": "Marketing", "title": "Marketing Analyst"},
			{"first": "Carlos", "last": "Castro", "department": "IT", "title": "Software Engineer"},
			{"first": "Valeria", "last": "Ruiz", "department": "HR", "title": "Recruiter"},
			{"first": "Diego", "last": "Mendoza", "department": "Finance", "title": "Financial Analyst"},
			{"first": "Gabriela", "last": "Santos", "department": "Sales", "title": "Sales Manager"},
			{"first": "Andres", "last": "Nunez", "department": "Operations", "title": "Operations Coordinator"},
			{"first": "Camila", "last": "Ortega", "department": "IT", "title": "QA Engineer"},
			{"first": "Miguel", "last": "Herrera", "department": "IT", "title": "Product Manager"},
			{"first": "Paula", "last": "Silva", "department": "Marketing", "title": "Content Specialist"},
			{"first": "Ricardo", "last": "Navarro", "department": "Operations", "title": "Logistics Lead"},
			{"first": "Natalia", "last": "Vargas", "department": "Finance", "title": "Payroll Specialist"},
			{"first": "Daniel", "last": "Morales", "department": "IT", "title": "Data Engineer"},
			{"first": "Elena", "last": "Paredes", "department": "HR", "title": "People Partner"},
			{"first": "Rafael", "last": "Cruz", "department": "Sales", "title": "Sales Development Rep"},
		]
		email_domains = ["empresa.com", "mintlab.io", "performtrack.app"]
		phone_prefix = "+1-312-555-"

		for idx in range(employee_count):
			if not seed_employees:
				break
			if idx < len(employee_seed):
				seed = employee_seed[idx]
				first = seed["first"]
				last = seed["last"]
				department = seed["department"]
				title = seed["title"]
			else:
				first = random.choice(["Andrea", "Jose", "Mario", "Laura", "Rosa", "Hector"])
				last = random.choice(["Luna", "Campos", "Reyes", "Flores", "Suarez", "Prieto"])
				department = random.choice(["IT", "HR", "Finance", "Sales", "Operations", "Marketing"])
				title = random.choice(
					[
						"Specialist",
						"Coordinator",
						"Lead",
						"Senior Analyst",
						"Associate",
						"Manager",
					]
				)

			username_seed = f"{first}.{last}.{idx}".lower()
			email_domain = random.choice(email_domains)
			fields = {
				"first_name": first,
				"last_name": last,
				"user_name": username_seed,
				"status": "Active",
				"employee_status": "Active",
				"department": department,
				"title": title,
				"email1": f"{first}.{last}@{email_domain}".lower(),
				"phone_work": f"{phone_prefix}{100 + idx}",
			}
			employee_id, employee_data = mint.create_employee(fields)
			if employee_id:
				employees_created.append(employee_id)
			else:
				print(f"Failed to create employee {first} {last}")
				if verbose:
					print(employee_data)

		for idx in range(project_count):
			if not seed_projects:
				break
			start_date, end_date = _rand_date_range(idx * 7, 30 + idx * 3)
			project_fields = {
				"name": f"Proyecto {idx + 1}",
				"status": "In Progress",
				"priority": "High",
				"estimated_start_date": start_date,
				"estimated_end_date": end_date,
				"description": "Proyecto semilla generado por PerformTrack",
			}
			if mint.user_id:
				project_fields["assigned_user_id"] = mint.user_id
			project_id, project_data = mint.create_project(project_fields)
			if project_id:
				projects_created.append(project_id)
				project_ids_for_tasks.append(project_id)
			else:
				print(f"Failed to create project {idx + 1}")
				if verbose:
					print(project_data)

			if project_id and seed_tasks:
				for task_idx in range(tasks_per_project):
					task_start, task_end = _rand_date_range(task_idx * 2, 7)
					task_fields = {
						"name": f"Tarea {task_idx + 1} - Proyecto {idx + 1}",
						"project_id": project_id,
						"project_task_id": task_idx + 1,
						"status": "In Progress",
						"percent_complete": random.randint(0, 100),
						"date_start": task_start,
						"date_finish": task_end,
						"description": "Tarea semilla generada por PerformTrack",
					}
					if mint.user_id:
						task_fields["assigned_user_id"] = mint.user_id
					task_id, task_data = mint.create_project_task(task_fields)
					if not task_id:
						print(f"Failed to create task {task_idx + 1} for project {idx + 1}")
						if verbose:
							print(task_data)

		if project_ids_for_tasks and seed_tasks and not seed_projects:
			for project_index, project_id in enumerate(project_ids_for_tasks, start=1):
				for task_idx in range(tasks_per_project):
					task_start, task_end = _rand_date_range(task_idx * 2, 7)
					task_fields = {
						"name": f"Tarea {task_idx + 1} - Proyecto existente {project_index}",
						"project_id": project_id,
						"project_task_id": task_idx + 1,
						"status": "In Progress",
						"percent_complete": random.randint(0, 100),
						"date_start": task_start,
						"date_finish": task_end,
						"description": "Tarea semilla generada por PerformTrack",
					}
					if mint.user_id:
						task_fields["assigned_user_id"] = mint.user_id
					task_id, task_data = mint.create_project_task(task_fields)
					if not task_id:
						print(
							f"Failed to create task {task_idx + 1} for existing project {project_index}"
						)
						if verbose:
							print(task_data)

	if create_performtrack_data and (seed_evaluations or seed_goals or seed_kpis):
		employees_for_performtrack = list(employees_created)
		if (seed_goals or seed_kpis) and not employees_for_performtrack and use_mint_employees:
			mint_for_ids = MintSeeder(base_url=base_url, username=username, password=password)
			if mint_for_ids.session_id:
				employees_for_performtrack = mint_for_ids.get_employee_ids(
					max_results=mint_employee_limit
				)
			else:
				print("MintHCM login failed. Cannot load employee IDs for PerformTrack.")
			if not employees_for_performtrack and verbose:
				print("No employee IDs found for PerformTrack seeding.")

		db = SessionLocal()
		try:
			forms: list[EvaluationForm] = []
			if seed_evaluations:
				forms = [
					EvaluationForm(nombre="Evaluacion Q1", periodo="2026-Q1", estado="Abierta"),
					EvaluationForm(nombre="Evaluacion Q2", periodo="2026-Q2", estado="Abierta"),
					EvaluationForm(nombre="Evaluacion Anual", periodo="2026", estado="Borrador"),
				]
				db.add_all(forms)
				db.commit()
				for form in forms:
					db.refresh(form)

			if employees_for_performtrack and (seed_goals or seed_kpis):
				if not forms:
					forms = db.query(EvaluationForm).all()

				for employee_id in employees_for_performtrack:
					if seed_goals:
						goal = EmployeeGoal(
							empleado_id=employee_id,
							descripcion="Mejorar indicadores clave del equipo",
							objetivo_okr="Aumentar productividad en 15%",
							peso=round(random.uniform(0.2, 0.6), 2),
							progreso=round(random.uniform(10, 90), 2),
						)
						db.add(goal)

					if seed_kpis:
						for form in forms:
							actual = round(random.uniform(40, 120), 2)
							target = round(random.uniform(80, 130), 2)
							kpi = KPIRecord(
								empleado_id=employee_id,
								form_id=form.id,
								kpi_nombre="Cumplimiento de objetivos",
								valor_actual=actual,
								valor_meta=target,
								porcentaje=_percent(actual, target),
							)
							db.add(kpi)

				db.commit()
		finally:
			db.close()

	print("Seed completado")
	if employees_created:
		print(f"Employees creados: {len(employees_created)}")
	if projects_created:
		print(f"Projects creados: {len(projects_created)}")


if __name__ == "__main__":
	main()
