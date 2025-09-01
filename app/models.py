# Import necessary components from Flask-RESTX and the local app instance.
from flask_restx import fields
from app import api

# Defines the data model for a 'School'. 
# This model is used for API input validation and output marshaling.
school_model = api.model('School', {
    '_id': fields.String(readonly=True, description='The unique identifier from the database'),
    'id': fields.Integer(required=True, description='The school-specific unique identifier'),
    'name': fields.String(required=True, description='The name of the school')
})

# Defines the data model for a 'Staff' member. 
staff_model = api.model('Staff', {
    '_id': fields.String(readonly=True, description='The unique identifier from the database'),
    'name': fields.String(required=True, description='The name of the staff member'),
    'employeeId': fields.String(required=True, description='The unique employee ID'),
    'schoolId': fields.String(required=True, description='The ID of the school the staff belongs to')
})

# Defines the data model for a 'Review'. 
review_model = api.model('Review', {
    '_id': fields.String(readonly=True, description='The unique identifier from the database'),
    'text': fields.String(required=True, description='The content of the review'),
    'rating': fields.Integer(required=True, min=1, max=5, description='The rating given, from 1 to 5'),
    'date': fields.DateTime(required=True, description='The date the review was submitted'),
    'staffId': fields.String(required=True, description='The ID of the staff member being reviewed')
})