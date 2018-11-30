import shelve

from tabulate import tabulate

from . import account, category, exceptions, expenditure, helpers

# TODO: Remember to validate user input in the CLI!!

def add_account(name, funds, monthly_income):
    try:
        acct = account.Account(name, funds, monthly_income)
        with shelve.open("accounts", 'c') as shelf:
            shelf[acct.name] = acct
    except Exception as e:
        raise exceptions.AccountCreationFailed(f"Account creation failed due to error {e}")

def remove_account(account_name):
    try:
        with shelve.open("accounts", 'c') as shelf:
            del shelf[account_name]
    except Exception as e:
        raise exceptions.AccountRemovalFailed(f"Account removal failed due to error {e}")

def edit_account(acct_name, new_name, new_funds, new_monthly_income):
    try:
        acct = helpers.get_account(acct_name)
    except KeyError:
        raise exceptions.AccountEditingFailed("Account editing failed: account does not exist.")
    
    if new_name != None:
        acct.name = new_name
    if new_funds != None:
        acct.funds = new_funds
    if new_monthly_income != None:
        acct.monthly_income = new_monthly_income
    
    acct.sync()

def view_account(account_name):
    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.AccountViewingFailed("Account viewing failed: account does not exist.")
    
    print(tabulate([[acct.name, acct.funds, acct.monthly_income]],
                   headers=["Name", "Funds ($)", "Monthly Income ($)"]))

def create_category(account_name, cat_name, desc, budget):
    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.CategoryCreationFailed("Category creation failed: account does not exist.")
    
    cat = category.Category(acct, cat_name, desc, budget)
    acct.categories[cat.name] = cat

    acct.sync()

def remove_category(account_name, cat_name):
    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.CategoryRemovalFailed("Category removal failed: account does not exist.")

    try:
        cat = helpers.get_category(acct, cat_name)
    except KeyError:
        raise exceptions.CategoryRemovalFailed("Category removal failed: category does not exist.")

    for exp in cat.expenditures:
        exp.category = None
    
    del acct.categories[cat_name]
    
    acct.sync()

def edit_category(account_name, cat_name, new_name, new_desc, new_funds, new_budget):
    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.CategoryEditingFailed("Category editing failed: account does not exist.")
    
    try:
        cat = helpers.get_category(acct, cat_name)
    except KeyError:
        raise exceptions.CategoryEditingFailed("Category editing failed: category does not exist.")
    
    if new_name != None:
        cat.name = new_name
    if new_desc != None:
        cat.name = new_desc
    if new_funds != None:
        cat.funds = new_funds
    if new_budget != None:
        cat.budget = new_budget
    
    acct.sync()

def view_category(account_name, cat_name):
    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.CategoryViewingFailed("Category viewing faild: account does not exist.")

    try:
        cat = helpers.get_category(acct, cat_name)
    except KeyError:
        raise exceptions.CategoryViewingFailed("Category viewing failed: category does not exist.")
    
    print(tabulate([[cat.name, cat.desc, cat.funds, cat.budget]],
                   headers=["Name", "Desc.", "Funds ($)", "Budget ($)"]))
    
    print("Category Expenditures")
    exps = [[exp.name, exp.desc, exp.amount] for exp in cat.expenditures]
    print(tabulate(exps, headers=["Name", "Desc.", "Amount ($)"]))

def add_expenditure(account_name, cat_name, name, desc, amount):
    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.ExpCreationFailed("Expenditure creation failed: account does not exist.")

    if cat_name != '':
        try:
            cat = helpers.get_category(acct, cat_name)
        except KeyError:
            raise exceptions.ExpCreationFailed("Expenditure creation failed: category does not exist.")
    else:
        cat = None

    exp = expenditure.Expenditure(name, desc, amount, cat)
    acct.expenditures[name] = exp
    acct.funds -= exp.amount
    if exp.category != None:
        exp.category.funds -= exp.amount
        exp.category.expenditures[exp.name] = exp

    acct.sync()

def remove_expenditure(account_name, expenditure_name):
    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.ExpRemovalFailed("Expenditure removal failed: account does not exist.")

    try:
        exp = helpers.get_expenditure(acct, expenditure_name)
        del acct.expenditures[expenditure_name]
    except KeyError:
        raise exceptions.ExpRemovalFailed("Expenditure removal failed: expenditure does not exist.")

    acct.funds += exp.amount
    if exp.category != None:
        exp.category.funds += exp.amount
        del exp.category.expenditures[exp.name]

    acct.sync()

def edit_expenditure(account_name, exp_name, new_desc, new_amount):
    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.ExpEditingFailed("Expenditure editing failed: account does not exist.")

    try:
        exp = helpers.get_expenditure(acct, exp_name)
    except KeyError:
        raise exceptions.ExpEditingFailed("Expenditure editing failed: expenditure does not exist.")
    
    if new_desc != None:
        exp.desc = new_desc
    if new_amount != None:
        difference = new_amount - exp.amount
        exp.amount = new_amount
    if exp.category != None:
        exp.category.funds -= difference
    acct.funds -= difference
    acct.sync()

def view_expenditure(account_name):
    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.ExpViewingFailed("Expenditure viewing failed: account does not exist.")

    exps = [[exp.name, exp.desc, exp.amount, exp.category.name] for exp in acct.expenditures]
    print(tabulate(exps, headers=["Name", "Desc.", "Amount ($)", "Category"]))

def check_paydays():
    with shelve.open("accounts", 'c') as shelf:
        for account in shelf:
            shelf[account].check_for_pay_day()
