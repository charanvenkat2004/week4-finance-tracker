from datetime import datetime
from .utils import validate_amount, validate_date, validate_category, validate_description, CATEGORIES


class Expense:
    def __init__(self, date, amount, category, description):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description
        self.created_at = datetime.now().isoformat()

    @classmethod
    def from_dict(cls, data):
        expense = cls(
            date=data.get("date", datetime.now().strftime("%Y-%m-%d")),
            amount=data.get("amount", 0.0),
            category=data.get("category", "Other"),
            description=data.get("description", "")
        )
        expense.created_at = data.get("created_at", expense.created_at)
        return expense

    def to_dict(self):
        return {
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "created_at": self.created_at
        }

    def validate(self):
        validate_date(self.date)
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        validate_amount(str(self.amount))
        cat = validate_category(self.category)
        if cat is None:
            raise ValueError(f"Invalid category. Choose from: {', '.join(CATEGORIES)}")
        self.category = cat
        if not self.description or not self.description.strip():
            raise ValueError("Description cannot be empty")
        self.description = self.description.strip()
        if len(self.description) > 200:
            raise ValueError("Description too long (max 200 characters)")
        return True

    def __str__(self):
        from .utils import format_currency
        return f"{self.date} | {self.category:<12} | {format_currency(self.amount):>10} | {self.description}"

    def __repr__(self):
        return f"Expense(date='{self.date}', amount={self.amount}, category='{self.category}')"
