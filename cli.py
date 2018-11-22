# TODO: fix bug where expenditure is removed but funds are not added back into category if there is one
# TODO: add proper category support for expenses, not just a string
    # Must implement get_category

import argparse
# Used to parse command line arguments to get command to run
import errno
# Used for the appropriate error codes where applicable
import shelve
# Used to store all account objects
import sys
# Used for system functions, namely sys.exit

from tabulate import tabulate
# Used to print object attributes in an organized format

from fynance_core import account as acct

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
    # Checking if an exp. exists. must take an account obkject as a param.
    exp_names = [exp.name for exp in account.expenditures]
    if expenditure_name in exp_names:
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
    for exp in account.expenditures:
        if exp.name == expenditure_name:
            return exp
    else:
        return None

def add_account():
    print("Add Account Wizard")
    account_name = input("Account name to create >> ").capitalize()
    try:
        account_funds = int(input("Account funds (for none enter 0) >> $"))
        account_monthly_income = int(input("Account monthly income >> $"))
    except ValueError:
        print("Integers only!")
        print("Account creation failed, exiting...")
        sys.exit(errno.EAGAIN)

    if check_for_account(account_name):
        print("Account name already exists")
        sys.exit(errno.EAGAIN)

    if account_name != '':
        account = acct.Account(name=account_name, funds=account_funds,
                                  monthly_income=account_monthly_income)
        account.sync()
        # Must call account.sync to write changes to shelf
    else:
        print("Account name may not be left blank")
        sys.exit(errno.EAGAIN)
    # Cannot create an account with an empty name
    
def remove_account():
    print("Account Removal Wizard")
    with shelve.open("accounts", 'c') as shelf:
        account_name = input("Account name to remove >> ")
        try:
            del shelf[account_name]
        except KeyError:
            print("Invalid account name.")
            print("Valid account names:")
            for key in shelf:
                print(key)
            print("Account removal failed, exiting...")

def edit_account():
    print("Account Editing Wizard")
    print("To keep a current value, simply press enter")
    account_name = input("Account name to edit >> ")
    try:
        account = get_account(account_name)
    except KeyError:
        print("Invalid account name.")
        print("Valid account names:")
        with shelve.open("accounts", 'c') as shelf:
            for key in shelf:
                print(key)
        print("Account edit failed, exiting...")
        sys.exit(errno.EAGAIN)

    print("To leave any value unchanged, simply press enter")
    new_name = input("New name >> ")
    try:
        new_monthly_income = int(input("New monthly income >> $"))
    except ValueError:
        print("Integers only")
        sys.exit(errno.EAGAIN)

    if new_name != '':
        account.name = new_name
    if new_monthly_income != '':
        account.monthly_income = new_monthly_income
    
    account.sync()
    # Must call account.sync to write changes to shelf
    
def view_account():
    with shelve.open("accounts", 'c') as accounts:
        print("Accounts available to view: ")
        for account in accounts:
            print(account)
        
        account_name = input("Account to view >> ")
            
        try:
            account = accounts[account_name]
        except KeyError:
            print("Not a valid account name!")
            sys.exit(errno.EAGAIN)

        print("Account information (To see expenditures, use view expenditure)")
        headers = ("Name", "Funds ($)", "Monthly Income ($)")
        properties = [[account.name, account.funds, account.monthly_income]]
        print(tabulate(properties, headers=headers))
        # Tabulate must take a list of lists as a pos. arg.

        print("Categories:")
        for category in account.categories:
            print(category)
            # The category key is simply the name of the category, so this code just gets the name of the category
            # As it's much simpler than doing acct.categories[category].name

def add_category():
    print("Add Category Wizard")
    acct_to_get = input("Account to add the category >> ")

    try:
        account = get_account(acct_to_get)
    except KeyError:
        print("Invalid account name")
        print("Valid account names:")
        with shelve.open("accounts", 'c') as shelf:
            for item in shelf:
                print(item)
        sys.exit(errno.EAGAIN)
    
    cat_name = input("Category name >> ")
    cat_desc = input("Category description (if none press enter) >> ")
    try:
        cat_budget = int(input("Category budget >> $"))
    except ValueError:
        print("Integers only")
        sys.exit(errno.EAGAIN)

    if check_for_category(account, cat_name):
        print("Category name already exists")

    if cat_name != '':
        account.add_category(name=cat_name, desc=cat_desc, budget=cat_budget)
        account.sync()
        # Must call account.sync to write changes to shelf
    else:
        print("Category name may not be left blank")
        sys.exit(errno.EAGAIN)

def remove_category():
    print("Remove Category Wizard")
    account_name = input("Account to remove category from >> ")
    try:
        account = get_account(account_name)
    except KeyError:
        print("Invalid account name")
        print("Valid account names:")
        with shelve.open("accounts", 'c') as shelf:
            for item in shelf:
                print(item)
        sys.exit(errno.EAGAIN)

    cat_to_remove = input("Category to remove >> ")
    try:
        del account.categories[cat_to_remove]
        account.sync()
    except KeyError:
        print("Invalid category name")
        print("Valid category names:")
        for cat in account.categories:
            print(cat)
        sys.exit(errno.EAGAIN)

    account.sync()
    # Must call account.sync to write changes to shelf

def edit_category():
    print("Edit Category Wizard")
    account_name = input("Account to edit category from >> ")
    try:
        account = get_account(account_name)
    except KeyError:
        print("Invalid account name")
        print("Valid account names:")
        with shelve.open("accounts", 'c') as shelf:
            for item in shelf:
                print(item)
        sys.exit(errno.EAGAIN)
    
    cat_to_edit = input("Category to edit >> ")
    try:
        category = get_category(account, cat_to_edit)
    except KeyError:
        print("Invalid category name")
        print("Valid category names:")
        for cat in account.categories:
            print(cat)
        sys.exit(errno.EAGAIN)
    
    print("To leave any value unchanged, simply press enter")
    new_desc = input("New description >> ")
    try:
        new_budget = input("New budget >> $")
        if new_budget != '':
            new_budget = int(new_budget)
    except ValueError:
        print("Integers only")
        sys.exit(errno.EAGAIN)

    if new_desc != '':
        category.desc = new_desc
    if new_budget != '':
        category.budget = new_budget

    account.sync()
    # Must call account.sync to write changes to shelf

def view_category():
    account_name = input("Account to view category from >> ")
    try:
        account = get_account(account_name)
    except KeyError:
        print("Invalid account name")
        print("Valid account names:")
        with shelve.open("accounts", 'c') as shelf:
            for item in shelf:
                print(item)
        sys.exit(errno.EAGAIN)
    
    cat_name = input("Category to view >> ")
    try:
        category = get_category(account, cat_name)
    except KeyError:
        print("Invalid category name")
        print("Valid category names:")
        for cat in account.categories:
            print(cat)
        sys.exit(errno.EAGAIN)
    
    headers = ("Name", "Description", "Budget ($)", "Funds ($)")
    properties = [[category.name, category.desc, category.budget, category.funds]]
    print(tabulate(properties, headers=headers))

def add_expenditure():
    account_name = input("Name of account to add expenditure  >> ")
    try:
        account = get_account(account_name)
    except KeyError:
        print("Invalid account name")
        print("Valid account names:")
        with shelve.open("accounts", 'c') as shelf:
            for item in shelf:
                print(item)
        sys.exit(errno.EAGAIN)

    exp_name = input("Expenditure name >> ")
    exp_desc = input("Expenditure description >> ")
    exp_cat = input("Expenditure category (For none press enter) >> ")
    try:
        exp_amount = int(input("Expenditure amount >> $"))
    except ValueError:
        print("Integers only")
        sys.exit(errno.EAGAIN)
    
    if exp_cat not in account.categories:
        exp_cat = None

    if check_for_expenditure(account, exp_name):
        print("Expenditure already exists")
        sys.exit(errno.EAGAIN)
    
    if exp_name != '' and exp_amount > 0:
        account.add_expenditure(exp_name, exp_desc, exp_amount, exp_cat)
        account.sync()

def remove_expenditure():
    account_name = input("Account to remove expenditure from >> ")
    try:
        account = get_account(account_name)
    except KeyError:
        print("Invalid account name")
        print("Valid account names:")
        with shelve.open("accounts", 'c') as shelf:
            for item in shelf:
                print(item)
        sys.exit(errno.EAGAIN)

    exp_to_remove = input("Name of expenditure to remove >> ")
    exp = get_expenditure(account, exp_to_remove)
    account.expenditures.remove(exp)
    account.funds += exp.amount
    if exp.category != None:
        exp.category.funds += exp.amount

def edit_expenditure():
    print("Expenditure editing wizard")
    account_name = input("Account to edit expenditure from >> ")
    try:
        account = get_account(account_name)
    except KeyError:
        print("Invalid account name")
        print("Valid account names:")
        with shelve.open("accounts", 'c') as shelf:
            for item in shelf:
                print(item)
        sys.exit(errno.EAGAIN)

    exp_name = input("Name of expenditure to edit >> ")
    exp = get_expenditure(account, exp_name)

    if exp is not None:
        print("To leave any value unchanged, simply press enter")
        new_desc = input("New description >> ")
        if new_desc != '':
            exp.desc = new_desc
            account.sync()

    else:
        print("Expenditure does not exist. To see all expenditures, run \"view expenditure\"")

def view_expenditures():
    account_name = input("Account to view expenditure from >> ")
    try:
        account = get_account(account_name)
    except KeyError:
        print("Invalid account name")
        print("Valid account names:")
        with shelve.open("accounts", 'c') as shelf:
            for item in shelf:
                print(item)
        sys.exit(errno.EAGAIN)

    properties = [[exp.name, exp.desc, exp.amount, exp.category] for exp in account.expenditures]
    headers = ("Name", "Description", "Amount ($)", "Category")
    print(tabulate(properties, headers=headers))

functions = {"add_account": add_account, "add_category": add_category,
             "add_expenditure": add_expenditure, "remove_account": remove_account,
             "remove_category": remove_category, "remove_expenditure": remove_expenditure,
             "edit_account": edit_account, "edit_category": edit_category,
             "view_account": view_account, "view_category": view_category,
             "view_expenditure": view_expenditures, "edit_expenditure": edit_expenditure}
             # Mapping strings to actual commands to relate arguments passed in from argparse to actual functions                           

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Specifies the command to run",
                        choices=("add", "remove", "edit", "view"))
    parser.add_argument("object", help="Specifies the type of object to perform the command on",
                        choices=("account", "category", "expenditure"))
    # Parser takes two arguments: the command, and the object(s) that the command is being performed upon

    args = parser.parse_args()

    func_to_call = "_".join((args.command.lower(), args.object.lower()))
    functions[func_to_call]()
    # Formatting the strings from args to get the appropriate function from the functions dict

if __name__ == "__main__":
    with shelve.open("accounts", 'c') as shelf:
        for account in shelf:
            shelf[account].check_for_pay_day()
    # Checking for each account's payday every time the program is run, even if args are invalid

    main()
