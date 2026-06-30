import json
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
        else:
            print("No expense with ID", id)

    @property
    def total_spending(self):
        return sum(expense.amount for expense in self.expenses.values())
    
    def find_by_category(self, category):
        return [expense for expense in self.expenses.values() if expense.category.lower() == category.lower()]
    
    def save(self, file_name):
        save_ver = {"next_id" : self.next_id, "expenses" : {}}
        
        for expense_id, expense in self.expenses.items():
            save_ver["expenses"][expense_id] = expense.dict_version() 
        with open(file_name, 'w', encoding = "utf-8") as file:
            json.dump(save_ver, file, indent = 4)

    def load(self, file_name):
        self.expenses = {}
        with open(file_name, 'r', encoding = "utf-8") as file:
            save_ver = json.load(file)
        self.next_id = save_ver["next_id"]
        for expense_id, expense in save_ver["expenses"].items():
            self.expenses[int(expense_id)] = Expense.from_dict(expense)
