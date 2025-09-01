# Import the 'os' module to interact with the operating system,
# specifically for accessing environment variables.
import os

# Import the 'load_dotenv' function from the 'python-dotenv' library.
# This library helps manage application configuration by loading variables
# from a special file into the environment.
from dotenv import load_dotenv

# Execute the function to load environment variables from a '.env' file
# in the project's root directory. This makes them accessible via os.getenv().
load_dotenv()

class Config:
    """
    A configuration class to store application settings. ⚙️

    This approach centralizes configuration variables, making them easier to
    manage and access throughout the application. It promotes a clean separation
    of configuration from code.
    """
    
    # Retrieve the MongoDB connection string from the environment variables.
    # os.getenv("MONGO_URI_CONNECTION") looks for an environment variable named
    # "MONGO_URI_CONNECTION" and assigns its value to this class attribute.
    # This practice is crucial for security as it avoids hardcoding sensitive
    # credentials like database URIs directly in the source code.
    MONGO_URI = os.getenv("MONGO_URI_CONNECTION")