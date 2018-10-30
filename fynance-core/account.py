import argparse as ap

class Account:
    """
    Main class for the account holder.
    Holds things such a monthly income, expenditures, etc.
    """

    def __init__(self, name):
        self._funds = 0
        self._expenditures = []
        self._current_balance = 0
        self._name = name
        self._budget = None

    def _update_current_balance(self):
        """
        Function to update the current balance, typically after an expenditure has been added
        """
        if len(self._expenditures()) > 0:
            total = 0
            for item in self._expenditures:
                total += item["amount"]

            self._current_balance = self._funds - total
        
        else:
            self._current_balance = self._funds

    def _add_expenditures(self, name, description, category, value):
        """
        Function that will add a single expenditure, in the form
        of a dict, to the expenditures attribute
        """
        expenditure = {}
        expenditure["name"] = name
        expenditure["description"] = description
        expenditure["category"] = category
        expenditure["value"] = value

        self._expenditures.append(expenditure)
        self._update_current_balance()
