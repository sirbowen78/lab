from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    sid = Column(Integer, primary_key=True)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    description = Column(String(2048))
    course = relationship("Course", back_populates="student")


class Course(Base):
    __tablename__ = "courses"
    cid = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    sid = Column(Integer, ForeignKey("students.sid"))
    student = relationship("Student", back_populates="course")
