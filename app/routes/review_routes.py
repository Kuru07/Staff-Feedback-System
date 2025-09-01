from flask_restx import Resource
from app import mongo
from bson.objectid import ObjectId
from app.models import review_model
from datetime import datetime

def register_routes(api):
    # Register REST endpoints for managing review resources
    @api.route('/reviews')
    class ReviewList(Resource):
        @api.marshal_list_with(review_model)
        def get(self):
            """
            Retrieve a list of all reviews from the database.

            Returns:
                List of reviews conforming to the review_model schema.
            """
            return list(mongo.db.reviews.find())

        @api.expect(review_model)
        def post(self):
            """
            Create a new review.

            - Expects payload conforming to review_model.
            - Resolves staffId based on employeeId provided by the user.
            - Converts 'date' field to Python datetime if given as a string.
            - Inserts the review into the database.

            Returns:
                Success message and ID of the newly added review.
                Error message if employeeId does not match any staff.
            """
            data = api.payload

            # Lookup staff in database using employeeId instead of MongoDB _id
            employee_id = data.get('staffId')
            staff = mongo.db.staffs.find_one({'employeeId': employee_id})
            if not staff:
                return {'error': 'Staff not found'}, 404

            # Replace staffId in review with MongoDB's string _id
            data['staffId'] = str(staff['_id'])

            # Convert provided date string (ISO format) to datetime object
            if 'date' in data and isinstance(data['date'], str):
                data['date'] = datetime.fromisoformat(data['date'].replace("Z", "+00:00"))

            # Insert the new review into the reviews collection
            result = mongo.db.reviews.insert_one(data)
            return {'message': 'Review added', 'review_id': str(result.inserted_id)}, 201


    @api.route('/reviews/<string:review_id>')
    class Review(Resource):
        @api.marshal_with(review_model)
        def get(self, review_id):
            """
            Retrieve a single review by its unique review_id.

            Args:
                review_id (str): The ObjectId string of the review.

            Returns:
                The review document if found, or error message if not found.
            """
            review = mongo.db.reviews.find_one({'_id': ObjectId(review_id)})
            if review:
                return review
            return {'error': 'Review not found'}, 404
