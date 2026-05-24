import httpx
import hashlib
import json

class MintHCMClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.session_id = self._login(username, password)

    def _login(self, username: str, password: str) -> str:
        pwd_hash = hashlib.md5(password.encode()).hexdigest()
        rest_data = json.dumps({
            "user_auth": {
                "user_name": username,
                "password": pwd_hash
            }
        })
        response = httpx.post(
            f"{self.base_url}/index.php",
            params={"entryPoint": "SugarRestServlet"},
            data={
                "method": "login",
                "input_type": "JSON",
                "response_type": "JSON",
                "rest_data": rest_data
            }
        )
        data = response.json()
        return data.get("id", "")

    def get_employees(self):
        response = httpx.get(
            f"{self.base_url}/index.php",
            params={
                "entryPoint": "SugarRestServlet",
                "method": "get_entry_list",
                "module": "Employees",
                "session": self.session_id,
                "input_type": "JSON",
                "response_type": "JSON",
                "rest_data": json.dumps({})
            }
        )
        return response.json()

    def get_departments(self):
        response = httpx.get(
            f"{self.base_url}/index.php",
            params={
                "entryPoint": "SugarRestServlet",
                "method": "get_entry_list",
                "module": "Departments",
                "session": self.session_id,
                "input_type": "JSON",
                "response_type": "JSON",
                "rest_data": json.dumps({})
            }
        )
        return response.json()