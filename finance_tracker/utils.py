import re
from datetime import datetime


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    UNDERLINE = '\033[4m'


CATEGORIES = [
    "Food", "Transport", "Entertainment", "Bills",
    "Shopping", "Healthcare", "Education", "Other"
]


def print_header(title, width=60, char="="):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{char * width}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title:^{width}}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{char * width}{Colors.RESET}")


def print_subheader(title, width=40, char="-"):
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{char * width}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{title:^{width}}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{char * width}{Colors.RESET}")


def print_success(message):
    print(f"{Colors.GREEN}{message}{Colors.RESET}")


def print_error(message):
    print(f"{Colors.RED}{message}{Colors.RESET}")


def print_warning(message):
    print(f"{Colors.YELLOW}{message}{Colors.RESET}")


def print_info(message):
    print(f"{Colors.BLUE}{message}{Colors.RESET}")


def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > 999999999.99:
            raise ValueError("Amount exceeds maximum limit")
        return round(amount, 2)
    except ValueError as e:
        if str(e) in ["Amount must be positive", "Amount exceeds maximum limit"]:
            raise
        raise ValueError("Invalid amount. Please enter a valid number")


def validate_date(date_str):
    date_str = date_str.strip()
    if not date_str:
        return datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")


def validate_category(category_str):
    category_str = category_str.strip().title()
    for cat in CATEGORIES:
        if cat.lower() == category_str.lower():
            return cat
    if category_str in CATEGORIES:
        return category_str
    return None


def validate_description(desc_str):
    desc_str = desc_str.strip()
    if not desc_str:
        raise ValueError("Description cannot be empty")
    if len(desc_str) > 200:
        raise ValueError("Description too long (max 200 characters)")
    return desc_str


def get_valid_input(prompt, validator=None, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if allow_empty and not value:
            return value
        if not value:
            print_error("Input cannot be empty")
            continue
        if validator:
            try:
                return validator(value)
            except ValueError as e:
                print_error(str(e))
                continue
        return value


def get_valid_amount(prompt="Enter amount: "):
    return get_valid_input(prompt, validate_amount)


def get_valid_date(prompt="Enter date (YYYY-MM-DD) or Enter for today: "):
    return get_valid_input(prompt, validate_date, allow_empty=True)


def select_category():
    print_subheader("CATEGORIES")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {Colors.BOLD}{i}.{Colors.RESET} {cat}")
    while True:
        choice = input(f"\nSelect category (1-{len(CATEGORIES)}): ").strip()
        try:
            idx = int(choice)
            if 1 <= idx <= len(CATEGORIES):
                return CATEGORIES[idx - 1]
            print_error(f"Please enter a number between 1 and {len(CATEGORIES)}")
        except ValueError:
            print_error("Invalid input. Please enter a number")


def format_currency(amount):
    return f"${amount:,.2f}"


def confirm_action(prompt="Are you sure? (y/n): "):
    response = input(prompt).strip().lower()
    return response in ('y', 'yes')


def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
