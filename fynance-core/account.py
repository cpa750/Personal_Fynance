import expenditure as exp

class Account:
    """
    Main class for the account holder.
    Holds things such a monthly income, expenditures, etc.
    """

    def __init__(self, name):
        self.funds = 0
        self.expenditures = []
        self.currentbalance = 0
        self.name = name
        self.categories = {}

    def update_current_balance(self):
        """
        Function to update the current balance, typically after an expenditure has been added
        """
        if len(self.expenditures) > 0:
            total = 0
            for item in self.expenditures:
                total += item["amount"]

            self.currentbalance = self.funds - total
        
        else:
            self.currentbalance = self.funds
    
    def add_expenditure(self, name, desc, amount, category):
        expenditure = exp.Expenditure(name=name, desc=desc,
                                      amount=amount, category=category)
        
        self.expenditures.append(expenditure)
        self.update_current_balance()

    def check_for_category(self, exepnditure):
        if exepnditure.category in self.categories:
            pass

    def add_category(self, name, limit):
        self.categories[name] = limit

    def rem_category(self, name):
        if name in self.categories:
            del self.categories[name]

        # Must call update_current_balance to update after adding the expenditure
