# SoftDesk Support API

[Setup Instructions](#setup-instructions)
[Testing Instructions](#testing-instructions-for-softdesk-support-api)

## Introduction
The SoftDesk Support API is a RESTful service designed for SoftDesk, a collaborative software development company. This API facilitates issue tracking and project management for B2B interactions, ensuring efficient and secure technical support solutions.

## Features
- User management with privacy and consent options.
- Project and contributor management, allowing for issue tracking and comment posting.
- Resource prioritization, tagging, and status updates to streamline project workflows.

## Prerequisites
- Git
- Python 3.x
- Django 3.x
- Django REST Framework
- Other dependencies as outlined in `requirements.txt`

## Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/joluhan/Softdesk-API.git
   ```
2. Navigate to the project directory:
   ```
   cd Softdesk-API/
   ```
3. Setup and activate the virtual environment:
   ```
   python -m venv env
   # Unix/MacOS
   source env/bin/activate
   # Windows
   source env\Scripts\activate
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Apply database migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

## Security and Optimization Features
- Implements OWASP security specifications, utilizing JWT for user authentication and defining resource access permissions.
- Adheres to GDPR guidelines, ensuring data protection and privacy for all users.
- Follows green code principles to minimize server request loads and optimize performance.

## Running the API
Launch the development server:
```
python manage.py runserver
```
Access the API at `http://127.0.0.1:8000/`.

## Creating a Superuser Account
Generate a superuser account for backend administration:
```
python manage.py createsuperuser
```

## Testing Instructions for SoftDesk Support API

Ensure you have the following tools installed for testing:

- Postman or any API testing tool
- A local server running the SoftDesk Support API

### User Endpoints

1. User Signup:
   ```http
   POST http://localhost:8000/user/signup/
   ```
2. User Login:
   ```http
   POST http://localhost:8000/user/login/
   ```
3. User Profile:
   ```http
   GET http://localhost:8000/user/profile/
   PUT http://localhost:8000/user/profile/
   PATCH http://localhost:8000/user/profile/
   DELETE http://localhost:8000/user/profile/
   ```

### Project Endpoints

1. Create a Project:
   ```http
   POST http://localhost:8000/project/
   ```
2. List All Projects:
   ```http
   GET http://localhost:8000/project/
   ```
3. List a Specific Project:
   ```http
   GET http://localhost:8000/project/{id}/
   ```
4. Update a Specific Project:
   ```http
   PUT http://localhost:8000/project/{id}/
   ```
5. Delete a Specific Project:
   ```http
   DELETE http://localhost:8000/project/{id}/
   ```
6. Add a Contributor to a Project:
   ```http
   POST http://localhost:8000/project/{id}/add-contributor/
   ```
7. Remove a Contributor from a Project:
   ```http
   DELETE http://localhost:8000/project/{id}/remove-contributor/
   ```
8. Create an Issue within a Project:
   ```http
   POST http://localhost:8000/project/{project_id}/create-issue/
   ```

### Issue Endpoints

1. List a Specific Issue:
   ```http
   GET http://localhost:8000/issue/{issue_id}/
   ```
2. Update a Specific Issue:
   ```http
   PUT http://localhost:8000/issue/{issue_id}/
   ```
3. Partially Update a Specific Issue:
   ```http
   PATCH http://localhost:8000/issue/{issue_id}/
   ```
4. Delete a Specific Issue:
   ```http
   DELETE http://localhost:8000/issue/{issue_id}/
   ```

### Comment Endpoints

1. List a Specific Comment:
   ```http
   GET http://localhost:8000/comment/{id}/
   ```
2. Update a Specific Comment:
   ```http
   PUT http://localhost:8000/comment/{id}/
   ```
3. Partially Update a Specific Comment:
   ```http
   PATCH http://localhost:8000/comment/{id}/
   ```
4. Delete a Specific Comment:
   ```http
   DELETE http://localhost:8000/comment/{id}/
   ```

- Replace `{id}`, `{issue_id}`, and `{project_id}` with actual numeric values corresponding to a project, issue, or comment.