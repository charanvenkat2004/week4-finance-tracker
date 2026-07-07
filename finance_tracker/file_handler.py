import json
import csv
import os
import shutil
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
BACKUP_DIR = DATA_DIR / "backup"
EXPORTS_DIR = DATA_DIR / "exports"
DATA_FILE = DATA_DIR / "expenses.json"

for directory in [DATA_DIR, BACKUP_DIR, EXPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def save_expenses(expenses_dict, budgets_dict):
    try:
        data = {
            "expenses": expenses_dict,
            "budgets": budgets_dict,
            "last_updated": datetime.now().isoformat()
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        create_backup()
        return True
    except (IOError, PermissionError) as e:
        raise IOError(f"Failed to save data: {e}")


def load_expenses():
    try:
        if not DATA_FILE.exists():
            return [], {}
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        expenses = data.get("expenses", [])
        budgets = data.get("budgets", {})
        return expenses, budgets
    except json.JSONDecodeError:
        backup_path = attempt_recovery()
        if backup_path:
            return load_backup(backup_path)
        return [], {}
    except (IOError, PermissionError) as e:
        raise IOError(f"Failed to load data: {e}")


def create_backup():
    try:
        if not DATA_FILE.exists():
            return False
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"expenses_backup_{timestamp}.json"
        shutil.copy2(DATA_FILE, backup_file)
        cleanup_old_backups(max_backups=20)
        return True
    except (IOError, PermissionError, shutil.Error):
        return False


def cleanup_old_backups(max_backups=20):
    try:
        backups = sorted(BACKUP_DIR.glob("expenses_backup_*.json"), reverse=True)
        for old_backup in backups[max_backups:]:
            old_backup.unlink()
    except (IOError, PermissionError):
        pass


def attempt_recovery():
    try:
        backups = sorted(BACKUP_DIR.glob("expenses_backup_*.json"), reverse=True)
        if backups:
            return backups[0]
        return None
    except (IOError, PermissionError):
        return None


def list_backups():
    try:
        backups = sorted(BACKUP_DIR.glob("expenses_backup_*.json"), reverse=True)
        result = []
        for b in backups:
            stats = b.stat()
            timestamp_str = b.stem.replace("expenses_backup_", "")
            try:
                ts = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                size = stats.st_size
                result.append({
                    "path": str(b),
                    "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "size": size
                })
            except ValueError:
                continue
        return result
    except (IOError, PermissionError):
        return []


def load_backup(backup_path):
    try:
        with open(backup_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        expenses = data.get("expenses", [])
        budgets = data.get("budgets", {})
        return expenses, budgets
    except (json.JSONDecodeError, IOError, PermissionError):
        return [], {}


def restore_from_backup(timestamp_str):
    backup_file = BACKUP_DIR / f"expenses_backup_{timestamp_str}.json"
    if not backup_file.exists():
        backups = list_backups()
        for b in backups:
            if timestamp_str in b["path"]:
                backup_file = Path(b["path"])
                break
        else:
            raise FileNotFoundError(f"No backup found matching '{timestamp_str}'")
    shutil.copy2(backup_file, DATA_FILE)
    expenses, budgets = load_backup(backup_file)
    return expenses, budgets


def export_to_csv(expense_list, filename=None):
    try:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = EXPORTS_DIR / f"expenses_export_{timestamp}.csv"
        else:
            filename = Path(filename)
            if not filename.suffix:
                filename = filename.with_suffix(".csv")
            if filename.parent == Path("."):
                filename = EXPORTS_DIR / filename.name
        with open(filename, "w", encoding="utf-8", newline="") as f:
            if expense_list:
                writer = csv.DictWriter(f, fieldnames=expense_list[0].keys())
                writer.writeheader()
                writer.writerows(expense_list)
        return str(filename)
    except (IOError, PermissionError) as e:
        raise IOError(f"Failed to export CSV: {e}")


def import_from_csv(filepath):
    try:
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            expenses = []
            for row in reader:
                expense = {
                    "date": row.get("date", ""),
                    "amount": float(row.get("amount", 0)),
                    "category": row.get("category", "Other"),
                    "description": row.get("description", ""),
                    "created_at": row.get("created_at", datetime.now().isoformat())
                }
                expenses.append(expense)
        return expenses
    except FileNotFoundError:
        raise
    except (IOError, PermissionError) as e:
        raise IOError(f"Failed to import CSV: {e}")
    except (ValueError, KeyError) as e:
        raise ValueError(f"Invalid CSV format: {e}")


def get_data_file_size():
    try:
        if DATA_FILE.exists():
            return DATA_FILE.stat().st_size
        return 0
    except (IOError, PermissionError):
        return 0
