# Staff Feedback System - Complete Documentation

## 🏫 System Overview

The Staff Feedback System is a comprehensive web-based application designed to manage educational institutions, their staff members, and collect feedback reviews. Built using Flask and MongoDB, this system provides a robust RESTful API for educational management with automated documentation through Swagger UI.

### 🎯 Key Features
- **School Management**: Create and retrieve school information
- **Staff Management**: Manage staff members across different schools
- **Review System**: Collect and manage feedback/reviews for staff members
- **RESTful API**: Well-structured API endpoints with automatic documentation
- **MongoDB Integration**: NoSQL database for flexible data storage
- **Swagger Documentation**: Interactive API documentation at `/swagger/`

---

## 📁 Project Structure

```
Staff-Feedback-System/
├── app.py                    # Application entry point
├── config.py                 # Configuration settings
├── .gitignore               # Git ignore file
├── app/                     # Main application package
│   ├── __init__.py         # App factory and initialization
│   ├── models.py           # Data models for API validation
│   └── routes/             # API route definitions
│       ├── __init__.py     # Route registration
│       ├── school_routes.py # School-related endpoints
│       ├── staff_routes.py # Staff-related endpoints
│       └── review_routes.py # Review-related endpoints
└── env/                    # Python virtual environment
    ├── Scripts/           # Environment scripts
    ├── Lib/site-packages/ # Installed packages
    └── pyvenv.cfg         # Virtual environment config
```

---

## 🛠️ Technical Architecture

### Core Components

#### 1. Application Factory Pattern (`app/__init__.py`)
- **Purpose**: Creates and configures Flask application instances
- **Benefits**: Enables multiple configurations (dev/test/production)
- **Key Functions**:
  - Initializes Flask application
  - Configures MongoDB connection
  - Sets up Flask-RESTX API with Swagger documentation
  - Registers all route blueprints

#### 2. Configuration Management (`config.py`)
- **Environment Variables**: Uses `python-dotenv` for secure configuration
- **MongoDB URI**: Configured via `MONGO_URI_CONNECTION` environment variable
- **Security**: Prevents hardcoding sensitive credentials

#### 3. Data Models (`app/models.py`)
**School Model**:
- `_id`: MongoDB unique identifier (read-only)
- `id`: School-specific integer ID (required)
- `name`: School name (required)

**Staff Model**:
- `_id`: MongoDB unique identifier (read-only)
- `name`: Staff member name (required)
- `employeeId`: Unique employee identifier (required)
- `schoolId`: Reference to associated school (required)

**Review Model**:
- `_id`: MongoDB unique identifier (read-only)
- `text`: Review content (required)
- `rating`: Numeric rating 1-5 (required)
- `date`: Review submission date (required)
- `staffId`: Reference to staff member (required)

#### 4. API Routes Architecture
**School Routes** (`app/routes/school_routes.py`):
- `GET /schools` - Retrieve all schools
- `POST /schools` - Create new school with validation
- `GET /schools/<int:school_id>` - Get specific school
- `GET /schools/<int:school_id>/staff` - Get all staff for a school

**Staff Routes** (`app/routes/staff_routes.py`):
- Complete CRUD operations for staff management
- School association validation
- Employee ID uniqueness checks

**Review Routes** (`app/routes/review_routes.py`):
- Review submission and retrieval
- Rating validation (1-5 scale)
- Staff association verification

---

## 🚀 Installation & Setup Guide

### Prerequisites
- Python 3.7 or higher
- MongoDB (local or cloud instance)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/Kuru07/Staff-Feedback-System.git
cd Staff-Feedback-System
```

### Step 2: Virtual Environment Setup
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# Linux/Mac:
source env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install flask
pip install flask-restx
pip install flask-pymongo
pip install python-dotenv
```

### Step 4: Environment Configuration
Create a `.env` file in the project root:
```env
MONGO_URI_CONNECTION=mongodb://localhost:27017/staff_feedback_db
# OR for MongoDB Atlas:
# MONGO_URI_CONNECTION=mongodb+srv://username:password@cluster.mongodb.net/staff_feedback_db
```

### Step 5: Database Setup
1. **Local MongoDB**: Ensure MongoDB service is running
2. **MongoDB Atlas**: Create cluster and obtain connection string
3. **Database Collections**: The application will auto-create collections:
   - `schools`
   - `staffs`
   - `reviews`

### Step 6: Run Application
```bash
python app.py
```

The application will start on `http://localhost:5000`
Swagger documentation available at: `http://localhost:5000/swagger/`

---

## 📖 User Guide

### Accessing the API

#### Interactive Documentation
- Navigate to `http://localhost:5000/swagger/`
- View all available endpoints
- Test API calls directly from the browser
- See request/response schemas

#### API Endpoints Overview

**School Management**:
1. **List All Schools**
   - **Method**: GET
   - **URL**: `/schools`
   - **Response**: Array of school objects

2. **Create New School**
   - **Method**: POST
   - **URL**: `/schools`
   - **Body**: `{"id": 1, "name": "Example School"}`
   - **Response**: Success message with school_id

3. **Get Specific School**
   - **Method**: GET
   - **URL**: `/schools/{school_id}`
   - **Response**: Single school object

4. **Get School Staff**
   - **Method**: GET
   - **URL**: `/schools/{school_id}/staff`
   - **Response**: Array of staff members

**Staff Management**:
- CRUD operations for staff members
- Associate staff with schools
- Manage employee information

**Review System**:
- Submit feedback for staff members
- Rate staff performance (1-5 scale)
- Retrieve reviews by staff member

### Sample Usage Workflows

#### Workflow 1: Setting Up a New School
1. Create school via POST `/schools`
2. Add staff members via POST `/staff`
3. Assign staff to school using schoolId
4. Begin collecting reviews

#### Workflow 2: Collecting Feedback
1. Identify staff member ID
2. Submit review via POST `/reviews`
3. Include rating (1-5) and text feedback
4. Review is automatically timestamped

---

## 🔧 API Reference

### Error Handling
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Server-side issues

### Data Validation
- **School ID**: Must be unique integer
- **Employee ID**: Must be unique string
- **Rating**: Must be integer between 1-5
- **Required Fields**: Validated on all POST requests

### Response Formats
**Success Response**:
```json
{
  "message": "Operation successful",
  "data": {...}
}
```

**Error Response**:
```json
{
  "error": "Description of error"
}
```

---

## 🤝 Contribution Guide

### Development Setup
1. Fork the repository
2. Clone your fork locally
3. Create a feature branch: `git checkout -b feature-name`
4. Set up development environment as per installation guide
5. Enable debug mode in `app.py` (already enabled)

### Code Standards
- **Python Style**: Follow PEP 8 guidelines
- **Documentation**: Add docstrings to all functions
- **Comments**: Explain complex logic and business rules
- **Validation**: Always validate input data
- **Error Handling**: Provide meaningful error messages

### File Organization
- **Routes**: Separate files for each major entity (school, staff, review)
- **Models**: Centralized data model definitions
- **Configuration**: Environment-based configuration management
- **Factory Pattern**: Use application factory for different environments

### Adding New Features

#### Adding a New Endpoint
1. Define data model in `app/models.py`
2. Create route file in `app/routes/`
3. Implement CRUD operations with validation
4. Register routes in `app/routes/__init__.py`
5. Update documentation

#### Database Schema Changes
1. Update corresponding model in `models.py`
2. Implement migration logic if needed
3. Update API documentation
4. Test with sample data

### Testing Guidelines
- Test all API endpoints
- Validate error handling
- Check data integrity
- Verify MongoDB operations
- Test with various input scenarios

### Submission Process
1. Commit changes with descriptive messages
2. Push to your fork
3. Create pull request with:
   - Clear description of changes
   - List of affected endpoints
   - Testing instructions
   - Documentation updates

---

## 🏗️ System Architecture Details

### Technology Stack
- **Backend Framework**: Flask (Python)
- **API Framework**: Flask-RESTX
- **Database**: MongoDB
- **ODM**: PyMongo
- **Configuration**: python-dotenv
- **Documentation**: Swagger/OpenAPI 3.0

### Design Patterns
- **Application Factory**: Flexible app creation
- **Blueprint Pattern**: Modular route organization
- **Repository Pattern**: Data access abstraction
- **Model-View-Controller**: Separation of concerns

### Security Considerations
- Environment variable configuration
- Input validation and sanitization
- MongoDB injection prevention
- Error message sanitization

### Scalability Features
- Modular route structure
- Database connection pooling via PyMongo
- Stateless API design
- Environment-based configuration

---

## 🔍 Troubleshooting

### Common Issues

**MongoDB Connection Error**:
- Verify MongoDB service is running
- Check connection string in `.env` file
- Ensure database permissions are correct

**Import Errors**:
- Activate virtual environment
- Install all required packages
- Check Python path configuration

**Port Already in Use**:
- Change port in `app.py`: `app.run(debug=True, port=5001)`
- Or kill process using port 5000

**Swagger UI Not Loading**:
- Verify Flask-RESTX installation
- Check API initialization in `app/__init__.py`
- Clear browser cache

### Debug Mode
- Debug mode is enabled by default
- Provides detailed error messages
- Auto-reloads on code changes
- **WARNING**: Disable in production

---

## 📝 Additional Notes

### Development Best Practices
- Use virtual environments for dependency isolation
- Keep sensitive data in environment variables
- Implement proper error handling
- Write comprehensive API documentation
- Follow RESTful API design principles

### Production Deployment
- Disable debug mode
- Use production WSGI server (Gunicorn, uWSGI)
- Implement proper logging
- Set up monitoring and health checks
- Use environment-specific configuration files

### Future Enhancements
- Authentication and authorization system
- Role-based access control
- Email notifications for reviews
- Advanced reporting and analytics
- Data export functionality
- Review moderation system

---

*Documentation last updated: September 1, 2025*
*Version: 1.0.0*
