from fynance_core import account, category, expenditure

import argparse, os, shelve

def add_account():
    print("Add Account Wizard")
    account_name = input("Account name >> ").capitalize()
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
    pass
def edit_account():
    pass
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

def first_setup():
    add_account()
    add_category()
    # TODO: Write feature to detect if the accounts file already exists

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Specifies the command to run",
                        choices=("add", "remove", "edit", "view"))
    parser.add_argument("object", help="Specifies the type of object to perform the command on",
                        choices=("account", "category", "expenditure"))

    args = parser.parse_args()

    func_to_call = "_".join((args.command, args.object))
    try:
        func_to_call()
    except NameError:
        print("Not a valid command/object!")

# TODO: FIX THIS ABSOLUTE MESS OF A SCRIPT
