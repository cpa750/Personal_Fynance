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
        self.expenditures = {}
        self.categories = {}
        # Decided to ultimately use a dict here as access is
        # quicker than a list
        self.pay_day = date.today()

    def __str__(self):
        return "Account {}".format(self.name)

    def check_for_pay_day(self):
        """
        Method to check if a payday has passed, and if
        it has, automatically add funds to the account
        """
        if date.today() >= self.pay_day + timedelta(days=30):
            self.funds += self.monthly_income
            self.pay_day += timedelta(days=30)
            for cat in self.categories:
                cat.funds = cat.budget + cat.funds

    def sync(self):
        """
        Function to write the account to the shelf after modifying.
        Call after user commands.
        """
        with shelve.open("accounts", 'c') as shelf:
            shelf[self.name] = self
