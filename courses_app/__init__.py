from flask import Flask
from flask_restful import Api

from courses_app.models import init_db
from courses_app.populating_db import populate_db
from courses_app.resources.courses import Courses
from courses_app.resources.groups import Groups
from courses_app.resources.index import Index
from courses_app.resources.students import Students

app = Flask(__name__)
api = Api(app, default_mediatype='application/json')
PREFIX1 = '/api/v1'

api.add_resource(Index, '/')
api.add_resource(Groups, PREFIX1 + '/groups/')
api.add_resource(Students, PREFIX1 + '/students/')
api.add_resource(Courses, PREFIX1 + '/courses/')

# init_db()
# populate_db()

if __name__ == '__main__':
    app.run(debug=True)
