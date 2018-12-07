import shelve

def get_account(account_name):
    # Getting and returning a specific account object. Must use error handling in case account DNE.
    with shelve.open("accounts", 'c') as shelf:
        account = shelf[account_name]
        return account

def get_category(account, category_name):
    # Getting and returning a category. Must handle errors, must take account object as param.
    category = account.categories[category_name]
    return category

def get_expenditure(account, expenditure_name):
    # Getting and returning an expenditure. Returns none if exp. DNE. must take account object as param.
    expenditure = account.expenditures[expenditure_name]
    return expenditure

# TODO: Finish writing tests
