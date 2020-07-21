from models import Course, Student
from db_test import engine
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)
session = Session()

session.add_all(
    [
        Student(firstname="Cyrus", lastname="Lok", email="cyruslab@test.local"),
        Student(firstname="Yew Mun", lastname="Lok", email="student@test.local"),
        Course(name="Mathematics", sid=1),
        Course(name="Science"),
        Course(name="Business Management"),
        Course(name="Cyber Security"),
        Course(name="Python", sid=2)
    ]
)
session.commit()
