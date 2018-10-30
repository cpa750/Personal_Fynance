class Expenditure:
    """
    Simple class to hold information about an expenditure under an account
    """
    def __init__(self, name, desc, amount, category):
        self.name = name
        self.desc = desc
        self.amount = amount
        self.category = category
        # When instantiating, category should be selected from Account.categories
