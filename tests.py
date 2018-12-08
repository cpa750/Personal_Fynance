from fynance_core.utils import accountmanager
import os

# Testing all the account-related API functions
print("Account-related functions\n")
accountmanager.add_account("Cian", 30.0, 50.0)
accountmanager.view_account("Cian")
print('\n')
accountmanager.edit_account("Cian", "John", 50.0, None)

try:
    accountmanager.view_account("Cian")
except Exception as e:
    print(e)

print('\n')

accountmanager.view_account("John")
print('\n')
accountmanager.edit_account("John", None, 30.0, 80.0)

try:
    accountmanager.edit_account("Cian", None, None, None)
except Exception as e:
    print(e)

print('\n')

accountmanager.view_account("John")
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
accountmanager.view_category("Cian", "Blah")
print('\n')
accountmanager.edit_category("Cian", "Blah", "Foo", "Bar", 40.0, 60.0)
accountmanager.view_category("Cian", "Foo")
print('\n')

# There was no easy way to call a bunch of fucntions with params
# And get each individual one's error messages with try/except,
# Hence the hacky workaround
# This is to test that raising errors works as expected.
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
accountmanager.view_expenditures("Cian")
print()
accountmanager.view_account("Cian")
print()
accountmanager.edit_expenditure("Cian", "Rand", "new desc", 6.0)
accountmanager.view_expenditures("Cian")
print()
accountmanager.view_account("Cian")
print()
accountmanager.remove_expenditure("Cian", "Rand")
accountmanager.view_account("Cian")
print()

accountmanager.add_expenditure("Cian", "Foo", "Blah", "desc", 10.0)
accountmanager.view_expenditures("Cian")
print()
accountmanager.view_category("Cian", "Foo")
print()
accountmanager.view_account("Cian")
print()
accountmanager.edit_expenditure("Cian", "Blah", None, 5.0)
accountmanager.view_expenditures("Cian")
print()
accountmanager.view_category("Cian", "Foo")
print()
accountmanager.view_account("Cian")
accountmanager.remove_category("Cian", "Foo")
accountmanager.view_account("Cian")
print()
accountmanager.view_expenditures("Cian")
print()
accountmanager.remove_expenditure("Cian", "Blah")
accountmanager.view_account("Cian")
print()
accountmanager.view_expenditures("Cian")

os.remove("accounts")
