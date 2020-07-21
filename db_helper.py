from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


# Reference: https://www.tutorialspoint.com/sqlalchemy/index.htm

def db_engine(db_user="admin",
              db_pass="password",
              db_addr="127.0.0.1",
              db_name=None,
              db_dialect="mysql",
              db_driver="pymysql",
              verbose=False):
    """
    :param db_user: database username
    :param db_pass: database password
    :param db_addr: database address
    :param db_port: database port, default 3306
    :param db_name: database name
    :param db_dialect: database type such as mysql, postgresql, sqlite
    :param db_driver: database python module such as pymysql
    :param verbose: sqlalchemy logging output, default is False.
    :return: Engine object
    """
    url = f"{db_dialect}+{db_driver}://{db_user}:{db_pass}@{db_addr}/{db_name}"
    engine = create_engine(url, echo=verbose)
    if not database_exists(engine.url):
        create_database(engine.url)
    return engine
