```markdown
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

1. **Clone the repository:**
   ```
   https://github.com/joluhan/Softdesk-API.git
   ```

2. **Navigate to the project directory:**
   ```
   cd softdesk-support-api
   ```

3. **Setup and activate the virtual environment:**
   ```
   python -m venv env
   source env/bin/activate  # Unix/MacOS
   env\Scripts\activate  # Windows
   ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Security and Optimization Features
- Implements OWASP security specifications, utilizing JWT for user authentication and defining resource access permissions.
- Adheres to GDPR guidelines, ensuring data protection and privacy for all users.
- Follows green code principles to minimize server request loads and optimize performance.

## Running the API

1. **Launch the development server:**
   ```
   python manage.py runserver
   ```

2. **Access the API:** The API will be available at `http://127.0.0.1:8000/`.

## Creating a Superuser Account

- Generate a superuser account for backend administration:
  ```
  python manage.py createsuperuser
  ```


# Testing Instructions for SoftDesk Support API

## User Endpoints

1. **User Signup:**
   ```
   POST http://localhost:8000/user/signup/
   ```
   Test: Submit user signup details and expect a confirmation message or token.

2. **User Login:**
   ```
   POST http://localhost:8000/user/login/
   ```
   Test: Submit user login credentials and expect a token in response.

3. **User Profile:**
   - GET `http://localhost:8000/user/profile/` to retrieve the user profile.
   - PUT `http://localhost:8000/user/profile/` to update the user profile with full data.
   - PATCH `http://localhost:8000/user/profile/` to partially update the user profile.
   - DELETE `http://localhost:8000/user/profile/` to remove the user profile.

## Project Endpoints

1. **Create a Project:**
   ```
   POST http://localhost:8000/project/
   ```
   Test: Submit new project details and expect a 201 status code for success.

2. **List All Projects:**
   ```
   GET http://localhost:8000/project/
   ```
   Test: Retrieve a list of all projects and expect a JSON list in response.

3. **List a Specific Project:**
   ```
   GET http://localhost:8000/project/{id}/
   ```
   Test: Retrieve details of a specific project using its ID.

4. **Update a Specific Project:**
   ```
   PUT http://localhost:8000/project/{id}/
   ```
   Test: Submit updated project details for a specific project.

5. **Delete a Specific Project:**
   ```
   DELETE http://localhost:8000/project/{id}/
   ```
   Test: Remove a specific project using its ID.

6. **Add a Contributor to a Project:**
   ```
   POST http://localhost:8000/project/{id}/add-contributor/
   ```
   Test: Add a contributor to a project and expect a success confirmation.

7. **Remove a Contributor from a Project:**
   ```
   DELETE http://localhost:8000/project/{id}/remove-contributor/
   ```
   Test: Remove a contributor from a project and expect a success confirmation.

8. **Create an Issue within a Project:**
   ```
   POST http://localhost:8000/project/{project_id}/create-issue/
   ```
   Test: Add a new issue to a project and expect a 201 status code for success.

## Issue Endpoints

1. **List a Specific Issue:**
   ```
   GET http://localhost:8000/issue/{issue_id}/
   ```
   Test: Retrieve details of a specific issue.

2. **Update a Specific Issue:**
   ```
   PUT http://localhost:8000/issue/{issue_id}/
   ```
   Test: Update details of a specific issue.

3. **Partially Update a Specific Issue:**
   ```
   PATCH http://localhost:8000/issue/{issue_id}/
   ```
   Test: Partially update details of a specific issue.

4. **Delete a Specific Issue:**
   ```
   DELETE http://localhost:8000/issue/{issue_id}/
   ```
   Test: Remove a specific issue using its ID.

## Comment Endpoints

1. **List a Specific Comment:**
   ```
   GET http://localhost:8000/comment/{id}/
   ```
   Test: Retrieve a specific comment using its ID.

2. **Update a Specific Comment:**
   ```
   PUT http://localhost:8000/comment/{id}/
   ```
   Test: Update a specific comment using its ID.

3. **Partially Update a Specific Comment:**
   ```
   PATCH http://localhost:8000/comment/{id}/
   ```
   Test: Partially update a comment using its ID.

4. **Delete a Specific Comment:**
   ```
   DELETE http://localhost:8000/comment/{id}/
   ```
   Test: Remove a specific comment using its ID.


- Replace `{id}`, `{issue_id}`, and `{project_id}` with actual numeric values corresponding to a project, issue, or comment.