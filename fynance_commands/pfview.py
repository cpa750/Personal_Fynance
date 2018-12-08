import errno
import sys

from fynance_core.utils import accountmanager, exceptions

from tabulate import tabulate

accountmanager.check_paydays()

try:
    arg = sys.argv[1].lower()
except IndexError:
    print("Positional argument must be one of the following: 'account', 'category', 'expenditures'.")
    sys.exit(errno.EAGAIN)

if arg == "account":
    account_name = input("Account name: ")
    
    try:
        data, headers = accountmanager.view_account(account_name)
        print(tabulate([data], headers))
    except exceptions.AccountViewingFailed as e:
        print(e)
        sys.exit(errno.EAGAIN)

elif arg == "category":
    account_name = input("Account name: ")
    cat_name = input("Category name: ")

    try:
        data, headers, exps, headers2 = accountmanager.view_category(account_name, cat_name)
        print(tabulate([data], headers))
        print()
        print(tabulate(exps, headers2))
    except exceptions.CategoryViewingFailed as e:
        print(e)
        sys.exit(errno.EAGAIN)

elif arg == "expenditures":
    account_name = input("Account name: ")

    try:
        exps, headers = accountmanager.view_expenditures(account_name)
        print(tabulate(exps, headers))
    except exceptions.ExpViewingFailed as e:
        print(e)
        sys.exit(errno.EAGAIN)

else:
    print("Positional argument must be one of the following: 'account', 'category', 'expenditures'.")
    sys.exit(errno.EAGAIN)
