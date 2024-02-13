# Import the admin module from Django's built-in 'contrib' package.
# This module provides administrative functionalities.
from django.contrib import admin

# Import the User model from the 'models.py' file located in the 'accounts' application.
# The User model is a custom model defined to handle user data.
from accounts.models import User

# This section is designated for registering models with the Django admin site.
# By registering a model, it becomes accessible via the Django admin interface, allowing
# administrators to view, add, delete, and update records of this model.

# Register the User model with the admin site.
# This enables the User model to be managed through the Django admin interface.
# Once registered, the User model will appear in the admin dashboard, where administrators
# can perform CRUD operations (Create, Read, Update, Delete) on User instances.
admin.site.register(User)
