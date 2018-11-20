#SuSi - SUper SImple Migration Skript

from belavoco_server.models import User
from playhouse.migrate import *
from peewee import *
from belavoco_server.models import database


migrator = SqliteMigrator(database)
    

def susi_add_column(model_and_field):

    table_name = model_and_field.model._meta.table_name
    try:
        migrate(
            migrator.add_column(table_name, model_and_field.column_name, model_and_field.model._meta.fields[model_and_field.column_name])
        )
    
    except Exception as e: 
        print(e)

def migration_201118():
    susi_add_column(User.app_version)
    pass

if __name__ == '__main__':
    migration_201118()
    
    