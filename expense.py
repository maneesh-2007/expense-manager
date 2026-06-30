class Expense:
    
    def __init__(self, amount, category, description, date):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date
        self.id = None

    def __str__(self):
        return (
            f"ID          : {self.id}\n"
            f"Amount      : {self.amount}\n"
            f"Category    : {self.category}\n"
            f"Description : {self.description}\n"
            f"Date        : {self.date}"
        )
    
    def dict_version(self):
        return {
                "amount" : self.amount,
                "category" : self.category,
                "description" : self.description,
                "date" : self.date
               }
    
    def from_dict(expense):
        return Expense(expense["amount"], expense["category"], expense["description"], expense["date"])