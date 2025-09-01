# Import the create_app function from the 'app' package/module.
# This function is an application factory, responsible for creating and configuring the Flask app instance.
from app import create_app

# Create an instance of the Flask application by calling the factory function.
app = create_app()

# This conditional block checks if the script is being executed directly
# by the Python interpreter (as opposed to being imported into another script).
if __name__ == "__main__":
    # If the script is run directly, start the built-in Flask development server.
    # 'debug=True' enables debug mode, which provides helpful error messages
    # and automatically reloads the server when code changes are saved.
    # Note: Debug mode should NOT be used in a production environment.
    app.run(debug=True)