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
        self.expenditures = None

    def sync_expenditures(self):
        # Function to sync the expenditures in the account with that of a category
        self.expenditures = [x for x in self.account.expenditures if x.category==self.name]
        # List comprehension of all the expenditures in the account if the expenditure's
        # category is the same as the category's name
