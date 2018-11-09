import shelve
from datetime import date, timedelta

from . import category as cat
from . import expenditure as exp


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
        self.pay_day = date.today()

    def __str__(self):
        return "Account {}".format(self.name)

    def add_expenditure(self, name, desc, amount, category):
        """
        This function adds an expenditure to the account.
        In addition, if the expenditure's category is in the
        account's list of categories, it will also add the
        expenditure to the category.
        """
        expenditure = exp.Expenditure(name=name, desc=desc,
                                      amount=amount, category=category)
        
        self.expenditures.append(expenditure)
        self.funds -= expenditure.amount

        category_name = self.check_for_cat(expenditure.category)
        if category_name is not None:
            category = self.categories[category_name]
            category.add_expenditure(expenditure)
            category.sync_expenditures()

for attribute in dir(account):
        new_value = input("New value for {} (To keep unchanged, press enter) >> ".format(attribute))
        if new_value != '':
            setattr(account, attribute, new_value)    def check_for_cat(self, category_name):
        """
        Searching the account.categories dict for the category name.
        The dict is organized cat.name: Category
        Hence the above spaghetti code.
        This is so the string identifying the category in the expense class
        can easily match up with a category with an entry in account.categories,
        and get the category class"""
        for key in self.categories:
            if category_name == key:
                return category_name
        return None

    def add_category(self, name, desc, budget):
        category = cat.Category(account=self, name=name,
                                 desc=desc, budget=budget)
        
        self.categories[category.name] = category

    def rem_category(self, name):
        if name in self.categories:
            del self.categories[name]

    def check_for_pay_day(self):
        """
        Method to check if a payday has passed, and if
        it has, automatically add funds to the account
        """
        if date.now() >= self.pay_day + timedelta(days=30):
            self.funds += self.monthly_income
            self.pay_day += timedelta(weeks=4)

    def sync(self):
        """
        Function to write the account to the shelf after modifying.
        Call after user commands.
        """
        with shelve.open("accounts", 'c') as shelf:
            shelf[self.name] = self
