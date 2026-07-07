from datetime import datetime
from collections import defaultdict
from .utils import (
    CATEGORIES, Colors, format_currency, print_header,
    print_subheader, print_info, print_warning
)


def generate_monthly_report(expense_manager, year, month):
    summary = expense_manager.get_monthly_summary(year, month)
    lines = []
    month_name = datetime(year, month, 1).strftime("%B %Y")
    lines.append(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    lines.append(f"{Colors.BOLD}{Colors.CYAN}{f'MONTHLY REPORT - {month_name}':^60}{Colors.RESET}")
    lines.append(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    lines.append(f"\n  Total Expenses:  {Colors.BOLD}{summary['count']}{Colors.RESET}")
    lines.append(f"  Total Spent:     {Colors.BOLD}{format_currency(summary['total'])}{Colors.RESET}")
    if summary['count'] > 0:
        lines.append(f"  Average:         {Colors.BOLD}{format_currency(summary['average'])}{Colors.RESET}")
    if summary['breakdown']:
        lines.append(f"\n  {Colors.BOLD}{Colors.YELLOW}Category Breakdown:{Colors.RESET}")
        for cat, amount in sorted(summary['breakdown'].items(), key=lambda x: x[1], reverse=True):
            pct = (amount / summary['total'] * 100) if summary['total'] > 0 else 0
            lines.append(f"    {cat:<15} {format_currency(amount):>10}  ({pct:5.1f}%)")
    monthly_expenses = expense_manager.get_expenses_by_month(year, month)
    if monthly_expenses:
        lines.append(f"\n  {Colors.BOLD}{Colors.YELLOW}Transactions:{Colors.RESET}")
        sorted_expenses = sorted(monthly_expenses, key=lambda e: e.date)
        for i, exp in enumerate(sorted_expenses, 1):
            lines.append(f"    {i:2d}. {exp}")
    budget_warnings = []
    for cat in CATEGORIES:
        status = expense_manager.get_budget_status(cat)
        if status["budget"] > 0 and status["percentage"] > 80:
            remaining = status["budget"] - status["spent"]
            budget_warnings.append(f"    {Colors.YELLOW}⚠ {cat}: {status['percentage']:.0f}% used ({format_currency(remaining)} remaining){Colors.RESET}")
    if budget_warnings:
        lines.append(f"\n  {Colors.BOLD}{Colors.RED}Budget Alerts:{Colors.RESET}")
        lines.extend(budget_warnings)
    lines.append(f"\n{Colors.CYAN}{'-' * 60}{Colors.RESET}")
    return "\n".join(lines)


def generate_category_breakdown(expense_manager):
    expenses = expense_manager.expenses
    if not expenses:
        return f"\n{Colors.YELLOW}No expenses to display.{Colors.RESET}"
    total = expense_manager.get_total_spent()
    breakdown = expense_manager.get_category_breakdown()
    lines = []
    lines.append(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    lines.append(f"{Colors.BOLD}{Colors.CYAN}{'CATEGORY BREAKDOWN':^60}{Colors.RESET}")
    lines.append(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    lines.append(f"\n  {Colors.BOLD}Total Spent: {format_currency(total)}{Colors.RESET}")
    lines.append("")
    header = f"  {'Category':<15} {'Amount':>10} {'%':>8}  {'Bar'}"
    lines.append(f"  {Colors.BOLD}{header}{Colors.RESET}")
    lines.append(f"  {'-' * 58}")
    sorted_items = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
    for cat, amount in sorted_items:
        pct = (amount / total * 100) if total > 0 else 0
        bar_width = int(pct / 2)
        bar = f"{Colors.BLUE}{'█' * bar_width}{Colors.RESET}" if bar_width > 0 else ""
        lines.append(f"  {cat:<15} {format_currency(amount):>10} {pct:>7.1f}%  {bar}")
    lines.append("")
    lines.append(f"  {'─' * 58}")
    other_cats = [c for c in CATEGORIES if c not in breakdown]
    if other_cats:
        lines.append(f"\n  {Colors.YELLOW}Categories with no spending:{Colors.RESET}")
        lines.append(f"  {', '.join(other_cats)}")
    for cat, amount in sorted_items:
        status = expense_manager.get_budget_status(cat)
        if status["budget"] > 0:
            bar_w = int((status["spent"] / status["budget"] * 100) / 2) if status["budget"] > 0 else 0
            color = Colors.GREEN if status["percentage"] < 80 else (Colors.YELLOW if status["percentage"] < 100 else Colors.RED)
            lines.append(f"\n  {Colors.BOLD}{cat} Budget{Colors.RESET}")
            lines.append(f"  Budget: {format_currency(status['budget'])} | Spent: {format_currency(status['spent'])} | Remaining: {format_currency(status['remaining'])}")
            lines.append(f"  {color}{'█' * min(bar_w, 50)}{Colors.RESET} {status['percentage']:.0f}%")
    lines.append(f"\n{Colors.CYAN}{'-' * 60}{Colors.RESET}")
    return "\n".join(lines)


def generate_trend_analysis(expense_manager):
    expenses = expense_manager.expenses
    if not expenses:
        return f"\n{Colors.YELLOW}No expenses to analyze.{Colors.RESET}"
    monthly_data = defaultdict(float)
    for exp in expenses:
        month_key = exp.date[:7]
        monthly_data[month_key] += exp.amount
    sorted_months = sorted(monthly_data.keys())
    lines = []
    lines.append(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    lines.append(f"{Colors.BOLD}{Colors.CYAN}{'EXPENSE TREND ANALYSIS':^60}{Colors.RESET}")
    lines.append(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    if len(sorted_months) >= 2:
        values = [monthly_data[m] for m in sorted_months]
        changes = []
        for i in range(1, len(values)):
            if values[i - 1] > 0:
                change = ((values[i] - values[i - 1]) / values[i - 1]) * 100
            else:
                change = 0
            changes.append(change)
        avg_change = sum(changes) / len(changes) if changes else 0
        trend = "↑ Increasing" if avg_change > 5 else ("↓ Decreasing" if avg_change < -5 else "→ Stable")
        trend_color = Colors.RED if avg_change > 5 else (Colors.GREEN if avg_change < -5 else Colors.YELLOW)
        lines.append(f"\n  {Colors.BOLD}Overall Trend: {trend_color}{trend}{Colors.RESET}")
        lines.append(f"  Average Monthly Change: {avg_change:+.1f}%")
        highest_month = max(monthly_data, key=monthly_data.get)
        lowest_month = min(monthly_data, key=monthly_data.get)
        lines.append(f"  Highest Spending:  {Colors.RED}{highest_month} ({format_currency(monthly_data[highest_month])}){Colors.RESET}")
        lines.append(f"  Lowest Spending:   {Colors.GREEN}{lowest_month} ({format_currency(monthly_data[lowest_month])}){Colors.RESET}")
    lines.append(f"\n  {Colors.BOLD}{Colors.YELLOW}Monthly Spending:{Colors.RESET}")
    lines.append(f"  {'Month':<10} {'Amount':>10} {'Change':>8}  Bar")
    lines.append(f"  {'-' * 55}")
    max_amount = max(monthly_data.values()) if monthly_data else 1
    for i, month in enumerate(sorted_months):
        amt = monthly_data[month]
        bar_w = int((amt / max_amount) * 30) if max_amount > 0 else 0
        bar = f"{Colors.CYAN}{'█' * bar_w}{Colors.RESET}"
        if i > 0:
            prev = monthly_data[sorted_months[i - 1]]
            chg = ((amt - prev) / prev * 100) if prev > 0 else 0
            chg_str = f"{chg:+.1f}%"
            chg_color = Colors.RED if chg > 0 else (Colors.GREEN if chg < 0 else Colors.YELLOW)
            chg_display = f"{chg_color}{chg_str:>8}{Colors.RESET}"
        else:
            chg_display = f"{'N/A':>8}"
        lines.append(f"  {month:<10} {format_currency(amt):>10} {chg_display}  {bar}")
    lines.append(f"\n{Colors.CYAN}{'-' * 60}{Colors.RESET}")
    return "\n".join(lines)


def generate_statistics_report(expense_manager):
    stats = expense_manager.get_statistics()
    lines = []
    lines.append(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    lines.append(f"{Colors.BOLD}{Colors.CYAN}{'EXPENSE STATISTICS':^60}{Colors.RESET}")
    lines.append(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    if stats["total_expenses"] == 0:
        lines.append(f"\n  {Colors.YELLOW}No expenses recorded yet.{Colors.RESET}")
        lines.append(f"\n{Colors.CYAN}{'-' * 60}{Colors.RESET}")
        return "\n".join(lines)
    lines.append(f"\n  {Colors.BOLD}Overview{Colors.RESET}")
    lines.append(f"  {'Total Expenses:':<25} {stats['total_expenses']}")
    lines.append(f"  {'Total Spent:':<25} {format_currency(stats['total_spent'])}")
    lines.append(f"  {'Average per Expense:':<25} {format_currency(stats['average_per_expense'])}")
    lines.append(f"  {'Smallest Expense:':<25} {format_currency(stats['min_expense'])}")
    lines.append(f"  {'Largest Expense:':<25} {format_currency(stats['max_expense'])}")
    lines.append(f"  {'Median Expense:':<25} {format_currency(stats['median_expense'])}")
    lines.append(f"\n  {Colors.BOLD}Insights{Colors.RESET}")
    lines.append(f"  {'Most Common Category:':<25} {stats['most_common_category']}")
    lines.append(f"  {'Busiest Month:':<25} {stats['busiest_month']}")
    total_budget = sum(expense_manager.get_all_budgets().values())
    if total_budget > 0:
        total_spent = stats["total_spent"]
        pct = (total_spent / total_budget) * 100
        lines.append(f"  {'Total Budget:':<25} {format_currency(total_budget)}")
        lines.append(f"  {'Budget Utilization:':<25} {pct:.1f}%")
    lines.append(f"\n{Colors.CYAN}{'-' * 60}{Colors.RESET}")
    return "\n".join(lines)


def generate_budget_report(expense_manager):
    budgets = expense_manager.get_all_budgets()
    if not budgets:
        return f"\n{Colors.YELLOW}No budgets set. Use option 6 to set budgets.{Colors.RESET}"
    lines = []
    lines.append(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    lines.append(f"{Colors.BOLD}{Colors.CYAN}{'BUDGET STATUS':^60}{Colors.RESET}")
    lines.append(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    total_budget = sum(budgets.values())
    total_spent_overall = sum(
        expense_manager.get_budget_status(cat)["spent"]
        for cat in budgets
    )
    lines.append(f"\n  {'Category':<15} {'Budget':>10} {'Spent':>10} {'Remain':>10} {'Used':>8}")
    lines.append(f"  {'-' * 58}")
    for cat in sorted(budgets.keys()):
        status = expense_manager.get_budget_status(cat)
        color = Colors.GREEN if status["percentage"] < 80 else (Colors.YELLOW if status["percentage"] < 100 else Colors.RED)
        lines.append(
            f"  {cat:<15} {format_currency(status['budget']):>10} "
            f"{format_currency(status['spent']):>10} "
            f"{format_currency(max(0, status['remaining'])):>10} "
            f"{color}{status['percentage']:>7.1f}%{Colors.RESET}"
        )
    lines.append(f"  {'-' * 58}")
    lines.append(
        f"  {'TOTAL':<15} {format_currency(total_budget):>10} "
        f"{format_currency(total_spent_overall):>10} "
        f"{format_currency(max(0, total_budget - total_spent_overall)):>10} "
        f"{(total_spent_overall / total_budget * 100):>7.1f}%" if total_budget > 0 else ""
    )
    over_budget = [cat for cat in budgets if expense_manager.get_budget_status(cat)["spent"] > budgets[cat]]
    near_limit = [cat for cat in budgets if 80 <= expense_manager.get_budget_status(cat)["percentage"] < 100]
    if over_budget:
        lines.append(f"\n  {Colors.RED}⚠ Over Budget: {', '.join(over_budget)}{Colors.RESET}")
    if near_limit:
        lines.append(f"  {Colors.YELLOW}⚠ Near Limit: {', '.join(near_limit)}{Colors.RESET}")
    lines.append(f"\n{Colors.CYAN}{'-' * 60}{Colors.RESET}")
    return "\n".join(lines)
