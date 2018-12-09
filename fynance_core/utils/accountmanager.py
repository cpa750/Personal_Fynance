import shelve

from . import exceptions, helpers
from ..datamodels import account, category, expenditure


def add_account(name: str, funds: float, monthly_income: float):
    typesafe = helpers.check_param_types((name, str), (funds, float), (monthly_income, float))
    if not typesafe:
        raise exceptions.AccountCreationFailed("API call not typesafe. If you're seeing this as a user, contact the developer.")

    acct = account.Account(name, funds, monthly_income)
    acct.sync()

def remove_account(account_name: str):
    typesafe = helpers.check_param_types((account_name, str))
    if not typesafe:
        raise exceptions.AccountRemovalFailed("API call not typesafe. If you're seeing this as a user, contact the developer.")

    try:
        with shelve.open("accounts", 'c') as shelf:
            del shelf[account_name]
    except KeyError:
        raise exceptions.AccountRemovalFailed("Account removal failed: account does not exist.")

def edit_account(acct_name: str, new_name: str, new_funds: float, new_monthly_income: float):
    """Passing any new_* params as None will leave the attribute as-is."""
    typesafe = helpers.check_param_types((acct_name, str), (new_name, str, True), (new_funds, float, True),
                                         (new_monthly_income, float, True))
    if not typesafe:
        raise exceptions.AccountEditingFailed("API call not typesafe. If you're seeing this as a user, contact the developer.")

    try:
        acct = helpers.get_account(acct_name)
    except KeyError:
        raise exceptions.AccountEditingFailed("Account editing failed: account does not exist.")
    
    if new_name != None:
        with shelve.open("accounts", 'c') as shelf:
            del shelf[acct.name]
            # Must delete old key associated with account
        acct.name = new_name
    if new_funds != None:
        acct.funds = new_funds
    if new_monthly_income != None:
        acct.monthly_income = new_monthly_income
    
    acct.sync()

def view_account(account_name: str):
    typesafe = helpers.check_param_types((account_name, str))
    if not typesafe:
        raise exceptions.AccountViewingFailed("API call not typesafe. If you're seeing this as a user, contact the developer.")

    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.AccountViewingFailed("Account viewing failed: account does not exist.")

    return ([acct.name, acct.funds, acct.monthly_income, acct.last_pay_day, acct.next_pay_day],
            ["Name", "Funds ($)", "Monthly Income ($)", "Last Pay Date", "Next Pay Date"])

def add_category(account_name: str, cat_name: str, desc: str, budget: float):
    typesafe = helpers.check_param_types((account_name, str), (cat_name, str), (desc, str),
                                         (budget, float))
    if not typesafe:
        raise exceptions.CategoryCreationFailed("API call not typesafe. If you're seeing this as a user, contact the developer.")

    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.CategoryCreationFailed("Category creation failed: account does not exist.")
    
    cat = category.Category(acct, cat_name, desc, budget)
    acct.categories[cat.name] = cat

    acct.sync()

def remove_category(account_name: str, cat_name: str):
    typesafe = helpers.check_param_types((account_name, str), (cat_name, str))
    if not typesafe:
        raise exceptions.CategoryRemovalFailed("API call not typesafe. If you're seeing this as a user, contact the developer.")

    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.CategoryRemovalFailed("Category removal failed: account does not exist.")

    try:
        cat = helpers.get_category(acct, cat_name)
    except KeyError:
        raise exceptions.CategoryRemovalFailed("Category removal failed: category does not exist.")

    for exp in cat.expenditures:
        exp = cat.expenditures[exp]
        exp.category = None
    
    del acct.categories[cat_name]
    
    acct.sync()

def edit_category(account_name: str, cat_name: str, new_name: str,
                  new_desc: str, new_funds: float, new_budget: float):
    """Passing any new_* params as None will leave the attribute as-is."""
    tpyesafe = helpers.check_param_types((account_name, str), (cat_name, str), (new_name, str, True),
                                         (new_desc, str, True), (new_funds, float, True),
                                         (new_budget, float, True))
    if not tpyesafe:
        raise exceptions.CategoryEditingFailed("API call not typesafe. If you're seeing this as a user, contact the developer.")

    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.CategoryEditingFailed("Category editing failed: account does not exist.")
    
    try:
        cat = helpers.get_category(acct, cat_name)
    except KeyError:
        raise exceptions.CategoryEditingFailed("Category editing failed: category does not exist.")
    
    if new_name != None:
        del acct.categories[cat.name]
        cat.name = new_name
        acct.categories[cat.name] = cat
        # Must delete old key, and save new one when name is changed
    if new_desc != None:
        cat.desc = new_desc
    if new_funds != None:
        cat.funds = new_funds
    if new_budget != None:
        cat.budget = new_budget
    
    acct.sync()

def view_category(account_name: str, cat_name: str):
    typesafe = helpers.check_param_types((account_name, str), (cat_name, str))
    if not typesafe:
        raise exceptions.CategoryViewingFailed("API call not typesafe. If you're seeing this as a user, contact the developer.") 

    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.CategoryViewingFailed("Category viewing failed: account does not exist.")

    try:
        cat = helpers.get_category(acct, cat_name)
    except KeyError:
        raise exceptions.CategoryViewingFailed("Category viewing failed: category does not exist.")
        
    exps = []
    for exp_name in acct.expenditures:
        exp = acct.expenditures[exp_name]
        exps.append([exp.name, exp.desc, exp.amount])

    return ([cat.name, cat.desc, cat.funds, cat.budget],
            ["Name", "Desc.", "Funds ($)", "Budget ($)"],
            exps, ["Name", "Desc.", "Amount ($)"])

def add_expenditure(account_name: str, cat_name: str, name: str,
                    desc: str, amount: float):
    """Passing in the cat_name as None will add the exp. with no category."""
    typesafe = helpers.check_param_types((account_name, str), (cat_name, str, True),
                                         (name, str), (desc, str), (amount, float))
    if not typesafe:
        raise exceptions.ExpCreationFailed("API call not typesafe. If you're seeing this as a user, contact the developer.")

    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.ExpCreationFailed("Expenditure creation failed: account does not exist.")

    if cat_name != None:
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

def remove_expenditure(account_name: str, expenditure_name: str):
    typesafe = helpers.check_param_types((account_name, str), (expenditure_name, str))
    if not typesafe:
        raise exceptions.ExpRemovalFailed("API call not typesafe. If you're seeing this as a user, contact the developer.")

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

def edit_expenditure(account_name: str, exp_name: str, new_desc: str, new_amount: float):
    """Passing any new_* params as None will leave the attribute as-is."""
    typesafe = helpers.check_param_types((account_name, str), (exp_name, str), (new_desc, str, True),
                                         (new_amount, float, True))
    if not typesafe:
        raise exceptions.ExpEditingFailed("API call not typesafe. If you're seeing this as a user, contact the developer.")

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
        acct.funds -= difference
        if exp.category != None:
            exp.category.funds -= difference
    acct.sync()

def view_expenditures(account_name: str):
    typesafe = helpers.check_param_types((account_name, str))
    if not typesafe:
        raise exceptions.ExpViewingFailed("API call not typesafe. If you're seeing this as a user, contact the developer.")

    try:
        acct = helpers.get_account(account_name)
    except KeyError:
        raise exceptions.ExpViewingFailed("Expenditure viewing failed: account does not exist.")

    exps = []
    for exp_name in acct.expenditures:
        exp = acct.expenditures[exp_name]
        if exp.category != None:
            exps.append([exp.name, exp.desc, exp.amount, exp.category.name])
        else:
            exps.append([exp.name, exp.desc, exp.amount, ''])

    return (exps, ["Name", "Desc.", "Amount ($)", "Category"])

def check_paydays():
    with shelve.open("accounts", 'c') as shelf:
        for account in shelf:
            shelf[account].check_for_pay_day()
