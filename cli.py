import argparse
import errno
import os
import shelve
import sys

from fynance_core import account


def get_account(account_name):
    with shelve.open("accounts", 'c') as shelf:
        account = shelf[account_name]

    return account

def get_category(account, category_name):
        category = account.categories[category_name]
        return category

def get_expenditure(account_name, expenditure_name):
    with shelve.open("accounts", 'c') as shelf:
        account = shelf[account_name]
        expenditures = [item for item in account.expenditures if item.name == expenditure_name]
    
    return expenditures

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
    if account_name != '':
        account = account.Account(name=account_name, funds=account_funds,
                                  monthly_income=account_monthly_income)
        account.sync()
    else:
        print("Account name may not be left blank")
        sys.exit(errno.EAGAIN)
    
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

        print("Account information (To see expenditures, use view expenditures)")
        print("Name\tFunds\tMonthly Income")
        print(account.name, account.funds, account.monthly_income, sep='\t')

        print("Categories:")
        for category in account.categories:
            print(category)
            # The category key is simply the name of the category, so this code just gets the name of the category
            # As it's much simpler than doing acct.categories[category].name

        print('\n')

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
        cat_budget = input("Category budget >> $")
    except ValueError:
        print("Integers only")
        sys.exit(errno.EAGAIN)

    if cat_name != '':
        account.add_category(name=cat_name, desc=cat_desc, budget=cat_budget)
        account.sync()
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
    new_name = input("New name >> ")
    new_desc = input("New description >> ")
    try:
        new_budget = input("New budget >> $")
        if new_budget != '':
            new_budget = int(new_budget)

    except ValueError:
        print("Integers only")
        sys.exit(errno.EAGAIN)

    if new_name != '':
        category.name = new_name
    if new_desc != '':
        category.desc = new_desc
    if new_budget != '':
        category.budget = new_budget

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
    
    print("Name\tDesc.\tBudget")
    print(category.name, category.desc, category.budget, sep='\t')

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
    exp_cat = input("Expenditure category >> ")
    try:
        exp_amount = int(input("Expenditure amount >> $"))
    except ValueError:
        print("Integers only")
        sys.exit(errno.EAGAIN)
    
    if exp_name != '' and exp.amount > 0:
        account.add_expenditure(exp_name, exp_desc, exp_amount, exp_cat)

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
    for expenditure in account.expenditures:
        if expenditure.name == exp_to_remove:
            account.remove(expenditure)
    # Due to the fact that account.expenditures is a list, this unfortunate for loop is necessary
    # TODO: Rewrite account.expenditures so it's a dict

def edit_expenditure():
    print("Expenditures are not editable.")
    sys.exit(0)

def view_expenditures():
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

    print("Name\tDesc\tAmount\tCategory")
    for item in account.expenditures:
        print(item.name, item.desc, item.amount, item.category, sep='\t')

def first_setup():
    add_account()
    add_category()
    # TODO: Write feature to detect if the accounts file already exists

functions = {"add_account": add_account, "add_category": add_category,
             "add_expenditure": add_expenditure, "remove_account": remove_account,
             "remove_category": remove_category, "remove_expenditure": remove_expenditure,
             "edit_account": edit_account, "edit_category": edit_category,
             "view_account": view_account, "view_category": view_category,
             "view_expenditures": view_expenditures, "edit_expenditure", edit_expenditure}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Specifies the command to run",
                        choices=("add", "remove", "edit", "view"))
    parser.add_argument("object", help="Specifies the type of object to perform the command on",
                        choices=("account", "category", "expenditure"))

    args = parser.parse_args()

    func_to_call = "_".join((args.command.lower(), args.object.lower()))
    functions[func_to_call]()

if __name__ == "__main__":
    main()
