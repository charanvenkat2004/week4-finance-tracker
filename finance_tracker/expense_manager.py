from datetime import datetime, timedelta
from .expense import Expense
from .utils import CATEGORIES


class ExpenseManager:
    def __init__(self):
        self._expenses = []
        self._budgets = {}

    @property
    def expenses(self):
        return self._expenses.copy()

    @expenses.setter
    def expenses(self, value):
        self._expenses = list(value)

    def add_expense(self, expense):
        if not isinstance(expense, Expense):
            raise TypeError("Must be an Expense object")
        expense.validate()
        self._expenses.append(expense)
        return True

    def remove_expense(self, index):
        if 0 <= index < len(self._expenses):
            removed = self._expenses.pop(index)
            return removed
        return None

    def get_expense(self, index):
        if 0 <= index < len(self._expenses):
            return self._expenses[index]
        return None

    def edit_expense(self, index, **kwargs):
        expense = self.get_expense(index)
        if not expense:
            return None
        if "date" in kwargs:
            expense.date = kwargs["date"]
        if "amount" in kwargs:
            expense.amount = kwargs["amount"]
        if "category" in kwargs:
            expense.category = kwargs["category"]
        if "description" in kwargs:
            expense.description = kwargs["description"]
        expense.validate()
        return expense

    def search_expenses(self, query):
        query = query.lower().strip()
        if not query:
            return self._expenses.copy()
        results = []
        for exp in self._expenses:
            if (query in exp.description.lower() or
                query in exp.category.lower() or
                query in exp.date or
                query in str(exp.amount)):
                results.append(exp)
        return results

    def filter_by_category(self, category):
        cat = category.strip().title()
        return [exp for exp in self._expenses if exp.category == cat]

    def filter_by_date_range(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if start > end:
                start, end = end, start
            end = end + timedelta(days=1)
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        return [exp for exp in self._expenses if start <= datetime.strptime(exp.date, "%Y-%m-%d") < end]

    def get_expenses_by_month(self, year, month):
        return [exp for exp in self._expenses
                if exp.date.startswith(f"{year:04d}-{month:02d}")]

    def get_total_spent(self, expense_list=None):
        if expense_list is None:
            expense_list = self._expenses
        return sum(exp.amount for exp in expense_list)

    def get_category_breakdown(self, expense_list=None):
        if expense_list is None:
            expense_list = self._expenses
        breakdown = {cat: 0.0 for cat in CATEGORIES}
        for exp in expense_list:
            if exp.category in breakdown:
                breakdown[exp.category] += exp.amount
            else:
                breakdown[exp.category] = exp.amount
        return {k: v for k, v in breakdown.items() if v > 0}

    def get_monthly_summary(self, year, month):
        monthly = self.get_expenses_by_month(year, month)
        total = self.get_total_spent(monthly)
        breakdown = self.get_category_breakdown(monthly)
        return {
            "year": year,
            "month": month,
            "total": total,
            "count": len(monthly),
            "breakdown": breakdown,
            "average": total / len(monthly) if monthly else 0
        }

    def get_statistics(self):
        if not self._expenses:
            return {
                "total_expenses": 0,
                "total_spent": 0.0,
                "average_per_expense": 0.0,
                "min_expense": 0.0,
                "max_expense": 0.0,
                "median_expense": 0.0,
                "most_common_category": "N/A",
                "busiest_month": "N/A"
            }
        amounts = [exp.amount for exp in self._expenses]
        amounts.sort()
        n = len(amounts)
        median = amounts[n // 2] if n % 2 == 1 else (amounts[n // 2 - 1] + amounts[n // 2]) / 2
        category_counts = {}
        for exp in self._expenses:
            category_counts[exp.category] = category_counts.get(exp.category, 0) + 1
        most_common = max(category_counts, key=category_counts.get)
        month_counts = {}
        for exp in self._expenses:
            month_key = exp.date[:7]
            month_counts[month_key] = month_counts.get(month_key, 0) + 1
        busiest = max(month_counts, key=month_counts.get) if month_counts else "N/A"
        return {
            "total_expenses": n,
            "total_spent": sum(amounts),
            "average_per_expense": sum(amounts) / n,
            "min_expense": amounts[0],
            "max_expense": amounts[-1],
            "median_expense": median,
            "most_common_category": most_common,
            "busiest_month": busiest
        }

    def set_budget(self, category, amount):
        if amount < 0:
            raise ValueError("Budget cannot be negative")
        cat = category.strip().title()
        self._budgets[cat] = amount
        return True

    def get_budget(self, category):
        cat = category.strip().title()
        return self._budgets.get(cat, 0.0)

    def get_all_budgets(self):
        return self._budgets.copy()

    def get_budget_status(self, category):
        cat = category.strip().title()
        budget = self._budgets.get(cat, 0.0)
        if budget == 0:
            return {"category": cat, "budget": 0, "spent": 0, "remaining": 0, "percentage": 0}
        spent = sum(exp.amount for exp in self._expenses if exp.category == cat)
        return {
            "category": cat,
            "budget": budget,
            "spent": spent,
            "remaining": budget - spent,
            "percentage": (spent / budget) * 100 if budget > 0 else 0
        }

    def get_expense_count(self):
        return len(self._expenses)

    def get_all_expenses_sorted(self, key="date", reverse=False):
        valid_keys = {"date", "amount", "category"}
        if key not in valid_keys:
            key = "date"
        return sorted(self._expenses, key=lambda e: getattr(e, key), reverse=reverse)

    def clear_all_expenses(self):
        self._expenses.clear()
        return True
