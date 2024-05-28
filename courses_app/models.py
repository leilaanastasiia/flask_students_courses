from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from setup import ENGINE_SETUP

Base = declarative_base()
engine = create_engine(ENGINE_SETUP)

class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(6), unique=True)
    # parent table in one-to-many relationship
    students = relationship('Student', back_populates='group')

    def __repr__(self):
        return f'Group(id={self.id!r}, name={self.name!r})'


association_table = Table(
    'association_table',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('student.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('course.id'), primary_key=True))


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    # child table in one-to-many has a foreign key (many side)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=True)
    group = relationship('Group', back_populates='students')
    # many-to-many relationship
    courses = relationship('Course', secondary='association_table', back_populates='students')

    def __repr__(self):
        return f'Student(id={self.id!r}, first_name={self.first_name!r}', \
            f'last_name={self.last_name!r}, group_id={self.group_id!r})'


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String(500))
    # many-to-many relationship with bidirectional
    students = relationship('Student', secondary=association_table, back_populates='courses')

    def __repr__(self):
        return f'Course(id={self.id!r}, name={self.name!r}, description={self.description!r})'


def init_db():
    """Create all models"""
    Base.metadata.create_all(engine)

def get_session() -> object:
    """Create a session"""
    Session = sessionmaker(engine)
    session = Session()
    return session
