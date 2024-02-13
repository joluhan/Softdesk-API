# Import the AppConfig class from django.apps module.
# AppConfig is used by Django applications to configure some of the application's attributes
# and behaviors.
from django.apps import AppConfig

# Define the AccountsConfig class which inherits from AppConfig.
# This class is used to configure some settings specific to the 'accounts' application.
class AccountsConfig(AppConfig):
    # Set the default_auto_field attribute to 'django.db.models.BigAutoField'.
    # This specifies the type of auto-incrementing ID field that Django will use for primary keys
    # in this application. 'BigAutoField' is a 64-bit integer field that is suitable for cases
    # where a very large number of records are expected and the standard AutoField's 32-bit integer
    # might not be sufficient.
    default_auto_field = 'django.db.models.BigAutoField'

    # The name attribute specifies the full Python path to the application.
    # It is used by Django to identify the application. This is especially important for projects
    # with multiple applications. Here, 'accounts' indicates that the configuration applies to
    # the 'accounts' application.
    name = 'accounts'
