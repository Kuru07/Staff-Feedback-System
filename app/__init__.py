# Import necessary classes from Flask and related extensions.
from flask import Flask
from flask_restx import Api
from flask_pymongo import PyMongo

# Import the application's configuration settings from the config.py file.
from config import Config

# Create an instance of the PyMongo extension. 
# This object will act as the bridge to the MongoDB database.
mongo = PyMongo()

# Create an instance of the Flask-RESTX Api.
# This sets up the main entry point for the API, including the title for the
# Swagger UI documentation, which will be available at the '/swagger/' endpoint.
api = Api(title="School Management API", doc="/swagger/")


def create_app():
    """
    Application factory function. 🏭

    This function encapsulates the creation of the Flask application instance,
    making the application structure more modular. It allows for creating
    different app instances for different environments (e.g., development, testing, production).

    :return: An instance of the configured Flask application.
    """
    # Create the core Flask application object.
    app = Flask(__name__)

    # Load configuration settings from the 'Config' class into the Flask app.
    # This keeps configuration variables separate from the application logic.
    app.config.from_object(Config)

    # Initialize the PyMongo extension with the Flask app.
    # This connects Flask to the MongoDB database using the URI from the app's config.
    mongo.init_app(app)

    # Initialize the Flask-RESTX Api extension with the Flask app.
    # This integrates the API layer with the application.
    api.init_app(app)

    # Import the route registration function locally to avoid circular dependencies.
    from app.routes import register_routes
    
    # Call the function to register all the defined API routes/namespaces with the Api instance.
    register_routes(api)

    # Return the fully configured application instance.
    return app