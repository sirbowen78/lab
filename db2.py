from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, create_engine, String
from sqlalchemy_utils import database_exists, create_database

url = "mysql+pymysql://username:password@192.168.1.254/test"
engine = create_engine(url, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)

base = declarative_base()


class Students(base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True)
    student_firstname = Column(String(255), nullable=False)
    student_lastname = Column(String(255), nullable=False)
    student_address = Column(String(255))
    student_email = Column(String(255), nullable=False)


class Course(base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(255), nullable=False)
    lecturer_id = Column(Integer)


base.metadata.create_all(engine)
