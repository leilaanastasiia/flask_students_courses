from flask import make_response, request, jsonify
from flask_restful import Resource
from sqlalchemy import select, func

from courses_app.models import get_session, Group, Student


class Groups(Resource):
    headers = {'content-type': 'application/json'}

    def get(self):
        """Find all groups with less or equals student count"""
        students_count_param = request.args.get('students_count')
        with get_session() as session:
            subquery = (
                select(Group.id, Group.name, func.count(Student.group_id).label('number_of_students'))
                .join(Student, Student.group_id == Group.id)
                .group_by(Group.id, Group.name)
                .order_by(Group.id))
            data = session.execute(subquery).all()
            if students_count_param:
                students_count = [number.number_of_students for number in data]
                if int(students_count_param) >= min(students_count):
                    data = session.execute(subquery
                                            .having(func.count(Student.group_id) <= students_count_param)
                                            ).all()
                elif int(students_count_param) < min(students_count):
                    resp = {'response': "Enter a bigger student's count number"}
                    return make_response(jsonify(resp), 200, self.headers)
            resp = []
            for item in data:
                resp.append({
                    'id': item.id,
                    'name': item.name,
                    'number_of_students': item.number_of_students
                })
            return make_response(jsonify(resp), 200, self.headers)
