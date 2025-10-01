
from flask_restx import Resource
from app import mongo
from bson.objectid import ObjectId
from app.models import review_model
from datetime import datetime

# --- Feedback Filtering Imports ---
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from urbandict import define
from nltk.corpus import wordnet

# Download required NLTK data (safe to call multiple times)
nltk.download('punkt', quiet=True)
nltk.download('wordnet',quiet=True)

nltk.download('stopwords', quiet=True)

abuse_words = {
    "idiot", "stupid", "useless", "fool", "dumb", "nonsense",
    "lazy", "moron", "hate", "trash", "worst"
}

def check_abuse_word(text):
    words = text.lower().split()
    found = [w for w in words if w in abuse_words]
    return found

model = pipeline("text-classification", model="unitary/toxic-bert")

def check_toxicity(text):
    threshold = 0.5
    result = model(text)[0]
    label = result['label']
    score = result['score']
    if label == 'toxic' and score >= threshold:
        return True, score
    return False, score

stop_words = set(stopwords.words('english'))

import requests
def check_urban_dictionary(word):
    try:
        url = f"https://api.urbandictionary.com/v0/define?term={word}"
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status
        data = response.json()
        return len(data.get("list", [])) > 0  # Word exists if list is not empty
    except Exception as e:
        print(f"Urban Dictionary API error for '{word}': {e}")
        return False

def check_dictionary(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words and w not in string.punctuation]
    invalid_words = [w for w in words if not (wordnet.synsets(w) or check_urban_dictionary(w))]
    return invalid_words

def filter_feedback(feedback):
    abusive_words = check_abuse_word(feedback)
    if abusive_words:
        return f"Feedback contains abusive words: {', '.join(abusive_words)}"
    invalid_words = check_dictionary(feedback)
    if invalid_words:
        return f"Feedback contains non english words or not a proper sentence. Invalid word(s): {', '.join(invalid_words)}"
    toxic, score = check_toxicity(feedback)
    if toxic:
        return f"Feedback rejected (toxic detected, score={score:.2f})"
    return None  # No issues

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

            # --- Feedback Filtering ---
            feedback_text = data.get('text', '')
            filter_result = filter_feedback(feedback_text)
            if filter_result:
                return {'error': filter_result}, 400

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
