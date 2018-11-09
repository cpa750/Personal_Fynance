from fynance_core import account

import argparse, os, shelve, sys

def get_account(account_name):
    with shelve.open("accounts") as shelf:
        account = shelf[account_name]
        return account

def add_account():
    print("Add Account Wizard")
    account_name = input("Account name to create >> ").capitalize()
    try:
        account_funds = int(input("Account funds (for none enter 0) >> $"))
        account_monthly_income = int(input("Account monthly income >> $"))
    except ValueError:
        print("Integers only!")
        print("Account creation failed, exiting...")
        return
    acct = account.Account(name=account_name, funds=account_funds,
                           monthly_income=account_monthly_income)
    acct.sync()
    
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
        print("Account removal failed, exiting...")
        sys.exit()

    for attribute in dir(account):
        new_value = input("New value for {} >> ".format(attribute))
        if new_value != '':
            setattr(account, attribute, new_value)
    
def view_account():
    pass

def add_category():
    pass
def remove_category():
    pass
def edit_category():
    pass
def view_category():
    pass

def add_expenditure():
    pass
def remove_expenditure():
    pass
def edit_expenditure():
    pass
def view_expenditure():
    pass
# TODO: Write the rest of these

def first_setup():
    add_account()
    add_category()
    # TODO: Write feature to detect if the accounts file already exists

functions = {"add_account": add_account, "add_category": add_category,
             "add_expenditure": add_expenditure, "remove_account": remove_account,
             "remove_category": remove_category, "remove_expenditure": remove_expenditure,
             "edit_account": edit_account, "edit_category": edit_category,
             "edit_expenditure": edit_expenditure}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Specifies the command to run",
                        choices=("add", "remove", "edit", "view"))
    parser.add_argument("object", help="Specifies the type of object to perform the command on",
                        choices=("account", "category", "expenditure"))

    args = parser.parse_args()

    func_to_call = "_".join((args.command, args.object))
    functions[func_to_call]()
    # TODO: This is a hacky workaround, figure out how to implement subparsers

if __name__ == "__main__":
    main()

# TODO: FIX THIS ABSOLUTE MESS OF A SCRIPT
