from fynance_core import accountmanager, exceptions
import sys
import errno

if sys.argv[1] == "account":
    account_name = input("Account name: ")
    try:
        account_funds = int(input("Account funds: $"))
        account_monthly_income = int(input("Account monthly income: $"))
        accountmanager.add_account(account_name, account_funds, account_monthly_income)
    except ValueError:
        print("Integers only")
        sys.exit(errno.EAGAIN)
    except exceptions.AccountCreationFailed as e:
        print(e)
