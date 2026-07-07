import unittest
import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from finance_tracker import file_handler


class TestFileHandlerSaveLoad(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_data_dir = file_handler.DATA_DIR
        self.original_backup_dir = file_handler.BACKUP_DIR
        self.original_exports_dir = file_handler.EXPORTS_DIR
        self.original_data_file = file_handler.DATA_FILE
        file_handler.DATA_DIR = Path(self.temp_dir)
        file_handler.BACKUP_DIR = file_handler.DATA_DIR / "backup"
        file_handler.EXPORTS_DIR = file_handler.DATA_DIR / "exports"
        file_handler.DATA_FILE = file_handler.DATA_DIR / "expenses.json"
        file_handler.BACKUP_DIR.mkdir(exist_ok=True)
        file_handler.EXPORTS_DIR.mkdir(exist_ok=True)

    def tearDown(self):
        file_handler.DATA_DIR = self.original_data_dir
        file_handler.BACKUP_DIR = self.original_backup_dir
        file_handler.EXPORTS_DIR = self.original_exports_dir
        file_handler.DATA_FILE = self.original_data_file
        shutil.rmtree(self.temp_dir)

    def test_save_and_load_expenses(self):
        expenses = [
            {"date": "2026-07-07", "amount": 25.00, "category": "Food", "description": "Lunch"}
        ]
        budgets = {"Food": 500.0}
        self.assertTrue(file_handler.save_expenses(expenses, budgets))
        loaded_expenses, loaded_budgets = file_handler.load_expenses()
        self.assertEqual(len(loaded_expenses), 1)
        self.assertEqual(loaded_expenses[0]["date"], "2026-07-07")
        self.assertEqual(loaded_budgets["Food"], 500.0)

    def test_load_no_file(self):
        expenses, budgets = file_handler.load_expenses()
        self.assertEqual(expenses, [])
        self.assertEqual(budgets, {})

    def test_corrupted_file_recovery(self):
        with open(file_handler.DATA_FILE, "w") as f:
            f.write("not valid json")
        expenses, budgets = file_handler.load_expenses()
        self.assertEqual(expenses, [])
        self.assertEqual(budgets, {})

    def test_create_backup(self):
        expenses = [{"date": "2026-07-07", "amount": 25.00, "category": "Food", "description": "Lunch"}]
        file_handler.save_expenses(expenses, {})
        backups = file_handler.list_backups()
        self.assertGreater(len(backups), 0)

    def test_list_backups_empty(self):
        backups = file_handler.list_backups()
        self.assertEqual(backups, [])

    def test_export_csv(self):
        expenses = [
            {"date": "2026-07-07", "amount": 25.00, "category": "Food", "description": "Lunch"}
        ]
        path = file_handler.export_to_csv(expenses, "test_export")
        self.assertTrue(os.path.exists(path))
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("date", content)
        self.assertIn("2026-07-07", content)
        self.assertIn("25.0", content)

    def test_export_empty_list(self):
        path = file_handler.export_to_csv([], "empty_export")
        self.assertTrue(os.path.exists(path))

    def test_import_csv(self):
        expenses = [
            {"date": "2026-07-07", "amount": 25.00, "category": "Food", "description": "Lunch"}
        ]
        path = file_handler.export_to_csv(expenses, "test_import")
        imported = file_handler.import_from_csv(path)
        self.assertEqual(len(imported), 1)
        self.assertEqual(imported[0]["description"], "Lunch")

    def test_import_nonexistent_csv(self):
        with self.assertRaises(FileNotFoundError):
            file_handler.import_from_csv("nonexistent_file.csv")


if __name__ == "__main__":
    unittest.main()
