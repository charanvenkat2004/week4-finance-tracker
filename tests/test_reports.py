import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from finance_tracker.expense import Expense
from finance_tracker.expense_manager import ExpenseManager
from finance_tracker import reports


class TestReportsGeneration(unittest.TestCase):
    def setUp(self):
        self.manager = ExpenseManager()
        self.manager.add_expense(Expense("2026-07-07", 25.00, "Food", "Lunch"))
        self.manager.add_expense(Expense("2026-07-08", 10.00, "Transport", "Bus"))
        self.manager.add_expense(Expense("2026-07-09", 50.00, "Entertainment", "Movies"))
        self.manager.add_expense(Expense("2026-07-10", 30.00, "Food", "Dinner"))
        self.manager.add_expense(Expense("2026-08-01", 100.00, "Bills", "Electricity"))

    def test_monthly_report_generation(self):
        report = reports.generate_monthly_report(self.manager, 2026, 7)
        self.assertIn("July 2026", report)
        self.assertIn("$115.00", report)
        self.assertIn("4", report)

    def test_monthly_report_empty_month(self):
        report = reports.generate_monthly_report(self.manager, 2025, 1)
        self.assertIn("January 2025", report)

    def test_category_breakdown_generation(self):
        breakdown = reports.generate_category_breakdown(self.manager)
        self.assertIn("Food", breakdown)
        self.assertIn("Transport", breakdown)
        self.assertIn("Entertainment", breakdown)
        self.assertIn("Bills", breakdown)

    def test_category_breakdown_empty(self):
        empty_manager = ExpenseManager()
        breakdown = reports.generate_category_breakdown(empty_manager)
        self.assertIn("No expenses", breakdown)

    def test_trend_analysis_generation(self):
        trend = reports.generate_trend_analysis(self.manager)
        self.assertIn("EXPENSE TREND ANALYSIS", trend)
        self.assertIn("2026-07", trend)
        self.assertIn("2026-08", trend)

    def test_trend_analysis_empty(self):
        empty_manager = ExpenseManager()
        trend = reports.generate_trend_analysis(empty_manager)
        self.assertIn("No expenses", trend)

    def test_statistics_report_generation(self):
        stats = reports.generate_statistics_report(self.manager)
        self.assertIn("5", stats)
        self.assertIn("$215.00", stats)

    def test_statistics_report_empty(self):
        empty_manager = ExpenseManager()
        stats = reports.generate_statistics_report(empty_manager)
        self.assertIn("No expenses", stats)

    def test_budget_report_generation(self):
        self.manager.set_budget("Food", 100.00)
        budget_report = reports.generate_budget_report(self.manager)
        self.assertIn("Food", budget_report)
        self.assertIn("$55.00", budget_report)

    def test_budget_report_no_budgets(self):
        budget_report = reports.generate_budget_report(self.manager)
        self.assertIn("No budgets set", budget_report)

    def test_monthly_report_with_budget_alert(self):
        self.manager.set_budget("Food", 50.00)
        self.manager.add_expense(Expense("2026-07-11", 45.00, "Food", "More food"))
        report = reports.generate_monthly_report(self.manager, 2026, 7)
        self.assertIn("Budget Alerts", report)

    def test_category_breakdown_with_budgets(self):
        self.manager.set_budget("Food", 200.00)
        breakdown = reports.generate_category_breakdown(self.manager)
        self.assertIn("Budget", breakdown)


if __name__ == "__main__":
    unittest.main()
