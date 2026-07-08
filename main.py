from expense import Expense
from expense_manager import ExpenseManager
from datetime import datetime
from typing import List

# Add methods for viewing and deleting tables from db
BACK: str = 'b'

manager: ExpenseManager = ExpenseManager("Expenses.db")

while True:

    choice: str = input(f"""===== Expense Tracker Menu=====

1.  Add Expense
2.  View Expenses
3.  Delete Expense
4.  Find by Category
5.  Show Total Spending
6.  View saved files
7.  Save Expenses
8.  Load Expenses
9.  Delete files
10. Exit

After selecting a choice enter {BACK} to go back to menu.

Enter your choice(1-9):
""")
    
    if not choice.isdigit():
        print("Choice should be an integer(1-8).")
        continue

    choice: int = int(choice)

    match choice:

        case 1:
            while True:
                amount: str = input("Enter the amount of expense.\n")
                if amount == BACK:
                    break
                try:
                    amount: float = float(amount)
                    if amount <= 0:
                        print("Amount should be a positive number.")
                    else:
                        break
                except ValueError:
                    print("Amount must be a positive number.")
            if amount == BACK:
                continue

            category: str = ''
            description: str = ''
            while not category:
                category = input("Enter the category of expense.\n")
                if category == BACK:
                    break
            if category == BACK:
                continue

            while not description:
                description = input("Add a description to your expense.\n")
                if description == BACK:
                    break
            if description == BACK:
                continue

            while True:
                date: str = input("Enter date (DD-MM-YYYY): ")
                if date == BACK:
                    break
                try:
                    datetime.strptime(date, "%d-%m-%Y")
                    break
                except ValueError:
                    print("Invalid date.")
            if date == BACK:
                continue

            manager.add_expense(Expense(float(amount), category, description, date))
        
        case 2:
            manager.view_expenses()

        case 3:
            while True:
                while True:
                    del_id: str = input("Enter the ID of expense to be deleted.\n")
                    if del_id == BACK:
                        break
                    try:
                        del_id: int = int(del_id)
                        break
                    except ValueError:
                        print("ID can only be a whole number.")
                if del_id == BACK:
                    break
                if manager.delete_expense(del_id):
                    break
            if del_id == BACK:
                continue
        
        case 4:
            category: str = ''
            while not category:
                category = input("Enter the category you wish to search.\n")
                if category == BACK:
                    break
            if category == BACK:
                continue
            category_expenses: List[Expense] = manager.find_by_category(category)
            for item in category_expenses:
                print(item)

        case 5:
            total: float = manager.total_spending
            print(total)

        case 6:
            print(manager.view_file_names())

        case 7:
            while True:
                if not manager.expenses:
                    action = input("Current expense manager is empty, do you want to save an empty file?(Y or N)\n")
                    if action.lower() == 'y':
                        action = True
                        file_name: str = input("Enter the name of file to be saved.\nWarning!If you use the name of an already existing file, it will be overwritten.\n")
                        if file_name == BACK:
                            break
                        if manager.save(file_name, True):
                            break
                    elif action.lower() == 'n':
                        action = False
                        break
                    elif action == BACK:
                        break
                    else:
                        print("Select valid action.(Y or N)")
                else:
                    file_name: str = input("Enter the name of file to be saved.\nWarning!If you use the name of an already existing file, it will be overwritten.\n")
                    if file_name == BACK:
                        break
                    if manager.save(file_name):
                        break
            if file_name == BACK:
                continue
            if not manager.expenses and action == BACK:
                continue

        
        case 8:
            file_name: str = input("Enter the name of file you wish to load.\n")

            while True:
                if file_name == BACK:
                    break
                if manager.load(file_name):
                    break
            if file_name == BACK:
                continue

        case 9:
            file_names = []
            print("Enter file names to be deleted.Enter 'Done' when you have typed all file names.")
            while True:
                file_name = input()
                if file_name == BACK:
                    break
                if file_name.lower() == 'done':
                    break
                file_names.append(file_name)
            if file_name == BACK:
                continue
            manager.delete_files(file_names)

        case 10:
            print("Exiting expense tracker.")
            break