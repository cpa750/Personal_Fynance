from fynance_core.utils import accountmanager
import os

from tabulate import tabulate

# Testing all the account-related API functions

# Testing that type checking works as expected
try:
    accountmanager.add_account(None, None, None)
    # Calling API with None, when params are not optional
except Exception as e:
    print(e)
accountmanager.add_account("Cian", 50.0, 100.0)
try:
    accountmanager.edit_account("Cian", 32, "foo", "bar")
    # Calling the API with the wrong types
except Exception as e:
    print(e)
accountmanager.remove_account("Cian")


print('\n')
print("Account-related functions\n")
accountmanager.add_account("Cian", 30.0, 50.0)
data, headers = accountmanager.view_account("Cian")
print(tabulate([data], headers))
print('\n')
accountmanager.edit_account("Cian", "John", 50.0, None)

try:
    data, headers = accountmanager.view_account("Cian")
    print(tabulate([data], headers))
except Exception as e:
    print(e)

print('\n')

data, headers = accountmanager.view_account("John")
print([data], headers)
print('\n')
accountmanager.edit_account("John", None, 30.0, 80.0)

try:
    accountmanager.edit_account("Cian", None, None, None)
except Exception as e:
    print(e)

print('\n')

data, headers = accountmanager.view_account("John")
print(tabulate([data], headers))
print('\n')
accountmanager.remove_account("John")

try:
    accountmanager.remove_account("Cian")
except Exception as e:
    print(e)

print('\n')

# Testing all category-related commands
print("Category-related functions\n")
accountmanager.add_account("Cian", 100.0, 300.0)
accountmanager.add_category("Cian", "Blah", "Random", 50.0)
data, headers1, exps, headers2 = accountmanager.view_category("Cian", "Blah")
print(tabulate([data], headers1))
print(tabulate(exps, headers2))
print('\n')
accountmanager.edit_category("Cian", "Blah", "Foo", "Bar", 40.0, 60.0)
data, headers1, exps, headers2 = accountmanager.view_category("Cian", "Foo")
print(tabulate([data], headers1))
print(tabulate(exps, headers2))
print('\n')

"""
There was no easy way to call a bunch of fucntions with params
And get each individual one's error messages with try/except,
Hence the hacky workaround
This block of code tests that raising exceptions works as expected.
"""
functions = (
    'accountmanager.view_category("John", "Blah")',
    'accountmanager.view_category("Cian", "asdf")',
    'accountmanager.edit_category("John", "Foo", None, None, None, None)',
    'accountmanager.edit_category("Cian", "asdf", None, None, None, None)',
    'accountmanager.remove_category("Cian", "asdf")',
    'accountmanager.remove_category("John", "Foo")',
)
for func in functions:
    try:
        eval(func)
    except Exception as e:
        print(e)

print('\n')
accountmanager.remove_category("Cian", "Foo")
accountmanager.remove_account("Cian")

# Testing all expenditure-related commands
print("Exp-related functions\n")
accountmanager.add_account("Cian", 50.0, 100.0)
accountmanager.add_category("Cian", "Foo", "Bar", 25.0)
accountmanager.add_expenditure("Cian", None, "Rand", "desc", 5.0)
exps, headers = accountmanager.view_expenditures("Cian")
print(tabulate(exps, headers))
print()
data, headers = accountmanager.view_account("Cian")
print(tabulate([data], headers))
print()
accountmanager.edit_expenditure("Cian", "Rand", "new desc", 6.0)
exps, headers = accountmanager.view_expenditures("Cian")
print(tabulate([data], headers))
print()
data, headers = accountmanager.view_account("Cian")
print(tabulate([data], headers))
print()
accountmanager.remove_expenditure("Cian", "Rand")
data, headers = accountmanager.view_account("Cian")
print(tabulate([data], headers))
print()

accountmanager.add_expenditure("Cian", "Foo", "Blah", "desc", 10.0)
exps, headers = accountmanager.view_expenditures("Cian")
print(tabulate(exps, headers))
print()
data, headers1, exps, headers2 = accountmanager.view_category("Cian", "Foo")
print(tabulate([data], headers1))
print(tabulate(exps, headers2))
print()
data, headers = accountmanager.view_account("Cian")
print(tabulate([data], headers))
print()
accountmanager.edit_expenditure("Cian", "Blah", None, 5.0)
exps, headers = accountmanager.view_expenditures("Cian")
print(tabulate(exps, headers))
print()
data, headers1, exps, headers2 = accountmanager.view_category("Cian", "Foo")
print(tabulate([data], headers1))
print(tabulate(exps, headers2))
print()
data, headers = accountmanager.view_account("Cian")
print(tabulate([data], headers))
accountmanager.remove_category("Cian", "Foo")
data, headers = accountmanager.view_account("Cian")
print(tabulate([data], headers))
print()
exps, headers = accountmanager.view_expenditures("Cian")
print(tabulate(exps, headers))
print()
accountmanager.remove_expenditure("Cian", "Blah")
data, headers = accountmanager.view_account("Cian")
print(tabulate([data], headers))
print()
exps, headers = accountmanager.view_expenditures("Cian")
print(tabulate(exps, headers))

os.remove("accounts")
