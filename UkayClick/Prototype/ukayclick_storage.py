import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
FILES = {
    "users": DATA_DIR / "users.json",
    "inventory": DATA_DIR / "inventory.json",
    "transactions": DATA_DIR / "transactions.json",
    "expenses": DATA_DIR / "expenses.json",
}

def _read(name):
    path = FILES[name]
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

def _write(name, data):
    FILES[name].write_text(json.dumps(data, indent=2), encoding="utf-8")

def load_users(): return _read("users")
def save_users(data): _write("users", data)
def load_inventory(): return _read("inventory")
def save_inventory(data): _write("inventory", data)
def load_transactions(): return _read("transactions")
def save_transactions(data): _write("transactions", data)
def load_expenses(): return _read("expenses")
def save_expenses(data): _write("expenses", data)

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
