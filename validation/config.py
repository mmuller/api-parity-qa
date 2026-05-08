import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
DB_PATH = os.getenv("DB_PATH", "../api-parity-lab/test.db")
LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../api-parity-lab/logs/app.log")
)
