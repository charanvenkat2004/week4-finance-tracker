# Personal Finance Tracker

A comprehensive personal finance tracking application built with Python. Track expenses, set budgets, generate reports, and export data — all from the command line.

## Features

- **Add/Edit/Delete Expenses** — Full CRUD with validation
- **Categorization** — 8 preset categories (Food, Transport, Entertainment, Bills, Shopping, Healthcare, Education, Other)
- **JSON Persistence** — Auto-saves after every change
- **Automatic Backups** — Timestamped backups on every save, keeps last 20
- **Backup/Restore** — Manual backup creation and restoration from any backup point
- **Monthly Reports** — Per-month summaries with category breakdowns and budget alerts
- **Category Breakdown** — Visual bar charts showing spending distribution
- **Trend Analysis** — Month-over-month spending trends with indicators
- **Budget Tracking** — Per-category budgets with real-time percentage tracking
- **CSV Export/Import** — Export all or filtered data, import from external CSV
- **Search & Filter** — Search by description, category, date, or amount
- **Statistics** — Total count, min/max/median/average expense, busiest month
- **Error Recovery** — Corrupted data file auto-recovers from latest backup

## Project Structure

```
week4-finance-tracker/
│── finance_tracker/         # Main package
│   ├── __init__.py         # Package marker
│   ├── main.py             # FinanceTracker class + menu system
│   ├── expense.py          # Expense dataclass
│   ├── expense_manager.py  # ExpenseManager (CRUD, search, budgets)
│   ├── file_handler.py     # JSON/CSV I/O, backups, recovery
│   ├── reports.py          # Reports, visualizations, statistics
│   └── utils.py            # Validation, ANSI colors, helpers
│── data/                   # Data directory
│   ├── expenses.json       # Primary data store (auto-created)
│   ├── backup/             # Timestamped backups (auto-created)
│   └── exports/            # CSV exports (auto-created)
│── tests/                  # Unit tests
│   ├── __init__.py
│   ├── test_expense.py     # 25+ tests for Expense + ExpenseManager
│   ├── test_file_handler.py# 10+ tests for file operations
│   └── test_reports.py     # 12+ tests for report generation
│── run.py                  # Entry point
│── requirements.txt        # No external dependencies
│── .gitignore              # Python + project-specific ignores
└── README.md               # This file
```

## How to Run

```bash
cd week4-finance-tracker
python run.py
```

## How to Run Tests

```bash
cd week4-finance-tracker
python -m unittest discover tests -v
```

## Usage Guide

### Main Menu Options

| Option | Description |
|--------|-------------|
| 1 | Add New Expense — enter date, amount, category, description |
| 2 | View All Expenses — sortable list with totals |
| 3 | Search Expenses — keyword search across all fields |
| 4 | Monthly Report — pick year/month, see full breakdown |
| 5 | Category Breakdown — visual bar chart + budget status |
| 6 | Set/Update Budget — per-category or all at once |
| 7 | Export/Import CSV — export all or filtered, import external data |
| 8 | Statistics — trend analysis + expense statistics |
| 9 | Backup/Restore — create, list, and restore backups |
| 10 | Edit/Delete — modify individual expenses or clear all |
| 0 | Exit — auto-saves data |

### Data Storage

Data is stored in `data/expenses.json` as:

```json
{
  "expenses": [
    {
      "date": "2026-07-07",
      "amount": 25.50,
      "category": "Food",
      "description": "Lunch",
      "created_at": "2026-07-07T12:00:00"
    }
  ],
  "budgets": {
    "Food": 500.0,
    "Transport": 200.0
  },
  "last_updated": "2026-07-07T12:00:00"
}
```

### Requirements

- Python 3.8+
- No external dependencies (uses standard library only)

## Technical Details

- **Architecture**: Modular OOP with 6 modules + entry point
- **Data Flow**: Input validation → Expense objects → ExpenseManager → JSON persistence with auto-backup
- **Error Handling**: Comprehensive try/except for file I/O (FileNotFoundError, PermissionError, json.JSONDecodeError), input validation with while loops, corrupted data recovery
- **Testing**: 47+ unittest tests across 3 test files
