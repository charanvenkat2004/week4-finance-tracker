import sys
from datetime import datetime

from .expense import Expense
from .expense_manager import ExpenseManager
from . import file_handler
from . import reports
from .utils import (
    Colors, CATEGORIES, format_currency,
    print_header, print_subheader, print_success,
    print_error, print_warning, print_info,
    get_valid_input, get_valid_amount, get_valid_date,
    validate_amount, validate_date, validate_category,
    validate_description, select_category,
    confirm_action, clear_screen
)


class FinanceTracker:
    def __init__(self):
        self.manager = ExpenseManager()
        self.load_data()

    def load_data(self):
        try:
            expenses_dict, budgets = file_handler.load_expenses()
            expenses = [Expense.from_dict(ed) for ed in expenses_dict]
            self.manager.expenses = expenses
            for cat, amt in budgets.items():
                self.manager.set_budget(cat, amt)
        except IOError as e:
            print_warning(f"Could not load saved data: {e}")
            print_info("Starting with empty data.")

    def save_data(self):
        try:
            expenses_dict = [exp.to_dict() for exp in self.manager._expenses]
            budgets = self.manager.get_all_budgets()
            file_handler.save_expenses(expenses_dict, budgets)
        except IOError as e:
            print_error(f"Error saving data: {e}")
            return False
        return True

    def run(self):
        print_header("PERSONAL FINANCE TRACKER")
        print(f"{Colors.BOLD}Track your expenses, set budgets, and generate reports{Colors.RESET}")
        while True:
            choice = self.display_menu()
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.search_expenses()
            elif choice == '4':
                self.generate_monthly_report()
            elif choice == '5':
                self.view_category_breakdown()
            elif choice == '6':
                self.set_budget()
            elif choice == '7':
                self.export_data()
            elif choice == '8':
                self.view_statistics()
            elif choice == '9':
                self.backup_restore()
            elif choice == '10':
                self.edit_delete_expense()
            elif choice == '0':
                self.exit_app()
                break

    def display_menu(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 50}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'MAIN MENU':^50}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 50}{Colors.RESET}")
        print(f"  {Colors.BOLD}1.{Colors.RESET}  Add New Expense")
        print(f"  {Colors.BOLD}2.{Colors.RESET}  View All Expenses")
        print(f"  {Colors.BOLD}3.{Colors.RESET}  Search Expenses")
        print(f"  {Colors.BOLD}4.{Colors.RESET}  Generate Monthly Report")
        print(f"  {Colors.BOLD}5.{Colors.RESET}  View Category Breakdown")
        print(f"  {Colors.BOLD}6.{Colors.RESET}  Set/Update Budget")
        print(f"  {Colors.BOLD}7.{Colors.RESET}  Export Data to CSV")
        print(f"  {Colors.BOLD}8.{Colors.RESET}  View Statistics")
        print(f"  {Colors.BOLD}9.{Colors.RESET}  Backup/Restore Data")
        print(f"  {Colors.BOLD}10.{Colors.RESET} Edit/Delete Expenses")
        print(f"  {Colors.BOLD}0.{Colors.RESET}  Exit")
        print(f"{Colors.CYAN}{'-' * 50}{Colors.RESET}")
        return get_valid_input("Enter your choice (0-10): ")

    def add_expense(self):
        print_header("ADD NEW EXPENSE")
        try:
            date = get_valid_date()
            amount = get_valid_amount()
            category = select_category()
            description = get_valid_input("Enter description: ", validate_description)
            expense = Expense(date, amount, category, description)
            self.manager.add_expense(expense)
            if self.save_data():
                print_success(f"Expense added: {format_currency(amount)} for {category}")
                status = self.manager.get_budget_status(category)
                if status["budget"] > 0 and status["percentage"] > 80:
                    remaining = status["budget"] - status["spent"]
                    print_warning(f"⚠ Budget alert: {category} is at {status['percentage']:.0f}% "
                                  f"({format_currency(remaining)} remaining)")
        except (ValueError, TypeError) as e:
            print_error(f"Error: {e}")

    def view_expenses(self):
        expenses = self.manager.expenses
        print_header("ALL EXPENSES")
        if not expenses:
            print_info("No expenses recorded yet.")
            return
        total = self.manager.get_total_spent()
        print(f"\n  {Colors.BOLD}Total Entries:{Colors.RESET} {len(expenses)}")
        print(f"  {Colors.BOLD}Total Spent:{Colors.RESET}   {format_currency(total)}")
        print(f"\n  {'#':<4} {'Date':<12} {'Category':<15} {'Amount':>10}  {'Description'}")
        print(f"  {'-' * 65}")
        for i, exp in enumerate(sorted(expenses, key=lambda e: e.date), 1):
            print(f"  {i:<4} {exp.date:<12} {exp.category:<15} {format_currency(exp.amount):>10}  {exp.description}")

    def search_expenses(self):
        print_header("SEARCH EXPENSES")
        print(f"  Search by: description, category, date, or amount\n")
        query = get_valid_input("Enter search term: ")
        results = self.manager.search_expenses(query)
        if not results:
            print_warning(f"No expenses found matching '{query}'")
            return
        print(f"\n  {Colors.BOLD}Found {len(results)} result(s):{Colors.RESET}")
        total = self.manager.get_total_spent(results)
        print(f"\n  {'#':<4} {'Date':<12} {'Category':<15} {'Amount':>10}  {'Description'}")
        print(f"  {'-' * 65}")
        for i, exp in enumerate(results, 1):
            print(f"  {i:<4} {exp.date:<12} {exp.category:<15} {format_currency(exp.amount):>10}  {exp.description}")
        print(f"\n  {Colors.BOLD}Subtotal: {format_currency(total)}{Colors.RESET}")

    def generate_monthly_report(self):
        print_header("MONTHLY REPORT")
        try:
            year_str = get_valid_input("Enter year (e.g., 2026): ")
            year = int(year_str)
            month_str = get_valid_input("Enter month (1-12): ")
            month = int(month_str)
            if month < 1 or month > 12:
                print_error("Month must be between 1 and 12")
                return
            report = reports.generate_monthly_report(self.manager, year, month)
            print(report)
        except ValueError:
            print_error("Invalid input. Please enter numbers only.")

    def view_category_breakdown(self):
        breakdown = reports.generate_category_breakdown(self.manager)
        print(breakdown)

    def set_budget(self):
        print_header("SET/UPDATE BUDGET")
        current = self.manager.get_all_budgets()
        if current:
            print(f"\n  {Colors.BOLD}Current Budgets:{Colors.RESET}")
            for cat, amt in sorted(current.items()):
                status = self.manager.get_budget_status(cat)
                print(f"    {cat:<15} {format_currency(amt):>10}  ({Colors.GREEN if status['percentage'] < 80 else Colors.YELLOW}{'✓' if status['spent'] <= amt else '⚠'}{Colors.RESET} used: {format_currency(status['spent'])})")
        print(f"\n  {Colors.BOLD}Select a category to set budget:{Colors.RESET}")
        for i, cat in enumerate(CATEGORIES, 1):
            current_budget = self.manager.get_budget(cat)
            current_str = f" ({format_currency(current_budget)})" if current_budget > 0 else ""
            print(f"  {i}. {cat}{current_str}")
        print(f"  {len(CATEGORIES) + 1}. Set all categories")
        print(f"  0. Cancel")
        try:
            choice = int(get_valid_input("\nChoice: "))
            if choice == 0:
                return
            elif choice == len(CATEGORIES) + 1:
                for cat in CATEGORIES:
                    amount_str = get_valid_input(f"  Budget for {cat} (Enter = skip): ", allow_empty=True)
                    if amount_str:
                        try:
                            amount = validate_amount(amount_str)
                            self.manager.set_budget(cat, amount)
                            print_success(f"  {cat}: {format_currency(amount)}")
                        except ValueError as e:
                            print_error(f"  {cat}: {e}")
            elif 1 <= choice <= len(CATEGORIES):
                cat = CATEGORIES[choice - 1]
                current_budget = self.manager.get_budget(cat)
                print(f"  Setting budget for {Colors.BOLD}{cat}{Colors.RESET}")
                print(f"  Current: {format_currency(current_budget) if current_budget > 0 else 'Not set'}")
                amount = get_valid_amount("  Budget amount: $")
                self.manager.set_budget(cat, amount)
                if self.save_data():
                    print_success(f"Budget for {cat} set to {format_currency(amount)}")
            else:
                print_error("Invalid choice")
        except ValueError:
            print_error("Invalid input")

    def export_data(self):
        print_header("EXPORT DATA")
        print(f"  1. Export all expenses to CSV")
        print(f"  2. Export filtered expenses to CSV")
        print(f"  3. Import expenses from CSV")
        print(f"  0. Cancel")
        choice = get_valid_input("\nChoice: ")
        if choice == '0':
            return
        elif choice == '1':
            try:
                expenses_dict = [exp.to_dict() for exp in self.manager._expenses]
                if not expenses_dict:
                    print_warning("No expenses to export.")
                    return
                filename = file_handler.export_to_csv(expenses_dict)
                print_success(f"Exported {len(expenses_dict)} expenses to: {filename}")
            except (IOError, ValueError) as e:
                print_error(f"Export failed: {e}")
        elif choice == '2':
            print(f"\n  Filter options:")
            print(f"  1. By category")
            cat_choice = get_valid_input("  Choice: ")
            if cat_choice == '1':
                cat = select_category()
                filtered = self.manager.filter_by_category(cat)
            else:
                filtered = self.manager.expenses
            if not filtered:
                print_warning("No expenses match the filter.")
                return
            try:
                expenses_dict = [exp.to_dict() for exp in filtered]
                filename = file_handler.export_to_csv(expenses_dict)
                print_success(f"Exported {len(expenses_dict)} expenses to: {filename}")
            except (IOError, ValueError) as e:
                print_error(f"Export failed: {e}")
        elif choice == '3':
            path = get_valid_input("Enter CSV file path: ")
            try:
                imported = file_handler.import_from_csv(path)
                count = 0
                for ed in imported:
                    try:
                        expense = Expense.from_dict(ed)
                        self.manager.add_expense(expense)
                        count += 1
                    except (ValueError, TypeError):
                        print_warning(f"Skipped invalid entry: {ed}")
                if count > 0 and self.save_data():
                    print_success(f"Imported {count} expense(s) from CSV.")
            except (FileNotFoundError, IOError, ValueError) as e:
                print_error(f"Import failed: {e}")

    def view_statistics(self):
        trend = reports.generate_trend_analysis(self.manager)
        print(trend)
        stats = reports.generate_statistics_report(self.manager)
        print(stats)

    def backup_restore(self):
        print_header("BACKUP / RESTORE")
        print(f"  1. Create manual backup")
        print(f"  2. List backups")
        print(f"  3. Restore from backup")
        print(f"  0. Cancel")
        choice = get_valid_input("\nChoice: ")
        if choice == '0':
            return
        elif choice == '1':
            if file_handler.create_backup():
                print_success("Manual backup created successfully.")
            else:
                print_error("Backup failed.")
        elif choice == '2':
            backups = file_handler.list_backups()
            if not backups:
                print_warning("No backups found.")
                return
            print(f"\n  {Colors.BOLD}Available Backups:{Colors.RESET}")
            print(f"  {'#':<3} {'Timestamp':<22} {'Size':>10}")
            print(f"  {'-' * 40}")
            for i, b in enumerate(backups, 1):
                size_str = f"{b['size'] / 1024:.1f} KB" if b['size'] < 1024 * 1024 else f"{b['size'] / (1024 * 1024):.1f} MB"
                print(f"  {i:<3} {b['timestamp']:<22} {size_str:>10}")
        elif choice == '3':
            backups = file_handler.list_backups()
            if not backups:
                print_warning("No backups available to restore.")
                return
            print(f"\n  {Colors.BOLD}Select a backup to restore:{Colors.RESET}")
            for i, b in enumerate(backups, 1):
                print(f"  {i}. {b['timestamp']}")
            try:
                idx = int(get_valid_input("\nBackup number: "))
                if 1 <= idx <= len(backups):
                    if confirm_action("Restore will replace all current data. Continue?"):
                        timestamp = backups[idx - 1]["timestamp"]
                        timestamp_file = backups[idx - 1]["path"].split("expenses_backup_")[-1].replace(".json", "")
                        expenses_dict, budgets = file_handler.restore_from_backup(timestamp_file)
                        expenses = [Expense.from_dict(ed) for ed in expenses_dict]
                        self.manager.expenses = expenses
                        self.manager._budgets = dict(budgets)
                        print_success(f"Restored {len(expenses)} expenses from backup.")
                else:
                    print_error("Invalid backup number.")
            except (ValueError, FileNotFoundError, IOError) as e:
                print_error(f"Restore failed: {e}")

    def edit_delete_expense(self):
        expenses = self.manager.expenses
        if not expenses:
            print_header("EDIT / DELETE EXPENSES")
            print_warning("No expenses to edit or delete.")
            return
        print_header("EDIT / DELETE EXPENSES")
        for i, exp in enumerate(expenses, 1):
            print(f"  {Colors.BOLD}{i:3d}.{Colors.RESET} {exp}")
        print(f"\n  {Colors.BOLD}A.{Colors.RESET}  Delete all expenses")
        print(f"  {Colors.BOLD}0.{Colors.RESET}  Cancel")
        try:
            choice = get_valid_input(f"\nSelect expense to edit (1-{len(expenses)}) or A to delete all: ")
            if choice.lower() == 'a':
                if confirm_action("Delete ALL expenses? This cannot be undone."):
                    self.manager.clear_all_expenses()
                    if self.save_data():
                        print_success("All expenses deleted.")
                return
            idx = int(choice)
            if idx == 0:
                return
            if 1 <= idx <= len(expenses):
                self._edit_single_expense(idx - 1)
            else:
                print_error("Invalid selection.")
        except ValueError:
            print_error("Invalid input.")

    def _edit_single_expense(self, index):
        expense = self.manager.get_expense(index)
        if not expense:
            print_error("Expense not found.")
            return
        print_subheader("EDIT EXPENSE")
        print(f"  Current: {expense}")
        print(f"\n  Leave field empty to keep current value.\n")
        date = get_valid_date(f"  Date [{expense.date}] (YYYY-MM-DD): ")
        if not date:
            date = expense.date
        amount_str = get_valid_input(f"  Amount [{format_currency(expense.amount)}]: ", allow_empty=True)
        amount = expense.amount
        if amount_str:
            try:
                amount = validate_amount(amount_str)
            except ValueError as e:
                print_warning(f"Keeping current amount: {e}")
        print(f"  Current category: {expense.category}")
        change_cat = get_valid_input("  Change category? (y/n): ").lower()
        category = expense.category
        if change_cat in ('y', 'yes'):
            category = select_category()
        desc = get_valid_input(f"  Description [{expense.description}]: ", allow_empty=True)
        if not desc:
            desc = expense.description
        try:
            self.manager.edit_expense(index, date=date, amount=amount, category=category, description=desc)
            if self.save_data():
                print_success("Expense updated successfully.")
        except (ValueError, TypeError) as e:
            print_error(f"Update failed: {e}")

    def exit_app(self):
        if self.save_data():
            print(f"\n{Colors.CYAN}{'=' * 60}{Colors.RESET}")
            print(f"{Colors.BOLD}Thank you for using Personal Finance Tracker!{Colors.RESET}")
            print(f"{Colors.CYAN}{'=' * 60}{Colors.RESET}")
        else:
            print_warning("Data may not have been saved properly.")


def main():
    try:
        tracker = FinanceTracker()
        tracker.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted. Saving data...{Colors.RESET}")
        try:
            tracker.save_data()
            print_success("Data saved.")
        except (NameError, IOError):
            print_error("Could not save data.")
        print(f"\n{Colors.BOLD}Goodbye!{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
