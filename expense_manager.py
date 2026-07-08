from typing import List, Dict
import sqlite3 as sql
from expense import Expense
class ExpenseManager:
    def __init__(self, database_name: str) -> None:
        self.expenses: Dict[int, Expense] = {}
        self.next_id: int = 1
        self.database_name: str = database_name

    def add_expense(self, expense: Expense) -> None:
        self.expenses[self.next_id] = expense
        expense.id = self.next_id
        self.next_id += 1

    def view_expenses(self) -> None:

        if not self.expenses:
            print("No expenses currently.")
            return
        
        for expense in self.expenses.values():
            print(expense)
            print()

    def delete_expense(self, id) -> bool:
        if id in self.expenses:
            del self.expenses[id]
            return True
        else:
            print("No expense with ID", id)
            return False

    @property
    def total_spending(self) -> float:
        return sum(expense.amount for expense in self.expenses.values())
    
    def find_by_category(self, category: str) -> List[Expense]:
        
        expenses = [expense for expense in self.expenses.values() if expense.category.lower() == category.lower()]
        if not expenses:
            print("No expenses in this category.")
        return expenses
    
    def view_file_names(self) -> None:
        conn: sql.Connection = sql.connect(self.database_name)
        cursor: sql.Cursor = conn.cursor()

        cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
        for serial, name in enumerate(cursor.fetchall()):
            file_name = name[0]
            print(f"{serial + 1}. {file_name}")
        conn.close()

    def save(self, file_name: str, force_empty: bool = False) -> bool:
        temp: str = ''
        for char in file_name:
            if char.isalnum() or char == '_':
                temp += char
        file_name = temp
        if not file_name:
            print("Enter valid file name.")
            return False
        conn: sql.Connection = sql.connect(self.database_name)
        cursor: sql.Cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS "{file_name}"
            (ID INTEGER PRIMARY KEY,
            Amount REAL,
            Category TEXT,
            Description TEXT,
            Date DATE)
            ''')
        
        for expense_id, expense in self.expenses.items():
            cursor.execute(f'''
            INSERT INTO {file_name} (ID, Amount, Category, Description, Date)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(ID)
            DO UPDATE SET Amount = excluded.Amount, Category = excluded.Category, Description = excluded.Description, Date = excluded.Date
            ''', (expense_id, expense.amount, expense.category, expense.description, expense.date))
        curr_ids: List[int] = list(self.expenses)
        placeholders: str = ','.join(['?' for x in curr_ids])
        if curr_ids:
            cursor.execute(f'DELETE FROM "{file_name}" WHERE ID NOT IN ({placeholders})', curr_ids)
        elif force_empty:
            cursor.execute(f'DELETE FROM "{file_name}"')
        print(f"File saved as {file_name}")
        conn.commit()
        conn.close()
        return True

    def load(self, file_name: str) -> bool:
        temp: str = ''
        for char in file_name:
            if char.isalnum() or char == '_':
                temp += char
        initial_name = file_name
        file_name = temp
        if not file_name:
            print("Enter valid file name.")
            return False
        conn: sql.Connection = sql.connect(self.database_name)
        cursor: sql.Cursor = conn.cursor()
        cursor.execute('Select name FROM sqlite_master WHERE type="table" AND name=?', [file_name])
        if not cursor.fetchone():
            print("Enter the name of an existing file to load.")
            conn.close()
            return False
        cursor.execute(f'SELECT ID, Amount, Category, Description, Date FROM "{file_name}"')
        expenses: List[tuple[int, float, str, str, str]]= cursor.fetchall()
        self.expenses = {}
        self.next_id = 1
        for expense_id, amount, category, description, date in expenses:
            self.expenses[expense_id] = Expense(float(amount), category, description, date, expense_id)
            self.next_id = max(expense_id + 1, self.next_id)
        print(f'File ({initial_name} -> {file_name}) loaded successfully.')
        conn.close()
        return True

    def delete_files(self, file_names: List[str], del_all_files: bool = False) -> None:
        sanitized_file_names = []
        for file_name in file_names:
            temp: str = ''
            for char in file_name:
                if char.isalnum() or char == '_':
                    temp += char
            sanitized_file_names.append(temp)
            
        conn: sql.Connection = sql.connect(self.database_name)
        cursor: sql.Cursor = conn.cursor()
        deleted_files = []
        number = -1
        for file_name in sanitized_file_names:
            number += 1
            if not file_name:
                print(f"File ({file_names[number]} -> {file_name}) is invalid")
                continue
            cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?', [file_name])
            if cursor.fetchone():
                cursor.execute(f'DROP TABLE "{file_name}"')
                deleted_files.append(file_name)
            else:
                print(f"File ({file_names[number]} -> {file_name}) not found. Skipped.")

        if deleted_files:
            statement = 'Files'
            for file_name in deleted_files:
                statement += ' ' + file_name + ','
            print(statement[0:-1] + " deleted successfully.")
        else:
            print("No files deleted.")
        conn.commit()
        conn.close()
    