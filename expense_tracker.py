"""
Expense Tracker
---------------
A simple command-line program to keep track of daily expenses.

Features:
  - add, view, search, edit and delete expenses
  - set a monthly budget for each category
  - monthly summary report
  - export expenses to a CSV file

Data is saved in a small SQLite database file (expenses.db) that is
created automatically in the same folder the first time you run it.

How to run:
    python expense_tracker.py

Made for learning purposes (first programming project).
"""

import csv
import sqlite3
from datetime import date, datetime

DB_FILE = "expenses.db"
CSV_FILE = "expenses_export.csv"
CURRENCY = "Rs."
WARNING_PERCENT = 80  # warn when this % of a budget is used

DEFAULT_CATEGORIES = ["Food", "Transport", "Housing", "Utilities", "Health",
                      "Entertainment", "Shopping", "Education", "Other"]

conn = sqlite3.connect(DB_FILE)


# ---------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------
def setup_database():
    """Create the tables if they don't exist yet."""
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS categories ("
                "name TEXT PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS expenses ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "amount REAL NOT NULL, "
                "category TEXT NOT NULL, "
                "description TEXT NOT NULL, "
                "expense_date TEXT NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS budgets ("
                "category TEXT PRIMARY KEY, "
                "monthly_limit REAL NOT NULL)")
    for name in DEFAULT_CATEGORIES:
        cur.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))
    conn.commit()


# ---------------------------------------------------------------
# Input helpers (keep asking until the user types something valid)
# ---------------------------------------------------------------
def get_amount(prompt, default=None):
    while True:
        text = input(prompt).strip().replace(",", "")
        if text == "" and default is not None:
            return default
        try:
            amount = float(text)
        except ValueError:
            print("  Please enter a number, like 250 or 199.99")
            continue
        if amount <= 0:
            print("  Amount must be more than 0.")
            continue
        return round(amount, 2)


def get_date(prompt, default=None):
    """Ask for a date as YYYY-MM-DD. Empty input gives today (or default)."""
    while True:
        text = input(prompt).strip()
        if text == "":
            return default if default else date.today().isoformat()
        try:
            d = datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            print("  Please use the format YYYY-MM-DD, like 2026-09-30")
            continue
        if d > date.today():
            print("  The date can't be in the future.")
            continue
        return d.isoformat()


def get_month(prompt):
    """Ask for a month as YYYY-MM. Empty input gives the current month."""
    while True:
        text = input(prompt).strip()
        if text == "":
            return date.today().strftime("%Y-%m")
        try:
            datetime.strptime(text + "-01", "%Y-%m-%d")
            return text
        except ValueError:
            print("  Please use the format YYYY-MM, like 2026-09")


def get_text(prompt, default=None):
    while True:
        text = input(prompt).strip()
        if text == "" and default is not None:
            return default
        if text != "":
            return text
        print("  This can't be empty.")


def get_category(default=None):
    """Show the categories and let the user pick one by number or name."""
    cur = conn.cursor()
    cur.execute("SELECT name FROM categories ORDER BY name")
    names = [row[0] for row in cur.fetchall()]
    print("Categories:")
    for i, name in enumerate(names, start=1):
        print(f"  {i}. {name}")
    while True:
        text = input("Category (number or name): ").strip()
        if text == "" and default is not None:
            return default
        if text.isdigit() and 1 <= int(text) <= len(names):
            return names[int(text) - 1]
        for name in names:
            if name.lower() == text.lower():
                return name
        print("  That category doesn't exist. (Add it from the Categories menu.)")


def ask_yes_no(question):
    return input(question + " (y/n): ").strip().lower() in ("y", "yes")


# ---------------------------------------------------------------
# Showing expenses
# ---------------------------------------------------------------
def print_expenses(rows):
    """rows are (id, amount, category, description, date) tuples."""
    if not rows:
        print("No expenses found.")
        return
    print(f"{'ID':<5}{'Date':<12}{'Category':<15}{'Description':<25}{'Amount':>10}")
    print("-" * 67)
    total = 0
    for row in rows:
        exp_id, amount, category, description, exp_date = row
        print(f"{exp_id:<5}{exp_date:<12}{category:<15}{description[:24]:<25}{amount:>10.2f}")
        total += amount
    print("-" * 67)
    print(f"{len(rows)} expense(s), total: {CURRENCY} {total:.2f}")


def fetch_expenses(where="", params=(), limit=None):
    sql = ("SELECT id, amount, category, description, expense_date "
           "FROM expenses " + where + " ORDER BY expense_date DESC, id DESC")
    if limit:
        sql += " LIMIT " + str(limit)
    cur = conn.cursor()
    cur.execute(sql, params)
    return cur.fetchall()


def month_total(category, month):
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM expenses "
                "WHERE category = ? AND expense_date LIKE ?",
                (category, month + "%"))
    result = cur.fetchone()[0]
    return result if result else 0


# ---------------------------------------------------------------
# Expense menu options
# ---------------------------------------------------------------
def add_expense():
    print("\n--- Add expense ---")
    amount = get_amount("Amount: ")
    category = get_category()
    description = get_text("Description: ")
    exp_date = get_date("Date (YYYY-MM-DD, Enter for today): ")

    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (amount, category, description, expense_date) "
                "VALUES (?, ?, ?, ?)", (amount, category, description, exp_date))
    conn.commit()
    print(f"Saved expense #{cur.lastrowid}: {CURRENCY} {amount:.2f} on {category}.")

    # check the budget for that month
    cur.execute("SELECT monthly_limit FROM budgets WHERE category = ?", (category,))
    row = cur.fetchone()
    if row:
        limit = row[0]
        spent = month_total(category, exp_date[:7])
        percent = spent / limit * 100
        if spent > limit:
            print(f"! Budget EXCEEDED for {category}: spent {spent:.2f} of {limit:.2f}")
        elif percent >= WARNING_PERCENT:
            print(f"! Warning: {percent:.0f}% of the {category} budget is used.")


def view_expenses():
    print("\n--- View expenses ---")
    print("1. Latest 10")
    print("2. A month")
    print("3. All")
    choice = input("Choose: ").strip()
    if choice == "1":
        print_expenses(fetch_expenses(limit=10))
    elif choice == "2":
        month = get_month("Month (YYYY-MM, Enter for this month): ")
        print_expenses(fetch_expenses("WHERE expense_date LIKE ?", (month + "%",)))
    elif choice == "3":
        print_expenses(fetch_expenses())
    else:
        print("Invalid choice.")


def search_expenses():
    print("\n--- Search (leave blank to skip a filter) ---")
    keyword = input("Word in description: ").strip()
    category = input("Category name: ").strip()

    conditions = []
    params = []
    if keyword:
        conditions.append("description LIKE ?")
        params.append("%" + keyword + "%")
    if category:
        conditions.append("category = ? COLLATE NOCASE")
        params.append(category)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    print_expenses(fetch_expenses(where, params))


def get_expense_by_id():
    text = input("Expense ID: ").strip()
    if not text.isdigit():
        print("  That is not a valid ID.")
        return None
    rows = fetch_expenses("WHERE id = ?", (int(text),))
    if not rows:
        print("  No expense with that ID.")
        return None
    return rows[0]


def edit_expense():
    print("\n--- Edit expense ---")
    expense = get_expense_by_id()
    if expense is None:
        return
    exp_id, old_amount, old_category, old_description, old_date = expense
    print_expenses([expense])
    print("Press Enter to keep the old value.")

    amount = get_amount(f"Amount [{old_amount}]: ", default=old_amount)
    category = get_category(default=old_category)
    description = get_text(f"Description [{old_description}]: ", default=old_description)
    exp_date = get_date(f"Date [{old_date}]: ", default=old_date)

    conn.execute("UPDATE expenses SET amount = ?, category = ?, description = ?, "
                 "expense_date = ? WHERE id = ?",
                 (amount, category, description, exp_date, exp_id))
    conn.commit()
    print("Expense updated.")


def delete_expense():
    print("\n--- Delete expense ---")
    expense = get_expense_by_id()
    if expense is None:
        return
    print_expenses([expense])
    if ask_yes_no("Delete this expense?"):
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense[0],))
        conn.commit()
        print("Deleted.")
    else:
        print("Nothing was deleted.")


# ---------------------------------------------------------------
# Budgets
# ---------------------------------------------------------------
def set_budget():
    print("\n--- Set monthly budget ---")
    category = get_category()
    limit = get_amount("Monthly limit: ")
    conn.execute("INSERT OR REPLACE INTO budgets (category, monthly_limit) VALUES (?, ?)",
                 (category, limit))
    conn.commit()
    print(f"Budget for {category} set to {CURRENCY} {limit:.2f} per month.")


def show_budgets(month):
    cur = conn.cursor()
    cur.execute("SELECT category, monthly_limit FROM budgets ORDER BY category")
    budgets = cur.fetchall()
    if not budgets:
        print("No budgets set yet.")
        return
    print(f"{'Category':<15}{'Budget':>10}{'Spent':>10}{'Left':>10}  Status")
    print("-" * 55)
    for category, limit in budgets:
        spent = month_total(category, month)
        percent = spent / limit * 100
        if spent > limit:
            status = "EXCEEDED"
        elif percent >= WARNING_PERCENT:
            status = "WARNING"
        else:
            status = "OK"
        print(f"{category:<15}{limit:>10.2f}{spent:>10.2f}{limit - spent:>10.2f}  {status}")


def budget_status():
    print("\n--- Budget status ---")
    month = get_month("Month (YYYY-MM, Enter for this month): ")
    show_budgets(month)


# ---------------------------------------------------------------
# Reports
# ---------------------------------------------------------------
def monthly_summary():
    print("\n--- Monthly summary ---")
    month = get_month("Month (YYYY-MM, Enter for this month): ")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*), SUM(amount) FROM expenses WHERE expense_date LIKE ?",
                (month + "%",))
    count, total = cur.fetchone()
    print(f"\nSummary for {month}")
    print("=" * 30)
    if not count:
        print("No expenses in this month.")
        return
    print(f"Total spent : {CURRENCY} {total:.2f}")
    print(f"Expenses    : {count}")
    print(f"Average     : {CURRENCY} {total / count:.2f}")

    print("\nBy category:")
    cur.execute("SELECT category, SUM(amount), COUNT(*) FROM expenses "
                "WHERE expense_date LIKE ? GROUP BY category ORDER BY SUM(amount) DESC",
                (month + "%",))
    for category, cat_total, cat_count in cur.fetchall():
        share = cat_total / total * 100
        bar = "#" * int(share / 5)
        print(f"  {category:<15}{cat_total:>10.2f}  {share:5.1f}%  {bar}")

    print("\nBudgets:")
    show_budgets(month)


# ---------------------------------------------------------------
# Categories
# ---------------------------------------------------------------
def list_categories():
    cur = conn.cursor()
    cur.execute("SELECT c.name, COUNT(e.id) FROM categories c "
                "LEFT JOIN expenses e ON e.category = c.name "
                "GROUP BY c.name ORDER BY c.name")
    print(f"\n{'Category':<20}Expenses")
    print("-" * 30)
    for name, count in cur.fetchall():
        print(f"{name:<20}{count}")


def add_category():
    name = get_text("New category name: ").title()
    exists = conn.execute("SELECT 1 FROM categories WHERE name = ? COLLATE NOCASE",
                          (name,)).fetchone()
    if exists:
        print("That category already exists.")
        return
    conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    print(f"Category '{name}' added.")


def category_menu():
    print("\n--- Categories ---")
    print("1. List categories")
    print("2. Add a category")
    choice = input("Choose: ").strip()
    if choice == "1":
        list_categories()
    elif choice == "2":
        add_category()
    else:
        print("Invalid choice.")


# ---------------------------------------------------------------
# Export
# ---------------------------------------------------------------
def export_csv():
    rows = fetch_expenses()
    if not rows:
        print("There is nothing to export.")
        return
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "amount", "category", "description", "date"])
        writer.writerows(rows)
    print(f"Exported {len(rows)} expenses to {CSV_FILE}")


# ---------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------
def main():
    setup_database()
    print("=" * 40)
    print("        EXPENSE TRACKER")
    print("=" * 40)

    while True:
        print("\n===== Main Menu =====")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Search expenses")
        print("4. Edit expense")
        print("5. Delete expense")
        print("6. Set budget")
        print("7. Budget status")
        print("8. Monthly summary")
        print("9. Categories")
        print("10. Export to CSV")
        print("0. Exit")

        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "0":
            break

        actions = {
            "1": add_expense,
            "2": view_expenses,
            "3": search_expenses,
            "4": edit_expense,
            "5": delete_expense,
            "6": set_budget,
            "7": budget_status,
            "8": monthly_summary,
            "9": category_menu,
            "10": export_csv,
        }
        if choice in actions:
            try:
                actions[choice]()
            except (EOFError, KeyboardInterrupt):
                print("\nCancelled.")
        else:
            print("Please enter a number from the menu.")

    conn.close()
    print("Goodbye!")


if __name__ == "__main__":
    main()
