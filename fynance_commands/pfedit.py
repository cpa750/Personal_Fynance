import errno
import sys

from fynance_core.utils import accountmanager, exceptions

accountmanager.check_paydays()

try:
    arg = sys.argv[1].lower()
except IndexError:
    print("Positional argument must be one of the following: 'account', 'category', 'expenditures'.")
    sys.exit(errno.EAGAIN)

if arg == "account":
    account_name = input("Account name: ")
    print("To leave any field unchanged, simply press enter.")
    new_name = input("New account name: ")
    if new_name == '':
        new_name = None
    
    try:
        new_funds = input("New funds: $")
        if new_funds == '':
            new_funds = None
        else:
            new_funds = float(new_funds)

        new_monthly_income = input("New monthly income: $")
        if new_monthly_income == '':
            new_monthly_income = None
        else:
            new_monthly_income = float(new_monthly_income)

        accountmanager.edit_account(account_name, new_name, new_funds, new_monthly_income)
        print("Account successfully edited")
    except ValueError:
        print("Floats only")
        sys.exit(errno.EAGAIN)
    except exceptions.AccountEditingFailed as e:
        print(e)
        sys.exit(errno.EAGAIN)

elif arg == "category":
    account_name = input("Account name: ")
    cat_name = input("Category name: ")
    print("To leave any field unchanged, simply press enter.")
    new_name = input("New name: ")
    new_desc = input("New description: ")
    if new_name == '':
        new_name = None
    if new_desc == '':
        new_desc = None
    
    try:
        new_funds = input("New funds: $")
        if new_funds == '':
            new_funds = None
        else:
            new_funds = float(new_funds)

        new_budget = input("New budget: $")
        if new_budget == '':
            new_budget = None
        else:
            new_budget = float(new_budget)
        accountmanager.edit_category(account_name, cat_name, new_name, new_desc,
                                     new_funds, new_budget)
        print("Category successfully edited")
    except ValueError:
        print("Floats only")
        sys.exit(errno.EAGAIN)
    except exceptions.CategoryEditingFailed as e:
        print(e)
        sys.exit(errno.EAGAIN)

elif arg == "expenditure":
    account_name = input("Account name: ")
    exp_name = input("Expenditure name: ")
    print("To leave any field unchanged, simply press enter.")
    new_desc = input("New description: ")
    if new_desc = '':
        new_desc = None

    try:
        new_amount = input("New amount")
        if new_amount = '':
            new_amount = None
        else:
            new_amount = float(new_amount)
            
        accountmanager.edit_expenditure(account_name, exp_name, new_desc, new_amount)
        print("Expenditure successfully edited")
    except ValueError:
        print("Floats only")
        sys.exit(errno.EAGAIN)
    except exceptions.ExpEditingFailed as e:
        print(e)
        sys.exit(errno.EAGAIN)

else:
    print("Positional argument must be one of the following: 'account', 'category', 'expenditure'.")
    sys.exit(errno.EAGAIN)
