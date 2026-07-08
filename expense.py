from typing import Dict, Any
class Expense:
    
    def __init__(self, amount: float, category: str, description: str, date: str , expense_id: Any = None) -> None:
        self.amount: float = amount
        self.category: str = category
        self.description: str = description
        self.date: str = date
        self.id: Any = expense_id

    def __str__(self) -> str:
        return (
            f"ID          : {self.id}\n"
            f"Amount      : {self.amount}\n"
            f"Category    : {self.category}\n"
            f"Description : {self.description}\n"
            f"Date        : {self.date}"
        )
    
    def dict_version(self) -> Dict[str, Any]:
        return {
                "id" : self.id,
                "amount" : self.amount,
                "category" : self.category,
                "description" : self.description,
                "date" : self.date
               }
    
    @staticmethod
    def from_dict(expense: Dict[str, Any]) -> 'Expense':
        return Expense(expense["amount"], expense["category"], expense["description"], expense["date"], expense["id"])