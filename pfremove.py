import errno
import sys

from fynance_core import accountmanager, exceptions

accountmanager.check_paydays()

try:
    arg = sys.argv[1].lower()
except IndexError:
    print("Positional argument must be one of the following: 'account', 'category', 'expenditures'.")
    sys.exit(errno.EAGAIN)

if arg == "account":
    account_name = input("Account name: ")
    confirm = input(f"Are you sure you want to delete account '{account_name}'? (y/n): ").lower()
    if confirm == 'y':
        try:
            accountmanager.remove_account(account_name)
            print("Account successfully removed")
        except exceptions.AccountRemovalFailed as e:
            print(e)
            sys.exit(errno.EAGAIN)
    else:
        print("Operation cancelled")

elif arg == "category":
    account_name = input("Account name: ")
    cat_name = input("Category name: ")
    confirm = input(f"Are you sure you want to delete category '{cat_name}'? (y/n): ").lower()
    if confirm == 'y':
        try:
            accountmanager.remove_category(account_name, cat_name)
            print("Category successfully removed")
        except exceptions.CategoryRemovalFailed as e:
            print(e)
            sys.exit(errno.EAGAIN)
    else:
        print("Operation cancelled")


elif arg == "expenditure":
    account_name = input("Account name: ")
    exp_name = input("Expenditure name: ")
    confirm = input(f"Are you sure you want to delete expenditure '{exp_name}'? (y/n): ").lower()
    if confirm == 'y':
        try:
            accountmanager.remove_expenditure(account_name, exp_name)
            print("Expenditure successfully removed")
        except exceptions.ExpRemovalFailed as e:
            print(e)
            sys.exit(errno.EAGAIN)
    else:
        print("Operation cancelled")

else:
    print("Positional argument must be one of the following: 'account', 'category', 'expenditure'.")
    sys.exit(errno.EAGAIN)
