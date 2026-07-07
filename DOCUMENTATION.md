# Documentation Requirements
## Complete guidelines for your project submission

# Personal Finance Tracker

## Project Description
A comprehensive personal finance tracking application that helps users manage their expenses, categorize spending, set budgets, and generate insightful reports. Built with modular architecture, JSON persistence, automatic backups, and CSV export/import capabilities.

## What I Learned
- **File Operations**: Reading/writing JSON and CSV files for data persistence
- **Modular Design**: Organizing code into 6+ modules with clear responsibilities
- **Object-Oriented Programming**: Using classes (Expense, ExpenseManager, FinanceTracker)
- **Error Handling**: Comprehensive try/except for file I/O, validation, and recovery
- **Data Visualization**: Text-based bar charts and trend analysis with ANSI colors
- **Context Managers**: Using `with open()` for proper resource management
- **Testing**: Writing unittest test suites for validation, file ops, and reports

## Features
- ✓ Add, edit, and delete expenses with full validation (date, amount, category, description)
- ✓ 8 preset categories: Food, Transport, Entertainment, Bills, Shopping, Healthcare, Education, Other
- ✓ JSON data persistence with auto-save after every change
- ✓ Automatic timestamped backups (keeps last 20) with manual restore
- ✓ Corrupted data file auto-recovery from latest backup
- ✓ Monthly expense reports with category breakdowns and budget alerts
- ✓ Category-wise spending breakdown with visual bar charts
- ✓ Month-over-month expense trend analysis with direction indicators
- ✓ Per-category budget setting with real-time spending tracking
- ✓ CSV export (all or filtered) and CSV import
- ✓ Search across description, category, date, and amount
- ✓ Comprehensive statistics (min/max/median/average, busiest month)
- ✓ Graceful KeyboardInterrupt handling with data save

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

## Code Structure

```
week4-finance-tracker/
│── finance_tracker/             # Main package (6 modules)
│   ├── __init__.py             # Package marker
│   ├── main.py                 # FinanceTracker class + 10-option menu system
│   ├── expense.py              # Expense dataclass (to_dict, from_dict, validate)
│   ├── expense_manager.py      # CRUD, search, filter, budgets, statistics
│   ├── file_handler.py         # JSON/CSV I/O, backup/restore, recovery
│   ├── reports.py              # Monthly reports, bar charts, trend analysis
│   └── utils.py                # ANSI colors, validation, display helpers
│── data/                       # Auto-created data directory
│   ├── expenses.json           # Primary data store (auto-created on first save)
│   ├── backup/                 # Timestamped backups (auto-created)
│   └── exports/                # CSV exports (auto-created)
│── tests/                      # Unit test suite
│   ├── __init__.py
│   ├── test_expense.py         # 34 tests: Expense + ExpenseManager
│   ├── test_file_handler.py    # 8 tests: save/load/backup/CSV
│   └── test_reports.py         # 13 tests: report generation
│── run.py                      # Entry point
│── requirements.txt            # No external dependencies
│── .gitignore                  # Python + project-specific ignores
├── README.md                   # Quick-start documentation
└── DOCUMENTATION.md            # Complete submission documentation
```

### Program Flow
1. On startup, `run.py` imports and calls `main()` from `finance_tracker.main`
2. `FinanceTracker.__init__()` loads data from `data/expenses.json` via `file_handler`
3. Data is converted to `Expense` objects and stored in `ExpenseManager`
4. Main menu loop displays 10 options and delegates to handler methods
5. Every mutation (add/edit/delete) triggers `save_data()` → JSON dump + auto-backup
6. Reports are generated on-demand from in-memory data
7. On exit, data is auto-saved; KeyboardInterrupt is caught and saves gracefully

## Visual Documentation

### Main Menu
```
============================================================
          PERSONAL FINANCE TRACKER
============================================================
Track your expenses, set budgets, and generate reports

==================================================
                    MAIN MENU
==================================================
  1.  Add New Expense
  2.  View All Expenses
  3.  Search Expenses
  4.  Generate Monthly Report
  5.  View Category Breakdown
  6.  Set/Update Budget
  7.  Export Data to CSV
  8.  View Statistics
  9.  Backup/Restore Data
  10. Edit/Delete Expenses
  0.  Exit
--------------------------------------------------
Enter your choice (0-10): 1
```

### Adding an Expense
```
--- ADD NEW EXPENSE ---

Enter date (YYYY-MM-DD) or Enter for today: 2026-07-07
Enter amount: 25.50

--- CATEGORIES ---
  1. Food
  2. Transport
  3. Entertainment
  4. Bills
  5. Shopping
  6. Healthcare
  7. Education
  8. Other

Select category (1-8): 1
Enter description: Lunch at restaurant
Expense added: $25.50 for Food
```

### Viewing All Expenses
```
--- ALL EXPENSES ---

  Total Entries: 3
  Total Spent:   $85.50

  #    Date         Category       Amount     Description
  ---------------------------------------------------------------
  1    2026-07-07   Food             $25.50   Lunch at restaurant
  2    2026-07-08   Transport        $10.00   Bus fare
  3    2026-07-09   Entertainment    $50.00   Movie tickets
```

### Monthly Report
```
============================================================
              MONTHLY REPORT - July 2026
============================================================

  Total Expenses:  3
  Total Spent:     $85.50
  Average:         $28.50

  Category Breakdown:
    Entertainment    $50.00  (58.5%)
    Food             $25.50  (29.8%)
    Transport        $10.00  (11.7%)

  Transactions:
     1. 2026-07-07 | Food         |    $25.50 | Lunch at restaurant
     2. 2026-07-08 | Transport    |    $10.00 | Bus fare
     3. 2026-07-09 | Entertainment|    $50.00 | Movie tickets
------------------------------------------------------------
```

### Category Breakdown with Bar Chart
```
============================================================
                  CATEGORY BREAKDOWN
============================================================

  Total Spent: $85.50

  Category       Amount        %      Bar
  ----------------------------------------------------------
  Entertainment  $50.00     58.5%   ████████████████████████████
  Food           $25.50     29.8%   ███████████████
  Transport      $10.00     11.7%   ██████

  Categories with no spending: Bills, Shopping, Healthcare, Education, Other
------------------------------------------------------------
```

### Trend Analysis
```
============================================================
              EXPENSE TREND ANALYSIS
============================================================

  Overall Trend: ↓ Decreasing
  Average Monthly Change: -13.0%
  Highest Spending:  2026-07 ($115.00)
  Lowest Spending:   2026-08 ($100.00)

  Monthly Spending:
  Month          Amount   Change  Bar
  -------------------------------------------------------
  2026-07      $115.00      N/A  ██████████████████████████████
  2026-08      $100.00  -13.0%  ███████████████████████████
------------------------------------------------------------
```

### Budget Status
```
============================================================
                    BUDGET STATUS
============================================================

  Category       Budget      Spent     Remain      Used
  ----------------------------------------------------------
  Food           $500.00    $55.00   $445.00    11.0%
  Transport      $200.00    $10.00   $190.00     5.0%
  Entertainment  $100.00    $50.00    $50.00    50.0%
  ----------------------------------------------------------
  TOTAL          $800.00   $115.00   $685.00    14.4%
------------------------------------------------------------
```

### Input Validation
```
Enter amount: -50
Invalid amount. Amount must be positive
Enter amount: abc
Invalid amount. Please enter a valid number
Enter amount: 25.50

Enter date (YYYY-MM-DD) or Enter for today: 13-32-2026
Invalid date format. Use YYYY-MM-DD
Enter date (YYYY-MM-DD) or Enter for today: 2026-07-07
```

## Technical Details

### Algorithms
1. **Input Validation**: `while True` loops with `try/except ValueError` — re-prompts until valid input is received; `.strip()` for whitespace handling
2. **Expense CRUD**: List-based storage with index access for edit/delete; linear search with case-insensitive matching across all fields
3. **Category Breakdown**: Iterates through expenses, aggregates `amount` by `category` into a dictionary, then sorts by value descending
4. **Monthly Summary**: Filters expenses by `YYYY-MM` prefix on date, computes total, count, average, and category breakdown
5. **Trend Analysis**: Groups expenses by month, computes month-over-month percentage change, identifies highest/lowest spending months, renders text-based bar chart scaled to max value
6. **Statistics**: Sort all amounts for median calculation; `max()`, `min()`, `sum()` / `len()` for average; frequency counting for most common category and busiest month
7. **Budget Tracking**: Per-category budget stored in dictionary; `get_budget_status()` computes spent vs budget percentage from in-memory expenses
8. **Backup Recovery**: On `json.JSONDecodeError`, sorts backup files by timestamp descending and loads from newest; `shutil.copy2()` for restore
9. **Auto-backup**: On every `save_data()`, copies current `expenses.json` to `data/backup/expenses_backup_{timestamp}.json`; cleans up oldest backups when count exceeds 20

### Data Structures
| Structure | Location | Purpose |
|-----------|----------|---------|
| `Expense` class | `expense.py` | Dataclass with date, amount, category, description, created_at |
| `list[Expense]` (`_expenses`) | `expense_manager.py` | In-memory store of all expense objects |
| `dict[str, float]` (`_budgets`) | `expense_manager.py` | Maps category names to budget amounts |
| `dict` (JSON structure) | `file_handler.py` / `expenses.json` | `{"expenses": [...], "budgets": {...}, "last_updated": "..."}` |
| `dict` (statistics) | `expense_manager.py` | Returned by `get_statistics()` with 8 computed fields |
| `list[dict]` (CSV rows) | `file_handler.py` | List of expense dicts for CSV export/import |

### Architecture

**Layered Design:**
```
┌─────────────────────────────────────────────────────────┐
│                   Presentation Layer                     │
│              main.py (FinanceTracker class)               │
│            Menu display, user interaction                 │
├─────────────────────────────────────────────────────────┤
│                   Business Logic Layer                    │
│      expense.py  +  expense_manager.py +  reports.py      │
│    Expense objects, CRUD, search, budgets, reports       │
├─────────────────────────────────────────────────────────┤
│                Persistence Layer                          │
│              file_handler.py                              │
│        JSON save/load, backup/restore, CSV I/O           │
├─────────────────────────────────────────────────────────┤
│                Utility Layer                              │
│              utils.py                                    │
│     Validation, ANSI colors, display helpers            │
└─────────────────────────────────────────────────────────┘
```

### Module Functions / Classes

| Module | Class/Function | Purpose |
|--------|---------------|---------|
| `expense.py` | `Expense.__init__()` | Create Expense with date, amount, category, description |
| `expense.py` | `Expense.to_dict()` | Serialize Expense to dict for JSON |
| `expense.py` | `Expense.from_dict()` | Deserialize dict to Expense |
| `expense.py` | `Expense.validate()` | Validate all fields, raise ValueError |
| `expense_manager.py` | `ExpenseManager.add_expense()` | Add validated expense to list |
| `expense_manager.py` | `ExpenseManager.remove_expense()` | Remove expense by index |
| `expense_manager.py` | `ExpenseManager.edit_expense()` | Update expense fields by index |
| `expense_manager.py` | `ExpenseManager.search_expenses()` | Case-insensitive search across fields |
| `expense_manager.py` | `ExpenseManager.filter_by_category()` | Filter expenses by category |
| `expense_manager.py` | `ExpenseManager.filter_by_date_range()` | Filter expenses between dates |
| `expense_manager.py` | `ExpenseManager.get_monthly_summary()` | Compute total/count/avg/breakdown for month |
| `expense_manager.py` | `ExpenseManager.get_category_breakdown()` | Aggregate amounts by category |
| `expense_manager.py` | `ExpenseManager.get_statistics()` | Compute 8 statistical measures |
| `expense_manager.py` | `ExpenseManager.set_budget()` | Set budget for a category |
| `expense_manager.py` | `ExpenseManager.get_budget_status()` | Get budget spent/remaining/percentage |
| `file_handler.py` | `save_expenses()` | Write JSON + create backup |
| `file_handler.py` | `load_expenses()` | Read JSON with auto-recovery |
| `file_handler.py` | `create_backup()` | Timestamped backup copy |
| `file_handler.py` | `restore_from_backup()` | Restore data from backup file |
| `file_handler.py` | `list_backups()` | List available backups with timestamps |
| `file_handler.py` | `export_to_csv()` | Write expenses to CSV file |
| `file_handler.py` | `import_from_csv()` | Read expenses from CSV file |
| `reports.py` | `generate_monthly_report()` | Formatted monthly report string |
| `reports.py` | `generate_category_breakdown()` | Category breakdown with bar chart |
| `reports.py` | `generate_trend_analysis()` | Month-over-month trend with viz |
| `reports.py` | `generate_statistics_report()` | Statistical overview |
| `reports.py` | `generate_budget_report()` | Budget status table |
| `utils.py` | `validate_amount()` | Positive number check |
| `utils.py` | `validate_date()` | YYYY-MM-DD format check |
| `utils.py` | `validate_category()` | Valid category check |
| `utils.py` | `validate_description()` | Non-empty, max 200 chars |
| `utils.py` | `format_currency()` | Format as $X,XXX.XX |
| `main.py` | `FinanceTracker.__init__()` | Load data, initialize manager |
| `main.py` | `FinanceTracker.run()` | Main menu loop |
| `main.py` | `FinanceTracker.add_expense()` | Add expense workflow |
| `main.py` | `FinanceTracker.view_expenses()` | Display all expenses |
| `main.py` | `FinanceTracker.search_expenses()` | Search workflow |
| `main.py` | `FinanceTracker.generate_monthly_report()` | Report workflow |
| `main.py` | `FinanceTracker.view_category_breakdown()` | Category visualization |
| `main.py` | `FinanceTracker.set_budget()` | Budget management workflow |
| `main.py` | `FinanceTracker.export_data()` | CSV export/import |
| `main.py` | `FinanceTracker.view_statistics()` | Statistics display |
| `main.py` | `FinanceTracker.backup_restore()` | Backup management |
| `main.py` | `FinanceTracker.edit_delete_expense()` | Edit/delete workflow |

## Testing Evidence

### Test Results
```
Ran 55 tests in 0.040s
OK
```

### Test Case Details

**test_expense.py (34 tests)**

| Test Case | Expected | Actual |
|-----------|----------|--------|
| Create expense with valid data | All fields match | Pass |
| Expense to_dict() roundtrip | Dict with all keys | Pass |
| Expense from_dict() | Restored object matches | Pass |
| Expense to_dict → from_dict roundtrip | Original == restored | Pass |
| Valid expense passes validation | True | Pass |
| Negative amount raises ValueError | ValueError raised | Pass |
| Zero amount raises ValueError | ValueError raised | Pass |
| Invalid date raises ValueError | ValueError raised | Pass |
| Invalid category raises ValueError | ValueError raised | Pass |
| Empty description raises ValueError | ValueError raised | Pass |
| Description >200 chars raises ValueError | ValueError raised | Pass |
| __str__() contains date, category, amount | String has all fields | Pass |
| Add expense to manager | Count = 1 | Pass |
| Add non-Expense type raises TypeError | TypeError raised | Pass |
| Remove expense by index | Count = 0, removed matches | Pass |
| Remove out-of-range index | None returned | Pass |
| Get expense by index | Object returned | Pass |
| Edit expense amount and description | Fields updated | Pass |
| Search by keyword | Correct results | Pass |
| Filter by category | Only matching category | Pass |
| Filter by date range | Expenses in range | Pass |
| Total spent computed | Sum matches | Pass |
| Empty total spent | 0 | Pass |
| Category breakdown | Correct per-category sums | Pass |
| Monthly summary count/total/average | Correct values | Pass |
| Empty monthly summary | 0 count, 0 total | Pass |
| Set and get budget | Budget matches | Pass |
| Negative budget raises error | ValueError raised | Pass |
| Budget status (budget/spent/remaining/%) | Correct percentages | Pass |
| Statistics with 3 expenses | 3 expenses, total correct | Pass |
| Statistics empty | 0 expenses | Pass |
| Clear all expenses | Count = 0 | Pass |
| Sorted by date | Earliest first | Pass |
| Get all budgets | Dict with 2 entries | Pass |

**test_file_handler.py (8 tests)**

| Test Case | Expected | Actual |
|-----------|----------|--------|
| Save and load expenses | 1 expense, budget $500 | Pass |
| Load with no file | Empty lists | Pass |
| Corrupted JSON file recovery | Empty fallback | Pass |
| Create backup on save | Backup file created | Pass |
| List backups when empty | Empty list | Pass |
| Export to CSV | File exists, has headers + data | Pass |
| Export empty list | File created | Pass |
| Import from CSV | 1 expense, description matches | Pass |
| Import nonexistent CSV | FileNotFoundError | Pass |

**test_reports.py (13 tests)**

| Test Case | Expected | Actual |
|-----------|----------|--------|
| Monthly report July 2026 | Contains month name, total, count | Pass |
| Monthly report empty month | Report generated | Pass |
| Category breakdown with data | All categories present | Pass |
| Category breakdown empty | "No expenses" message | Pass |
| Trend analysis with 2 months | Both months in output | Pass |
| Trend analysis empty | "No expenses" message | Pass |
| Statistics with 5 expenses | Count=5, total=$215 | Pass |
| Statistics empty | "No expenses" message | Pass |
| Budget report with budget set | Category + amounts shown | Pass |
| Budget report no budgets | "No budgets set" | Pass |
| Monthly report with budget alert | "Budget Alerts" shown | Pass |
| Category breakdown with budgets | "Budget" in output | Pass |

### Edge Cases Covered
- **Empty data file** (first run): Returns empty lists gracefully
- **Corrupted JSON file**: Auto-recovers from latest backup
- **No backups available for recovery**: Returns empty data safely
- **Permission denied on file write**: Caught by IOError handler, user notified
- **CSV with missing fields**: Gracefully defaults empty values
- **KeyboardInterrupt during input**: Caught, data saved before exit
- **Negative/zero amounts**: Rejected by validator with clear message
- **Incorrect date format (DD-MM-YYYY)**: Rejected, format hint provided
- **Empty/whitespace descriptions**: Rejected by description validator
- **Non-existent backup restore**: FileNotFoundError caught, user notified

## Challenges & Solutions
- **Challenge**: Corrupted JSON file breaks data loading
  - **Solution**: Added `attempt_recovery()` that finds the latest backup and loads from it; if no backup exists, returns empty data gracefully

- **Challenge**: Data loss risk when saving
  - **Solution**: Backup is created *before* the new save completes; on every save, `create_backup()` runs via `shutil.copy2()`; corrupted files are recovered from newest backup

- **Challenge**: ANSI colors don't render in some terminals (Windows cmd)
  - **Solution**: Colors still function without errors; Windows Terminal, VS Code terminal, and PowerShell all support ANSI; user sees plain text without colors in unsupported terminals

- **Challenge**: Month-over-month trend needs at least 2 data points
  - **Solution**: Single-month data shows no trend direction; the code checks `len(sorted_months) >= 2` before computing percentages

- **Challenge**: CSV import with varying column order
  - **Solution**: Uses `csv.DictReader` which reads by header name, not column position; fields are accessed with `.get()` for missing columns

- **Challenge**: User might accidentally delete all expenses
  - **Solution**: Added `confirm_action()` before `clear_all_expenses()`; backups exist so data can be restored

- **Challenge**: Budget alerts remain visible after spending
  - **Solution**: Budget status is computed fresh from `_expenses` on each report render; no caching of budget status

- **Challenge**: Long-running sessions with no auto-save
  - **Solution**: Every mutation (add, edit, delete, budget set) triggers `save_data()` immediately; exit also saves

## Quality Standards Checklist

### Project Overview
Clear description of project goals and objectives.
The Personal Finance Tracker manages expenses with full CRUD, 8 categories, JSON persistence with automatic timestamped backups, per-category budgets, monthly reports with visual bar charts, trend analysis, CSV export/import, and comprehensive error handling. Built with a 6-module OOP architecture and 55 passing unit tests.

### Setup Instructions
Step-by-step installation and configuration guide.

**Prerequisites:**
- Python 3.8+ installed on your system

**Steps:**
1. Clone the repository: `git clone https://github.com/charanvenkat2004/week4-finance-tracker.git`
2. Navigate: `cd week4-finance-tracker`
3. Run: `python run.py`
4. Follow the on-screen menu to manage expenses
5. Run tests: `python -m unittest discover tests -v`

### Code Structure
Well-organized code with clear file hierarchy. See the tree diagram in the Code Structure section above. All modules have single responsibilities: `expense.py` (data model), `expense_manager.py` (business logic), `file_handler.py` (persistence), `reports.py` (presentation), `utils.py` (shared utilities), `main.py` (orchestration).

### Visual Documentation
Screenshots demonstrating functionality. See the Visual Documentation section above with 7 annotated terminal output examples covering the main menu, adding expenses, viewing expenses, monthly reports, category breakdown, trend analysis, budget status, and input validation.

### Technical Details
Explanation of algorithms, data structures, and architecture. See the Technical Details section covering 9 algorithms (validation, CRUD, breakdown, summary, trend, statistics, budget, recovery, auto-backup), 6 data structures with locations and purposes, a layered architecture diagram, and a complete function/class table with all 40+ methods.

### Testing Evidence
Examples of test cases and validation. All 55 tests pass across 3 test files with detailed test case tables covering validation, CRUD, file operations, CSV I/O, backup/recovery, report generation, budget tracking, statistics, and edge cases.
