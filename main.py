from expense import Expense
from expense_manager import ExpenseManager

manager = ExpenseManager()
# car = Expense(300000, "Vehicle", "New car bought.", "13-06-2026")
# Food = Expense(300, "Food", "Ate food outside.", "14-06-2026")
# manager.add_expense(car)
# manager.add_expense(Food)

# manager.save("my_expenses.json")
manager.load("my_expenses.json")
manager.view_expenses()