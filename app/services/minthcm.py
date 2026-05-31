import httpx
import hashlib
import json

class MintHCMClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.api_url = f"{base_url}/service/v4_1/rest.php"
        self.session_id = self._login(username, password)

    def _login(self, username: str, password: str) -> str:
        pwd_hash = hashlib.md5(password.encode()).hexdigest()
        rest_data = json.dumps({
            "user_auth": {
                "user_name": username,
                "password": pwd_hash
            },
            "application_name": "PerformTrack"
        })
        try:
            response = httpx.post(
                self.api_url,
                data={
                    "method": "login",
                    "input_type": "JSON",
                    "response_type": "JSON",
                    "rest_data": rest_data
                },
                timeout=10.0
            )
            data = response.json()
            return data.get("id", "")
        except Exception as e:
            print(f"Login error: {e}")
            return ""

    def get_employees(self):
        try:
            rest_data = json.dumps({
                "session": self.session_id,
                "module_name": "Employees",
                "query": "",
                "order_by": "",
                "offset": 0,
                "select_fields": ["id", "first_name", "last_name", "email1"],
                "link_name_to_fields_array": [],
                "max_results": 20,
                "deleted": 0
            })
            response = httpx.post(
                self.api_url,
                data={
                    "method": "get_entry_list",
                    "input_type": "JSON",
                    "response_type": "JSON",
                    "rest_data": rest_data
                },
                timeout=10.0
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_departments(self):
        try:
            rest_data = json.dumps({
                "session": self.session_id,
                "module_name": "SecurityGroups",
                "query": "",
                "order_by": "",
                "offset": 0,
                "select_fields": ["id", "name", "description"],
                "link_name_to_fields_array": [],
                "max_results": 50,
                "deleted": 0
            })
            response = httpx.post(
                self.api_url,
                data={
                    "method": "get_entry_list",
                    "input_type": "JSON",
                    "response_type": "JSON",
                    "rest_data": rest_data
                },
                timeout=10.0
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_positions(self):
        try:
            rest_data = json.dumps({
                "session": self.session_id,
                "module_name": "Positions",
                "query": "",
                "order_by": "",
                "offset": 0,
                "select_fields": ["id", "name"],
                "link_name_to_fields_array": [],
                "max_results": 50,
                "deleted": 0
            })
            response = httpx.post(
                self.api_url,
                data={
                    "method": "get_entry_list",
                    "input_type": "JSON",
                    "response_type": "JSON",
                    "rest_data": rest_data
                },
                timeout=10.0
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}