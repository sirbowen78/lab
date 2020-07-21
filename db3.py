from db2 import Students, Course, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
db_session = Session()

cyruslok = Students(student_firstname="Cyrus",
                    student_lastname="Lok",
                    student_email="cyruslab@local")

j_smith = Students(student_firstname="Jackie",
                   student_lastname="Smith",
                   student_email="j.smith@test.local")

g_gold = Students(student_firstname="Gerald",
                  student_lastname="Gold",
                  student_email="g.gold@test.local")

mathematics = Course(course_name="Mathematics", lecturer_id=1)
science = Course(course_name="Science", lecturer_id=2)

db_session.add_all(
    [cyruslok, j_smith, g_gold, mathematics, science]
)
db_session.commit()