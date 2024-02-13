# Import the AppConfig class from the django.apps module.
from django.apps import AppConfig

# Define a new class named SoftdeskConfig, which inherits from AppConfig.
class SoftdeskConfig(AppConfig):
    # Set the default_auto_field attribute to 'django.db.models.BigAutoField'.
    default_auto_field = 'django.db.models.BigAutoField'
    # Set the name attribute to 'softdesk'.
    name = 'softdesk'
