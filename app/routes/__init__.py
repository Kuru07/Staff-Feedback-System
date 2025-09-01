from .school_routes import register_routes as register_school_routes
from .staff_routes import register_routes as register_staff_routes
from .review_routes import register_routes as register_review_routes

def register_routes(api):
    """
    Registers all routes (school, staff, review) to the given Api instance.
    """
    register_school_routes(api)
    register_staff_routes(api)
    register_review_routes(api)
