from fynance_core import accountmanager

accountmanager.add_account("Cian", 30, 50)
accountmanager.view_account("Cian")
accountmanager.edit_account("Cian", "John", 50, None)
accountmanager.view_account("Cian")
accountmanager.view_account("John")
