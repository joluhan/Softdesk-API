# Import the default policy from the email.policy module. 
# This is not used in the provided code snippet, so it might be a remnant from other operations or a mistake.
from email.policy import default

# Import models from the django.db module.
# This module provides classes for defining database schema (models) in Django.
from django.db import models

# Import AbstractUser, Group, and Permission classes from django.contrib.auth.models.
# AbstractUser: A base class for implementing custom user models with Django's authentication system.
# Group: A model that represents groups for users. Groups are a generic way of categorizing users.
# Permission: A model that represents specific permissions that can be granted to users or groups.
from django.contrib.auth.models import AbstractUser, Group, Permission

# Import gettext function from django.utils.translation module and rename it to _.
# This function is used for internationalizing strings, allowing them to be translated into different languages.
from django.utils.translation import gettext as _

# Define the User class, inheriting from AbstractUser.
# This custom User model extends the base functionality provided by Django's default user model.
class User(AbstractUser):
    # Define a BooleanField for 'can_be_contacted', with a default value of False.
    # This field specifies whether the user agrees to be contacted.
    can_be_contacted = models.BooleanField(default=False)

    # Define a BooleanField for 'can_data_be_shared', with a default value of False.
    # This field specifies whether the user agrees for their data to be shared.
    can_data_be_shared = models.BooleanField(default=False)

    # Define a DateField for 'date_of_birth'.
    # This field stores the user's date of birth.
    date_of_birth = models.DateField()

    # Define a ManyToManyField relationship with the Group model.
    # This specifies the groups a user belongs to, allowing for categorization and permission management.
    # It is customized with a verbose_name, blank option, and a related_name for reverse queries.
    groups = models.ManyToManyField(Group, verbose_name=_('groups'),
        blank=True, related_name='custom_user_groups')

    # Define a ManyToManyField relationship with the Permission model.
    # This allows specifying custom permissions for each user.
    # It includes a verbose_name, blank option, related_name, and help_text for additional context.
    user_permissions = models.ManyToManyField(
        Permission, verbose_name=_('user permissions'),
        blank=True, related_name='custom_user_permissions',
        help_text=_('Specific permissions for this user.'),
    )

    # Define the __str__ method to return the username of the user.
    # This method is used to represent a User instance as a string, making it easier to identify users.
    def __str__(self):
        return self.username
