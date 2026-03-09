from fastmcp import FastMCP
import sqlite3,os

from pathlib import Path

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

mcp = FastMCP("Expenses Tracker Server")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@mcp.tool()
def add_expense(description: str, amount: float) -> str:
    """Add a new expense to the tracker."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (description, amount) VALUES (?, ?)", (description, amount))
    conn.commit()
    conn.close()
    return "Expense added successfully."

@mcp.tool()
def get_expenses() -> list:
    """Retrieve all expenses from the tracker."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, amount, date FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return expenses

@mcp.tool()
def delete_expense(expense_id: int) -> str:
    """Delete an expense by its ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return "Expense deleted successfully."

@mcp.tool()
def update_expense(expense_id: int, description: str, amount: float) -> str:
    """Update an existing expense by its ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE expenses SET description = ?, amount = ? WHERE id = ?", (description, amount, expense_id))
    conn.commit()
    conn.close()
    return "Expense updated successfully."
@mcp.tool()
def get_total_expenses() -> float:
    """Calculate the total amount of expenses."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0.0
    conn.close()
    return total

@mcp.tool()
def get_expenses_by_date(start_date: str, end_date: str) -> list:
    """Retrieve expenses within a specific date range."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, amount, date FROM expenses WHERE date BETWEEN ? AND ?", (start_date, end_date))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

if __name__ == "__main__":
    mcp.run()
