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

    # Defining getters and setters
    @property
    def _funds(self):
        return self._funds

    @_funds.setter
    def _funds(self, value):
        if value < 0:
            raise ValueError("Funds must be greater than 0.")
        else:
            self._funds = value

    @property
    def _expenditures(self):
        return self._expenditures

    @_expenditures.setter
    def _expenditures(self, expenditure):
        # Takes an expenditure object (defined later)
        self._expenditures.append(expenditure)

    @property
    def _current_balance(self):
        return self._current_balance
    
    @_current_balance.setter
    def _current_balance(self, value):
        if value < 0:
            raise ValueError("New current balance must be greater than 0.")
        else:
            self._current_balance = value

    @property
    def _name(self):
        return self._name

    @_name.setter
    def _name(self, value):
        self._name = value

    def update_expenditures(self):
        pass
        # TODO: Define once the expenditures class is defined

# TODO: Add expenditure class
# TODO: Add method to subtract the expenditures in the list from funds to get the current balance
