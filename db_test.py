from db_helper import db_engine
from getpass import getpass
from models import Base

# Get database address.
db_addr = input("DB ip address: ")
# Get username of the database.
db_user = input(f"Username of {db_addr}: ")
# Get password.
db_pass = getpass(f"Password of {db_user}@{db_addr}: ")
# Get the database name.
db_name = input("Database name to connect: ")

db_config = {
    "db_addr": db_addr,
    "db_user": db_user,
    "db_pass": db_pass,
    "db_name": db_name,
    "verbose": True
}

engine = db_engine(**db_config)


Base.metadata.create_all(engine)
