import os
from dotenv import load_dotenv

load_dotenv()

MINTHCM_BASE_URL = os.getenv("MINTHCM_BASE_URL", "http://localhost")
MINTHCM_USERNAME = os.getenv("MINTHCM_USERNAME", "admin")
MINTHCM_PASSWORD = os.getenv("MINTHCM_PASSWORD", "minthcm")