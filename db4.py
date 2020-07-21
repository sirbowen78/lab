from db2 import Students, engine, Course
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
db_session = Session()

results = db_session.query(Students).all()
for row in results:
    print(f"Lastname: {row.student_lastname}, Firstname: {row.student_firstname}, email: {row.student_email}")

courses = db_session.query(Course).all()
for row in courses:
    print(f"Course name: {row.course_name}")
