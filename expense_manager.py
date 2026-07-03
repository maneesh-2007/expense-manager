import json
import sqlite3 as sql
from expense import Expense
class ExpenseManager:
    def __init__(self):
        self.expenses = {}
        self.next_id = 1

    def add_expense(self, expense):
        self.expenses[self.next_id] = expense
        expense.id = self.next_id
        self.next_id += 1

    def view_expenses(self):

        if not self.expenses:
            print("No expenses currently.")
            return
        
        for expense in self.expenses.values():
            print(expense)
            print()

    def delete_expense(self, id):
        if id in self.expenses:
            del self.expenses[id]
            return True
        else:
            print("No expense with ID", id)
            return False

    @property
    def total_spending(self):
        return sum(expense.amount for expense in self.expenses.values())
    
    def find_by_category(self, category):
        
        expenses = [expense for expense in self.expenses.values() if expense.category.lower() == category.lower()]
        if not expenses:
            print("No expenses in this category.")
        return expenses
    
    def save(self, database_name):
        conn = sql.connect(database_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses
            (ID INTEGER PRIMARY KEY,
            Amount REAL,
            Category TEXT,
            Description TEXT,
            Date DATE)
            '''
        )
        curr_ids = []
        for expense_id, expense in self.expenses.items():
            cursor.execute('''
            INSERT INTO expenses (ID, Amount, Category, Description, Date)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(ID)
            DO UPDATE SET Amount = excluded.Amount, Category = excluded.Category, Description = excluded.Description, Date = excluded.Date
            ''', (expense_id, expense.amount, expense.category, expense.description, expense.date))
            curr_ids.append(expense_id)
        placeholders = ','.join(['?' for x in curr_ids])
        cursor.execute(f'DELETE FROM expenses WHERE ID NOT IN ({placeholders})', curr_ids)
        conn.commit()
        conn.close()

    #ID, Amount, Category, Description, Date
    def load(self, file_name):
        conn = sql.connect(file_name)
        cursor = conn.cursor()
        cursor.execute('SELECT ID, Amount, Category, Description, Date FROM expenses')
        expenses = cursor.fetchall()
        self.expenses = {}
        self.next_id = 1
        for expense_id, amount, category, description, date in expenses:
            self.expenses[expense_id] = Expense(float(amount), category, description, date, expense_id)
            self.next_id = max(expense_id + 1, self.next_id)
        