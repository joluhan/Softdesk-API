from rest_framework.pagination import PageNumberPagination  # Importing the PageNumberPagination class from the rest_framework.pagination module

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for controlling pagination settings.
    """
    page_size = 5  # Number of items to include per page
    page_size_query_param = 'page_size'  # Name of the query parameter to specify the page size
    max_page_size = 50  # Maximum number of items allowed per page
