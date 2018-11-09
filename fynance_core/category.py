class Category:
    """
    Class for holding information about
    category under an account
    """

    def __init__(self, account, name, desc, budget):
        self.name = name
        self.account = account
        self.desc = desc
        self.budget = budget
        self.funds = budget
        self.expenditures = []

    def __str__(self):
        return "Category {}".format(self.name)

    def add_expenditure(self, expenditure):
        self.expenditures.append(expenditure)
        self.funds -= expenditure.amount
