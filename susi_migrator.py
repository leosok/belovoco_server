#SuSi - SUper SImple Migration Skript

from belavoco_server.models import User, Audiofile, Audio_not_allowed
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

def un_allow_all_for_fu():
    fu_user = User.select().where( User.user_email == 'pitch@fu-berlin.de' ).get()
    for a in Audiofile.select(Audiofile):
        Audio_not_allowed.create(user=fu_user,
                                audiofile=a)
    print "populated with denial"


if __name__ == '__main__':
    #migration_201118()
    un_allow_all_for_fu()
    