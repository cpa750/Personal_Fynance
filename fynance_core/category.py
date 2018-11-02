class Category:
    """
    Class for holding information about
    category under an account
    """

    def __init__(self, account, name, desc, budget):
        self.name = name
        self.account = account
        self.desc = desc
        self.budget = sbudget
        self.funds = budget
        self.expenditures = []

    def __str__(self):
        return "Category {}".format(self.name)

    def add_expenditure(self, expenditure):
        self.expenditures.append(expenditure)
        self.update_funds()

    def update_funds(self):
        """
        Function to sync the expenditures in the account with that of a category,
        particularly after adding an expenditure to the category
        """
        for expenditure in self.expenditures:
            costs += expenditure.amount
        
        self.funds = self.budget - costs
