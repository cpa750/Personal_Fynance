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
    try:
        account_funds = float(input("Account funds: $"))
        account_monthly_income = float(input("Account monthly income: $"))
        accountmanager.add_account(account_name, account_funds, account_monthly_income)
        print("Account successfully added")
    except ValueError:
        print("Floats only")
        sys.exit(errno.EAGAIN)
    except exceptions.AccountCreationFailed as e:
        print(e)
        sys.exit(errno.EAGAIN)

elif arg == "category":
    account_name = input("Account name: ")
    cat_name = input("Category name: ")
    cat_desc = input("Category description: ")

    try:
        cat_budget = float(input("Category budget: $"))
        accountmanager.add_category(account_name, cat_name, cat_desc, cat_budget)
        print("Category successfully added")
    except ValueError:
        print("Floats only")
        sys.exit(errno.EAGAIN)
    except exceptions.CategoryCreationFailed as e:
        print(e)
        sys.exit(errno.EAGAIN)
    
elif arg == "expenditure":
    account_name = input("Account name: ")
    exp_name =  input("Expenditure name: ")
    exp_desc = input("Expenditure description: ")
    cat_name = input("Expenditure's category name (for no category press enter): ")

    try:
        exp_amount = float(input("Expenditure amount: $"))
        accountmanager.add_expenditure(account_name, cat_name, exp_name, exp_desc, exp_amount)
        print("Expenditure successfully added")
    except ValueError:
        print("Floats only")
        sys.exit(errno.EAGAIN)
    except exceptions.ExpCreationFailed as e:
        print(e)
        sys.exit(errno.EAGAIN)
    
else:
    print("Positional argument must be one of the following: 'account', 'category', 'expenditure'.")
    sys.exit(errno.EAGAIN)
