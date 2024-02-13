from rest_framework import permissions  # Importing permissions module from rest_framework
from rest_framework.permissions import BasePermission, SAFE_METHODS  # Importing BasePermission class and SAFE_METHODS constant
from .models import ProjectContributor  # Importing the ProjectContributor model from the current directory

# Permission class to allow only read operations
class ReadOnly(BasePermission):
    """
    Permission class to allow only read operations.
    """
    def has_permission(self, request, view):
        """
        Check if the request method is a safe method (GET, HEAD, OPTIONS).
        """
        return request.user and request.method in SAFE_METHODS

# Permission class to check if the user is a contributor to the project
class IsContributor(permissions.BasePermission):
    """
    Permission class to check if the user is a contributor to the project.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a contributor to the project associated with the object.
        """
        return ProjectContributor.objects.filter(project=obj, contributor=request.user).exists()

# Permission class to check if the user is the creator of the object
class IsCreator(permissions.BasePermission):
    """
    Permission class to check if the user is the creator of the element.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the creator of the object.
        """
        return obj.creator == request.user

# Permission class to check if the user is the creator of the project
class IsProjectCreator(permissions.BasePermission):
    """
    Permission class to check if the user is the creator of the project.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the creator of the project associated with the object or the issue.
        """
        return obj.project.creator == request.user or obj.issue.project.creator == request.user
