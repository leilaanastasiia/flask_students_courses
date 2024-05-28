from courses_app.models import Group, Student, Course


########################################################################
'''TEST MODELS'''
########################################################################

def test_new_group():
    """
    GIVEN a Group model
    WHEN a new Group is created
    THEN check the name field are defined correctly
    """
    group = Group(name='AA__01')
    assert group.name == 'AA__01'


def test_new_student():
    """
    GIVEN a Student model
    WHEN a new Student is created
    THEN check the first_name, last_name, group_id fields are defined correctly
    """
    student = Student(first_name='Mia', last_name='Pip', group_id=5)
    assert student.first_name == 'Mia'
    assert student.last_name == 'Pip'
    assert student.group_id == 5


def test_new_course():
    """
    GIVEN a Course model
    WHEN a new Course is created
    THEN check the name and description field are defined correctly
    """
    course = Course(name='Mathematics', description='The science and study of quality, structure, space, and change')
    assert course.name == 'Mathematics'
    assert course.description == 'The science and study of quality, structure, space, and change'



def test_new_association_table():
    """
    GIVEN Student & Course models
    WHEN a new association is created between student and course
    THEN check the relationship is defined correctly
    """
    student = Student(first_name='Mia', last_name='Pip', group_id=5)
    course = Course(name='Mathematics', description='The science and study of quality, structure, space, and change')
    student.courses.append(course)
    assert student.courses[0].name == 'Mathematics'
    assert course.students[0].first_name == 'Mia'
