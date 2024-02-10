from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import ProjectContributor


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.method in SAFE_METHODS
    
class IsContributor(permissions.BasePermission):
    # must be a contributor to the project
    def has_object_permission(self, request, view, obj):
        return ProjectContributor.objects.filter(project=obj, contributor=request.user).exists()


class IsCreator(permissions.BasePermission):
    # must be the creator of the element
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class IsProjectCreator(permissions.BasePermission):
    # must be the creator of the project
    def has_object_permission(self, request, view, obj):
        obj.project.creator == request.user or obj.issue.project.creator == request.user
