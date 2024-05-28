# Students' courses Flask REST API
___

Easy to use example project of CRUDing data of students' info and courses. 

Stack: `Flask`, `flask_restful`, `PostgreSQL`, `SQLAlchemy`, `pytest`, `coverage`

Features:

- GET:
   - `courses/`: all courses with the description and students' list 
   - `groups/?students_count=20`: all groups with an optional filter of students' count in it 
   - `students/?course_name=Biology`: list of all students with an optional filter of course name
- POST:
   - add a new student
   - add a new student to the course
- DELETE:
  - delete a student by STUDENT_ID
  - remove the student from one of his/her courses 

__The database should be created and populated before use__ (an example of data is in the setup.py file).

The predefined logic of the database population is to create 
- 10 groups with a random amount of students;
- 10 different courses:
- 200 students randomly assigned for 1-3 courses.

Covered with pytest.