import expenditure as exp
import category as cat

class Account:
    """
    Main class for the account holder.
    Holds things such a monthly income, expenditures, etc.
    """

    def __init__(self, name, funds, monthly_income):
        self.name = name
        self.funds = funds
        self.monthly_income = monthly_income
        self.expenditures = []
        self.categories = {}
        # Decided to ultimately use a dict here as access is
        # quicker than a list

    def __str__(self):
        return "Account {}".format(self.name)

    def update_current_balance(self):
        # Function to update the current balance, typically after an expenditure has been added
        if len(self.expenditures) > 0:
            total = 0
            for item in self.expenditures:
                total += item.amount

            self.funds -= total
    
    def add_expenditure(self, nm, dsc, amt, cat):
        """
        This function adds an expenditure to the account.
        In addition, if the expenditure's category is in the
        account's list of categories, it will also add the
        expenditure to the category.
        """
        expenditure = exp.Expenditure(name=nm, desc=dsc, amount=amt, category=cat)
        
        self.expenditures.append(expenditure)
        self.update_current_balance()

        category_name = self.check_for_cat(expenditure.category)
        if category_name is not None:
            category = self.categories[category_name]
            category.add_expenditure(expenditure)
            category.update_funds()


    def check_for_cat(self, category_name):
        for key in self.categories:
            if category_name == key:
                return category_name
        return None
        """
        Searching the account.categories dict for the category name.
        The dict is organized cat.name: Category
        Hence the above spaghetti code.
        This is so the string identifying the category in the expense class
        can easily match up with a category with an entry in account.categories,
        and get the category class
        """

    def add_category(self, name, desc, budget):
        category = cat.Category(account=self, name=name,
                                 desc=desc, budget=budget)
        
        self.categories[category.name] = category

    def rem_category(self, name):
        if name in self.categories:
            del self.categories[name]

    # TODO: Write in ablility to automagically top-up the monthly income
