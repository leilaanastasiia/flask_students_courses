import random
import psycopg2
from sqlalchemy import select

from .models import Group, Student, Course, get_session
from setup import GROUP_LIST, COURSES_DICT, FIRST_NAMES_LIST, LAST_NAMES_LIST


def create_groups() -> None:
    """Populate groups model with required data"""
    groups_list = GROUP_LIST
    with get_session() as session:
        for abbreviation in groups_list:
            one_group = Group(name=abbreviation)
            session.add(one_group)
        session.commit()

def create_courses() -> None:
    """Populate courses model with required data"""
    courses_dict = COURSES_DICT
    with get_session() as session:
        for course  in courses_dict:
            one_course = Course(name=course, description=courses_dict[course])
            session.add(one_course)
        session.commit()

def create_students() -> None:
    """Populate students model with required data"""
    for name in range(200):
        add_first_name = random.choice(FIRST_NAMES_LIST)
        add_last_name = random.choice(LAST_NAMES_LIST)
        with get_session() as session:
            select_group = session.execute(
                select(Group)
                .where(Group.id == random.randint(1, 10))
            ).scalar_one()
            student = Student(first_name=add_first_name, last_name=add_last_name, group_id=select_group.id)
            courses_amount = random.randint(1, 3)
            for course_amount in range(courses_amount):
                while True:  # keep searching an appropriate group id
                    try:
                        select_course = session.execute(
                        select(Course)
                        .where(Course.id == random.randint(1, 10))
                    ).scalar_one()
                        student.courses.append(select_course)
                        session.add(student)
                        session.commit()
                    except psycopg2.errors.UniqueViolation:
                        continue  # try again if pair has already exist
                    break  # go for a next course or student


def populate_db():
    """Add all initial data"""
    create_courses()
    create_groups()
    create_students()
