import shelve

def check_paydays():
    with shelve.open("accounts", 'c') as shelf:
        for account in shelf:
            shelf[account].check_for_pay_day()

def check_for_account(account_name):
    # Checking if an account exists
    if account_name in shelve.open("accounts", 'c'):
        return True
    else:
        return False

def check_for_category(account, category_name):
    # Checking if a category exists. must take an account object as a param
    if category_name in account.categories:
        return True
    else:
        return False

def check_for_expenditure(account, expenditure_name):
    # Checking if an exp. exists. must take an account object as a param
    if expenditure_name in account.expenditures:
        return True
    else:
        return False

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
