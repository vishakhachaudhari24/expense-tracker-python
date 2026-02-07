import sqlite3

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()


def add_expense():
    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category (Food/Transport/Shopping/Bills/Others): ")
        date = input("Enter date (DD-MM-YYYY): ")

        cursor.execute(
            "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
            (amount, category, date)
        )
        conn.commit()
        print("Expense added successfully!\n")

    except ValueError:
        print("Invalid amount. Please enter a number.\n")


def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    if not rows:
        print("No expenses found.\n")
        return

    print("\n--- Expense List ---")
    for row in rows:
        print(f"ID: {row[0]}, Amount: {row[1]}, Category: {row[2]}, Date: {row[3]}")
    print()


def category_summary():
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)
    rows = cursor.fetchall()

    if not rows:
        print("No expenses to analyze.\n")
        return

    print("\n--- Category-wise Summary ---")
    for row in rows:
        print(f"{row[0]}: {row[1]}")
    print()


def total_expense():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print(f"\nTotal Expense: {total}\n")


def main():
    while True:
        print("===== Expense Tracker (Python + SQL) =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Category-wise Summary")
        print("4. Total Expense")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            category_summary()
        elif choice == "4":
            total_expense()
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice.\n")


main()
conn.close()
