# This code snippet is setting up a Flask application with a RESTful API using Flask-RestX extension.
# Here's a breakdown of what each part of the code is doing:
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI_CONNECTION")

mongo = PyMongo(app)
api = Api(app, doc='/swagger/')  

school_model = api.model('School', {
    'id': fields.String(required=True, description="School Id"),
    'name': fields.String(required=True, description="School Name")
})

@api.route('/schools')
class SchoolList(Resource):
    @api.marshal_list_with(school_model)
    def get(self):
        schools = list(mongo.db.schools.find())
        for school in schools:
            school['id'] = str(school.get('id',school['_id']))
        return schools

    @api.expect(school_model)
    def post(self):
        data = api.payload
        result = mongo.db.schools.insert_one(data)
        return {'message': 'School added', 'school_id': str(result.inserted_id)}, 201

@api.route('/schools/<string:school_id>')
class User(Resource):
    @api.marshal_with(school_model)
    def get(self, school_id):
        school = mongo.db.schools.find_one({'_id': ObjectId(school_id)})
        if school:
            school['id'] = str(school.get('id',school['_id']))
            return school
        return {'error': 'School not found'}, 404

    @api.expect(school_model)
    def put(self, school_id):
        mongo.db.schools.update_one({'_id': ObjectId(school_id)}, {'$set': api.payload})
        return {'message': 'School updated'}

    def delete(self, school_id):
        mongo.db.schools.delete_one({'_id': ObjectId(school_id)})
        return {'message': 'School deleted'}


if __name__ == '__main__':
    app.run(debug=True)