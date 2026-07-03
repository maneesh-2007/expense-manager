from expense import Expense
from expense_manager import ExpenseManager
from datetime import datetime

BACK = 'b'

manager = ExpenseManager()

while True:

    choice = input(f"""===== Expense Tracker Menu=====

1. Add Expense
2. View Expenses
3. Delete Expense
4. Find by Category
5. Show Total Spending
6. Save Expenses
7. Load Expenses
8. Exit

After selecting a choice enter {BACK} to go back to menu.

Enter your choice(1-8):
""")
    
    if not choice.isdigit():
        print("Choice should be an integer(1-8).")
        continue

    choice = int(choice)

    match choice:

        case 1:

            while True:
                amount = input("Enter the amount of expense.\n")
                if amount == BACK:
                    break
                try:
                    amount = float(amount)
                    if amount <= 0:
                        print("Amount should be a positive number.")
                    else:
                        break
                except ValueError:
                    print("Amount must be a positive number.")
            if amount == BACK:
                continue

            category = ''
            description = ''

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
                date = input("Enter date (DD-MM-YYYY): ")

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

                    del_id = input("Enter the ID of expense to be deleted.\n")

                    if del_id == BACK:
                        break

                    try:
                        del_id = int(del_id)
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

            category = ''

            while not category:
                category = input("Enter the category you wish to search.\n")

                if category == BACK:
                    break

            if category == BACK:
                continue

            for item in manager.find_by_category(category):
                print(item)

        case 5:
            print(manager.total_spending)

        case 6:
            file_name = input("Enter the name of file to be saved.\nWarning!\nIf you use the name of an already existing file, it will be overwritten.\n")
            
            if file_name == BACK:
                continue

            manager.save(file_name)
        
        case 7:
            file_name = input("Enter the name of file you wish to load.\n")

            if file_name == BACK:
                continue

            if manager.load(file_name):
                break

        case 8:
            print("Exiting expense tracker.")
            break