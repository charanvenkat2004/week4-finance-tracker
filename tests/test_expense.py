import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from finance_tracker.expense import Expense
from finance_tracker.expense_manager import ExpenseManager
from finance_tracker.utils import CATEGORIES


class TestExpenseCreation(unittest.TestCase):
    def test_create_expense(self):
        exp = Expense("2026-07-07", 25.50, "Food", "Lunch")
        self.assertEqual(exp.date, "2026-07-07")
        self.assertEqual(exp.amount, 25.50)
        self.assertEqual(exp.category, "Food")
        self.assertEqual(exp.description, "Lunch")

    def test_expense_to_dict(self):
        exp = Expense("2026-07-07", 25.50, "Food", "Lunch")
        d = exp.to_dict()
        self.assertEqual(d["date"], "2026-07-07")
        self.assertEqual(d["amount"], 25.50)
        self.assertEqual(d["category"], "Food")
        self.assertEqual(d["description"], "Lunch")
        self.assertIn("created_at", d)

    def test_expense_from_dict(self):
        data = {
            "date": "2026-07-07",
            "amount": 15.00,
            "category": "Transport",
            "description": "Bus fare"
        }
        exp = Expense.from_dict(data)
        self.assertEqual(exp.date, "2026-07-07")
        self.assertEqual(exp.amount, 15.00)
        self.assertEqual(exp.category, "Transport")
        self.assertEqual(exp.description, "Bus fare")

    def test_expense_roundtrip(self):
        original = Expense("2026-07-07", 99.99, "Entertainment", "Movie tickets")
        data = original.to_dict()
        restored = Expense.from_dict(data)
        self.assertEqual(original.date, restored.date)
        self.assertEqual(original.amount, restored.amount)
        self.assertEqual(original.category, restored.category)
        self.assertEqual(original.description, restored.description)

    def test_valid_expense_passes_validation(self):
        exp = Expense("2026-07-07", 50.00, "Food", "Groceries")
        self.assertTrue(exp.validate())

    def test_invalid_amount_raises_error(self):
        with self.assertRaises(ValueError):
            exp = Expense("2026-07-07", -10, "Food", "Test")
            exp.validate()

    def test_zero_amount_raises_error(self):
        with self.assertRaises(ValueError):
            exp = Expense("2026-07-07", 0, "Food", "Test")
            exp.validate()

    def test_invalid_date_raises_error(self):
        with self.assertRaises(ValueError):
            exp = Expense("13-32-2026", 10, "Food", "Test")
            exp.validate()

    def test_invalid_category_raises_error(self):
        with self.assertRaises(ValueError):
            exp = Expense("2026-07-07", 10, "InvalidCat!", "Test")
            exp.validate()

    def test_empty_description_raises_error(self):
        with self.assertRaises(ValueError):
            exp = Expense("2026-07-07", 10, "Food", "  ")
            exp.validate()

    def test_long_description_raises_error(self):
        with self.assertRaises(ValueError):
            exp = Expense("2026-07-07", 10, "Food", "x" * 201)
            exp.validate()

    def test_str_representation(self):
        exp = Expense("2026-07-07", 25.50, "Food", "Lunch")
        str_repr = str(exp)
        self.assertIn("2026-07-07", str_repr)
        self.assertIn("Food", str_repr)
        self.assertIn("25.50", str_repr)


class TestExpenseManager(unittest.TestCase):
    def setUp(self):
        self.manager = ExpenseManager()

    def test_add_expense(self):
        exp = Expense("2026-07-07", 25.00, "Food", "Lunch")
        self.assertTrue(self.manager.add_expense(exp))
        self.assertEqual(self.manager.get_expense_count(), 1)

    def test_add_invalid_type_raises_error(self):
        with self.assertRaises(TypeError):
            self.manager.add_expense("not an expense")

    def test_remove_expense(self):
        exp = Expense("2026-07-07", 25.00, "Food", "Lunch")
        self.manager.add_expense(exp)
        removed = self.manager.remove_expense(0)
        self.assertIsNotNone(removed)
        self.assertEqual(removed.description, "Lunch")
        self.assertEqual(self.manager.get_expense_count(), 0)

    def test_remove_out_of_range(self):
        self.assertIsNone(self.manager.remove_expense(99))

    def test_get_expense(self):
        exp = Expense("2026-07-07", 25.00, "Food", "Lunch")
        self.manager.add_expense(exp)
        self.assertIsNotNone(self.manager.get_expense(0))
        self.assertIsNone(self.manager.get_expense(99))

    def test_edit_expense(self):
        exp = Expense("2026-07-07", 25.00, "Food", "Lunch")
        self.manager.add_expense(exp)
        edited = self.manager.edit_expense(0, amount=30.00, description="Dinner")
        self.assertIsNotNone(edited)
        self.assertEqual(edited.amount, 30.00)
        self.assertEqual(edited.description, "Dinner")

    def test_search_expenses(self):
        self.manager.add_expense(Expense("2026-07-07", 25.00, "Food", "Lunch"))
        self.manager.add_expense(Expense("2026-07-08", 10.00, "Transport", "Bus"))
        results = self.manager.search_expenses("Lunch")
        self.assertEqual(len(results), 1)
        results = self.manager.search_expenses("")
        self.assertEqual(len(results), 2)

    def test_filter_by_category(self):
        self.manager.add_expense(Expense("2026-07-07", 25.00, "Food", "Lunch"))
        self.manager.add_expense(Expense("2026-07-08", 10.00, "Transport", "Bus"))
        food = self.manager.filter_by_category("Food")
        self.assertEqual(len(food), 1)
        self.assertEqual(food[0].category, "Food")

    def test_filter_by_date_range(self):
        self.manager.add_expense(Expense("2026-07-07", 25.00, "Food", "Lunch"))
        self.manager.add_expense(Expense("2026-07-08", 10.00, "Transport", "Bus"))
        self.manager.add_expense(Expense("2026-07-10", 50.00, "Food", "Dinner"))
        results = self.manager.filter_by_date_range("2026-07-07", "2026-07-08")
        self.assertEqual(len(results), 2)

    def test_get_total_spent(self):
        self.manager.add_expense(Expense("2026-07-07", 25.00, "Food", "Lunch"))
        self.manager.add_expense(Expense("2026-07-08", 10.00, "Transport", "Bus"))
        self.assertEqual(self.manager.get_total_spent(), 35.00)

    def test_get_total_spent_empty(self):
        self.assertEqual(self.manager.get_total_spent(), 0)

    def test_get_category_breakdown(self):
        self.manager.add_expense(Expense("2026-07-07", 25.00, "Food", "Lunch"))
        self.manager.add_expense(Expense("2026-07-08", 10.00, "Transport", "Bus"))
        self.manager.add_expense(Expense("2026-07-09", 15.00, "Food", "Dinner"))
        breakdown = self.manager.get_category_breakdown()
        self.assertEqual(breakdown.get("Food"), 40.00)
        self.assertEqual(breakdown.get("Transport"), 10.00)

    def test_get_monthly_summary(self):
        self.manager.add_expense(Expense("2026-07-07", 25.00, "Food", "Lunch"))
        self.manager.add_expense(Expense("2026-07-08", 10.00, "Transport", "Bus"))
        summary = self.manager.get_monthly_summary(2026, 7)
        self.assertEqual(summary["count"], 2)
        self.assertEqual(summary["total"], 35.00)
        self.assertEqual(summary["average"], 17.50)

    def test_empty_monthly_summary(self):
        summary = self.manager.get_monthly_summary(2026, 1)
        self.assertEqual(summary["count"], 0)
        self.assertEqual(summary["total"], 0)

    def test_set_and_get_budget(self):
        self.manager.set_budget("Food", 500.00)
        self.assertEqual(self.manager.get_budget("Food"), 500.00)

    def test_negative_budget_raises_error(self):
        with self.assertRaises(ValueError):
            self.manager.set_budget("Food", -100)

    def test_budget_status(self):
        self.manager.set_budget("Food", 100.00)
        self.manager.add_expense(Expense("2026-07-07", 25.00, "Food", "Lunch"))
        status = self.manager.get_budget_status("Food")
        self.assertEqual(status["budget"], 100.00)
        self.assertEqual(status["spent"], 25.00)
        self.assertEqual(status["remaining"], 75.00)
        self.assertEqual(status["percentage"], 25.0)

    def test_get_statistics(self):
        self.manager.add_expense(Expense("2026-07-07", 25.00, "Food", "Lunch"))
        self.manager.add_expense(Expense("2026-07-08", 10.00, "Transport", "Bus"))
        self.manager.add_expense(Expense("2026-07-09", 50.00, "Entertainment", "Movies"))
        stats = self.manager.get_statistics()
        self.assertEqual(stats["total_expenses"], 3)
        self.assertEqual(stats["total_spent"], 85.00)

    def test_get_statistics_empty(self):
        stats = self.manager.get_statistics()
        self.assertEqual(stats["total_expenses"], 0)

    def test_clear_all_expenses(self):
        self.manager.add_expense(Expense("2026-07-07", 25.00, "Food", "Lunch"))
        self.manager.clear_all_expenses()
        self.assertEqual(self.manager.get_expense_count(), 0)

    def test_get_expenses_sorted_by_date(self):
        self.manager.add_expense(Expense("2026-07-10", 25.00, "Food", "Late"))
        self.manager.add_expense(Expense("2026-07-07", 25.00, "Food", "Early"))
        sorted_exp = self.manager.get_all_expenses_sorted("date")
        self.assertEqual(sorted_exp[0].date, "2026-07-07")
        self.assertEqual(sorted_exp[1].date, "2026-07-10")

    def test_get_all_budgets(self):
        self.manager.set_budget("Food", 500)
        self.manager.set_budget("Transport", 200)
        budgets = self.manager.get_all_budgets()
        self.assertEqual(len(budgets), 2)


if __name__ == "__main__":
    unittest.main()
