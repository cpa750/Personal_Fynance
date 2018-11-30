from fynance_core import accountmanager
import os

# Testing all the account-related API functions
accountmanager.add_account("Cian", 30, 50)
accountmanager.view_account("Cian")
print('\n')
accountmanager.edit_account("Cian", "John", 50, None)

try:
    accountmanager.view_account("Cian")
except Exception as e:
    print(e)

print('\n')

accountmanager.view_account("John")
print('\n')
accountmanager.edit_account("John", None, 30, 80)

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
accountmanager.add_account("Cian", 100, 300)
accountmanager.add_category("Cian", "Blah", "Random", 50)
accountmanager.view_category("Cian", "Blah")
print('\n')
accountmanager.edit_category("Cian", "Blah", "Foo", "Bar", 40, 60)
accountmanager.view_category("Cian", "Foo")
print('\n')

# There was no easy way to call a bunch of fucntions with params
# And get each individual one's error messages with try/except,
# Hence the hacky workaround
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


os.remove("accounts")
