# Expense Tracker

A command-line expense tracker built with Python to manage daily expenses. The application stores data using SQLite and allows you to save, load, and manage multiple expense files.

## Features

* Add new expenses
* View all current expenses
* Delete expenses by ID
* Search expenses by category
* Calculate total spending
* Save expenses to a SQLite database
* Load previously saved expense files
* View all saved files
* Delete saved files from the database
* Automatic expense ID generation
* Input validation and basic error handling
* Overwrite existing saved files when required

## Project Structure

```text
expense-manager/
├── expense.py
├── expense_manager.py
├── main.py
├── Expenses.db      # Created automatically after first save
└── README.md
```

## Technologies Used

* Python
* Object-Oriented Programming (OOP)
* SQLite
* Git & GitHub

## How to Run

1. Clone the repository.

```bash
git clone https://github.com/maneesh-2007/expense-manager.git
```

2. Navigate to the project directory.

```bash
cd expense-manager
```

3. Run the application.

```bash
python main.py
```

## Menu Options

1. Add Expense
2. View Expenses
3. Delete Expense
4. Find by Category
5. Show Total Spending
6. View Saved Files
7. Save Expenses
8. Load Expenses
9. Delete Saved Files
10. Exit

## Configuration

* The SQLite database file can be changed by modifying the value passed to `ExpenseManager` in `main.py`:

```python
manager = ExpenseManager("Expenses.db")
```

* The back command can be customized by changing the value of the `BACK` constant in `main.py`:

```python
BACK = "b"
```

## Notes

* Saved expense files are stored as separate tables inside the SQLite database.
* Saving with the name of an existing file updates its contents.
* File names are automatically sanitized to contain only letters, numbers, and underscores.
* Enter the configured back command (default: `b`) during most prompts to return to the main menu.
