# Import necessary components from Flask-RESTX and the local application.
from flask_restx import Resource
from app import mongo
from app.models import school_model, staff_model

def register_routes(api):
    """
    Registers all the school-related API routes.

    This function groups the endpoints for schools and attaches them to the
    main Flask-RESTX Api instance.

    :param api: The main Flask-RESTX Api instance.
    """

    # Defines the resource for the collection of schools (e.g., /schools).
    @api.route('/schools')
    class SchoolList(Resource):
        
        # Decorator to format the list of schools in the response using the school_model.
        @api.marshal_list_with(school_model)
        def get(self):
            """Get all schools"""
            # Fetches all documents from the 'schools' collection in MongoDB.
            return list(mongo.db.schools.find())

        # Decorator to specify the expected input format for Swagger UI.
        @api.expect(school_model)
        def post(self):
            """Create a new school"""
            # 'api.payload' contains the parsed JSON data from the request body.
            data = api.payload

            # --- Input Validation ---
            # Ensure the user-provided 'id' is a valid integer.
            try:
                data['id'] = int(data['id'])
            except (TypeError, ValueError):
                return {'error': 'School id must be an integer'}, 400

            # Check if a school with this numeric 'id' already exists to prevent duplicates.
            if mongo.db.schools.find_one({'id': data['id']}):
                return {'error': 'School ID already exists'}, 400

            # Insert the validated data into the 'schools' collection.
            result = mongo.db.schools.insert_one(data)
            
            # Return a success message with the new MongoDB document ID (_id) and a 201 Created status.
            return {'message': 'School added', 'school_id': str(result.inserted_id)}, 201

    # Defines the resource for a single school, identified by its numeric ID.
    @api.route('/schools/<int:school_id>')
    class School(Resource):
        
        # Decorator to format the single school object in the response.
        @api.marshal_with(school_model)
        def get(self, school_id):
            """Get a specific school by its numeric ID"""
            # Find one document in the 'schools' collection where the 'id' field matches.
            school = mongo.db.schools.find_one({'id': school_id})
            
            # If a school document is found, return it.
            if school:
                return school
            # Otherwise, return a 404 Not Found error.
            return {'error': 'School not found'}, 404

    # Defines the resource for getting all staff associated with a specific school.
    @api.route('/schools/<int:school_id>/staff')
    class SchoolStaff(Resource):

        # Decorator to format the list of staff members in the response.
        @api.marshal_list_with(staff_model)
        def get(self, school_id):
            """Get all staff members for a given school"""
            # First, confirm that the school exists using its numeric ID.
            school = mongo.db.schools.find_one({'id': school_id})
            if not school:
                # If the school doesn't exist, we can't get its staff. Return a 404.
                return {'error': 'School not found'}, 404

            # Find all staff members where the 'schoolId' field matches the
            # MongoDB _id of the school we just found.
            staff_list = list(mongo.db.staffs.find({'schoolId': str(school['_id'])}))
            
            # Return the list of staff members.
            return staff_list