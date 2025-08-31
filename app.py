from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)



# # This code snippet is setting up a Flask application with a RESTful API using Flask-RestX extension.
# # Here's a breakdown of what each part of the code is doing:
# from flask import Flask, request, jsonify
# from flask_restx import Api, Resource, fields
# from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
# from dotenv import load_dotenv
# import os

# load_dotenv()


# app = Flask(__name__)
# app.config["MONGO_URI"] = os.getenv("MONGO_URI_CONNECTION")

# mongo = PyMongo(app)
# api = Api(app, doc='/swagger/')  

# school_model = api.model('School', {
#     'id': fields.Integer(required=True, description="School Id"),
#     'name': fields.String(required=True, description="School Name")
# })

# @api.route('/schools')
# class SchoolList(Resource):
#     @api.marshal_list_with(school_model)
#     def get(self):
#         schools = list(mongo.db.schools.find())
#         return schools

#     @api.expect(school_model)
#     def post(self):
#         data = api.payload
#         # Optional: prevent duplicate school ids
#         if mongo.db.schools.find_one({'id': data['id']}):
#             return {'error': 'School ID already exists'}, 400
#         result = mongo.db.schools.insert_one(data)
#         return {'message': 'School added', 'school_id': str(result.inserted_id)}, 201


# @api.route('/schools/<int:school_id>')
# class School(Resource):
#     @api.marshal_with(school_model)
#     def get(self, school_id):
#         school = mongo.db.schools.find_one({'id': school_id})
#         if school:
#             return school
#         return {'error': 'School not found'}, 404

#     @api.expect(school_model)
#     def put(self, school_id):
#         result = mongo.db.schools.update_one({'id': school_id}, {'$set': api.payload})
#         if result.matched_count == 0:
#             return {'error': 'School not found'}, 404
#         return {'message': 'School updated'}

#     def delete(self, school_id):
#         result = mongo.db.schools.delete_one({'id': school_id})
#         if result.deleted_count == 0:
#             return {'error': 'School not found'}, 404
#         return {'message': 'School deleted'}



# if __name__ == '__main__':
#     app.run(debug=True)