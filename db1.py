from sqlalchemy import (create_engine,
                        Table, Column, Integer, String,
                        MetaData)
from sqlalchemy_utils import database_exists, create_database
from getpass import getpass

"""
database url is dialect+driver://username:password@db_address/db_name
To connect to mysql/mariadb, pymysql module is required to install.
The purpose of using SqlAlchemy is to abstract sql syntax from the programmer/scripter,
hence there should be no sql syntax used, to use sql syntax use the execute method of the create_engine object.
"""

# Get database address.
db_addr = input("DB ip address: ")
# Get username of the database.
db_user = input(f"Username of {db_addr}: ")
# Get password.
db_pass = getpass(f"Password of {db_user}@{db_addr}: ")
# Get the database name.
db_name = input("Database name to connect: ")

# join the inputs into a complete database url.
url = f"mysql+pymysql://{db_user}:{db_pass}@{db_addr}/{db_name}"

# Create an engine object.
engine = create_engine(url, echo=True)

# Create database if it does not exist.
if not database_exists(engine.url):
    create_database(engine.url)
else:
    # Connect to database if exists, returns connection object.
    conn = engine.connect()

    # create a metadata object for table.
    # This allows multiple tables to be created with metadata.
    meta = MetaData()

    """
    Define the table. The below is the same as
    CREATE TABLE test_table (
        id INTEGER NOT NULL AUTO_INCREMENT,
        name VARCHAR(255),
        PRIMARY KEY (id)
    )
    """
    # First table
    test_table = Table(
        "test_table", meta,
        Column("id", Integer, primary_key=True),
        Column("name", String(255))  # MySql VARCHAR requires a defined length.
    )

    # Second table
    mac_address_table = Table(
        "mac_address_table", meta,
        Column("id", Integer, primary_key=True),
        Column("device", String(255)),
        Column("mac_address", String(100))
    )

    # Third table
    test_table2 = Table(
        "test_table2", meta,
        Column("id", Integer, primary_key=True),
        Column("firstName", String(255)),
        Column("lastName", String(255))
    )

    # This commits the table to database.
    meta.create_all(engine)
    conn.execute(test_table2.insert(), [
        {
            "firstName": "Cyrus",
            "lastName": "Lok"
        },
        {
            "firstName": "Yew Mun",
            "lastName": "Lok"
        },
        {
            "firstName": "Baoli",
            "lastName": "Sun"
        }
    ])
    result = conn.execute(test_table2.select().where(test_table2.c.id == 1))
    for row in result:
        print(row)
