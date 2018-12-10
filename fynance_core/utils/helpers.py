import shelve

def get_account(account_name):
    """Getting and returning a specific account object. Must handle KeyError in API"""
    with shelve.open("accounts", 'c') as shelf:
        account = shelf[account_name]
        return account

def get_category(account, category_name):
    """Getting and returning a specific category. Must handle KeyError in API"""
    category = account.categories[category_name]
    return category

def get_expenditure(account, expenditure_name):
    """Getting and returning a specific exp. Must handle KeyEorror in API."""
    expenditure = account.expenditures[expenditure_name]
    return expenditure

def check_param_types(*args):
    """
    Checking the types of params passed in an API function
    are what they are expected to be. Args are an arbitrary
    number of tuples in the form (param, expected_type [, optional])
    Optional specifies whether a param can be None or not.
    """
    for arg in args:
        param = arg[0]
        expected_type = arg[1]
        
        if len(arg) == 3:
            optional = arg[2]
        else:
            optional = False

        if optional:
            compound = type(param) == expected_type or param == None
            if compound:
                continue
            else:
                return False

        else:
            type_is_expected = type(param) == expected_type
            if type_is_expected:
                continue
            else:
                return False

    return True
