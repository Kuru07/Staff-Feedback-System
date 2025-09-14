# Import necessary components from Flask-RESTX and local modules.
from flask_restx import Resource
from app import mongo
from bson.objectid import ObjectId  # Used to convert string IDs to MongoDB's ObjectId format.
from app.models import staff_model, review_model # Import the data models for request/response marshaling.

def register_routes(api):
    """
    Registers all the API routes and their corresponding resource classes.

    This function acts as a centralized place to organize and attach all
    API endpoints to the main Flask-RESTX Api instance.

    :param api: The Flask-RESTX Api instance from the main app.
    """

    # Define the resource for handling the collection of staff members.
    @api.route('/staffs')
    class StaffList(Resource):
        
        # Decorator to serialize the response (a list of staff) using the staff_model.
        @api.marshal_list_with(staff_model)
        def get(self):
            """Get all staff members"""
            # Fetch all documents from the 'staffs' collection and return them as a list.
            return list(mongo.db.staffs.find())

        # Decorator indicating the expected input payload format for Swagger UI.
        @api.expect(staff_model)
        def post(self):
            """Create a new staff member linked to a school"""
            # 'api.payload' automatically parses the incoming JSON request body.
            data = api.payload

            # Validate and convert the incoming 'schoolId' (which should be numeric) to an integer.
            try:
                school_id_numeric = int(data.get('schoolId'))
            except (TypeError, ValueError):
                # If conversion fails, return a client error.
                return {'error': 'schoolId must be a numeric value'}, 400

            # Find the corresponding school document using its numeric 'id' field.
            school = mongo.db.schools.find_one({'id': school_id_numeric})
            if not school:
                # If no school is found, return a 404 Not Found error.
                return {'error': 'School not found'}, 404

            # Before saving, replace the numeric schoolId in the payload with the school's MongoDB _id.
            # This establishes the reference between the staff member and the school document.
            data['schoolId'] = str(school['_id'])

            # Insert the new staff member data into the 'staffs' collection.
            result = mongo.db.staffs.insert_one(data)
            
            # Return a success message and the new document's ID with a 201 Created status.
            return {'message': 'Staff added', 'staff_id': str(result.inserted_id)}, 201

    # Define the resource for handling a single staff member by their MongoDB _id.
    @api.route('/staffs/<string:staff_id>')
    class Staff(Resource):
        
        # Decorator to serialize the single object response using the staff_model.
        @api.marshal_with(staff_model)
        def get(self, staff_id):
            """Get a single staff member by MongoDB _id"""
            # Find a single staff member by their unique MongoDB '_id'.
            # ObjectId() is required to convert the URL's string parameter to a BSON ObjectId.
            staff = mongo.db.staffs.find_one({'_id': ObjectId(staff_id)})
            
            # If a staff member is found, return it.
            if staff:
                return staff
            # Otherwise, return a 404 Not Found error.
            return {'error': 'Staff not found'}, 404

    # Define the resource for handling reviews related to a specific staff member.
    # Note: This route uses the 'employeeId' for lookup, not the MongoDB '_id'.
    @api.route('/staffs/<string:staff_id>/reviews')
    class StaffReviews(Resource):

        # Decorator to serialize the list of reviews using the review_model.
        @api.marshal_list_with(review_model)
        def get(self, staff_id):
            """Get all reviews for a specific staff member"""
            # First, find the staff member using their human-readable 'employeeId'.
            staff = mongo.db.staffs.find_one({'employeeId': staff_id})
            if not staff:
                # If the staff member doesn't exist, return a 404 error.
                return {'error': 'Staff not found'}, 404

            # Use the MongoDB '_id' from the found staff member to fetch all related reviews.
            # The 'staffId' in the 'reviews' collection stores the MongoDB _id of the staff.
            reviews = list(mongo.db.reviews.find({'staffId': str(staff['_id'])}))
            
            # This line is likely for debugging purposes to check the staff's _id.
            print(staff['_id'])
            
            # Return the list of found reviews.
            return reviews