from django.shortcuts import render  # Importing render function from django.shortcuts
from rest_framework.response import Response  # Importing Response class from rest_framework.response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView  # Importing CreateAPIView and RetrieveUpdateDestroyAPIView from rest_framework.generics
from rest_framework.decorators import api_view, permission_classes, action  # Importing api_view, permission_classes, and action decorators
from rest_framework import status  # Importing status module from rest_framework
from drf_yasg.utils import swagger_auto_schema  # Importing swagger_auto_schema function from drf_yasg.utils
from rest_framework.viewsets import ReadOnlyModelViewSet  # Importing ReadOnlyModelViewSet from rest_framework.viewsets
from rest_framework.permissions import IsAuthenticated  # Importing IsAuthenticated permission class from rest_framework.permissions
from accounts.models import User  # Importing User model from accounts app
from .models import Comment, Issue, Project, ProjectContributor  # Importing models from the current directory
from .paginations import CustomPagination  # Importing CustomPagination class from paginations module
from .permissions import IsContributor  # Importing IsContributor permission class from permissions module
from .serializers import AddContributorSerializer, CommentSerializer, IssueListSerializer, IssueSerializer, ProjectDetailSerializer, ProjectListSerializer, ProjectSerializer, RemoveContributorSerializer  # Importing serializers from the current directory

# Create your views here.

# View mixin for custom project list view
class CustomListProjectsViewMixin:
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])  # Decorator for creating a new project
    def create(self, request):
        serializer = ProjectSerializer(data=request.data)  # Serializing the request data
        if serializer.is_valid():  # Checking if the serializer data is valid
            project = serializer.save(creator=request.user)  # Saving the project with the current user as creator
            ProjectContributor.objects.create(project=project, contributor=request.user)  # Adding the current user as contributor to the project
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Returning successful response with created project data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Returning error response with serializer errors

# View for listing projects with permissions applied
@permission_classes([IsAuthenticated])  # Applying IsAuthenticated permission to the view
class ListProjectsView(CustomListProjectsViewMixin, ReadOnlyModelViewSet):
    queryset = Project.objects.all()  # Queryset for retrieving all projects
    serializer_class = ProjectListSerializer  # Serializer class for serializing projects
    pagination_class = CustomPagination  # Pagination class for paginating project list

# Endpoint for adding a contributor to a project
@swagger_auto_schema(methods=['POST'], request_body=AddContributorSerializer)  # Adding swagger documentation for the endpoint
@api_view(['POST'])  # Specifying the HTTP methods allowed for this endpoint
@permission_classes([IsAuthenticated])  # Applying IsAuthenticated permission to the endpoint
def add_contributor(request, id):
    try:
        project = Project.objects.get(id=id)  # Retrieving the project with the given id
    except Project.DoesNotExist:
        return Response({"message": "Project does not exist"}, status=status.HTTP_404_NOT_FOUND)  # Returning error response if project does not exist

    if project.creator == request.user:  # Checking if the current user is the creator of the project
        try:
            contributor = User.objects.get(username=request.data['username'])  # Retrieving the user to be added as a contributor
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)  # Returning error response if user not found

        if ProjectContributor.objects.filter(project=project, contributor=contributor).exists():
            return Response({"message": f"{contributor} is already a contributor to this project"}, status=status.HTTP_400_BAD_REQUEST)  # Returning error response if user is already a contributor

        ProjectContributor.objects.create(project=project, contributor=contributor)  # Adding the user as a contributor to the project
        return Response({"message": f"{contributor} added as a contributor to this project successfully"}, status=status.HTTP_201_CREATED)  # Returning success response if user added successfully

    return Response({"detail": "You do not have permission to add contributors to this project!"}, status=status.HTTP_403_FORBIDDEN)  # Returning error response if user does not have permission

@swagger_auto_schema(methods=['DELETE'], request_body=RemoveContributorSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_contributor(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        return Response({
            "message": "Project does not exist"
        }, status=status.HTTP_404_NOT_FOUND)
    
    if project.creator == request.user:
        try:
            contributor = ProjectContributor.objects.get(project=project, contributor__username=request.data['username'])
            if contributor.contributor == project.creator:
                return Response({
                    "message": f"{contributor.contributor} is project creator and cannot be removed"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                contributor.delete()
                return Response({
                    "message": f"{request.data['username']} has been removed from the project"
                }, status=status.HTTP_204_NO_CONTENT)
        except ProjectContributor.DoesNotExist:
            return Response({
                "message": "User not a contributor to this project"
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response({
            "detail": "You do not have permission to remove project contributors!"
        }, status=status.HTTP_403_FORBIDDEN)


class ProjectView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsContributor]
    pagination_class = CustomPagination

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.creator == request.user:
            project.delete()
            return Response({
                "detail": "Project successfully deleted"
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "detail": "You do not have permission to delete this project !"
        }, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if project.creator == request.user:
            serializer = self.get_serializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"detail": "Project successfully updated"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "detail": "You do not have permission to update this project !"
                }, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        issues = instance.issue_set.all()

        # Use pagination to paginate issues and add them to 'project_details'
        page = self.paginate_queryset(issues)
        if page is not None:
            issue_serializer = IssueListSerializer(page, many=True)
            return self.get_paginated_response({
                'project_details': serializer.data,
                'project_issues': issue_serializer.data,
            })


class CreateIssueView(CreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')  # get ID Project
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        # control if user is a contributor of Project
        if not ProjectContributor.objects.filter(project=project, contributor=request.user).exists():
            return Response({"message": "You are not a contributor to this project"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract the assigned_to username from the request data
        assigned_to_username = serializer.validated_data.get('assigned_to')
        if assigned_to_username:
            # Find the User by username
            user = User.objects.filter(username=assigned_to_username).first()

            if not user:
                return Response({
                    "message": "The specified user does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Ensure that the user is a contributor of the project
            contributor = ProjectContributor.objects.filter(project=project, contributor=user).first()
            if not contributor:
                return Response({
                    "message": "The specified user is not a contributor to this project"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Set the assigned_to field to the Contributor instance
            serializer.validated_data['assigned_to'] = contributor.contributor
        serializer.save(creator=request.user, project=project)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IssueView(RetrieveUpdateDestroyAPIView):
    serializer_class = IssueListSerializer
    queryset = Issue.objects.all()
    permission_classes = [IsAuthenticated, IsContributor]
    pagination_class = CustomPagination

    def get_object(self):
        # to config and select id of issue
        issue_id = self.kwargs.get('issue_id')
        try:
            issue = Issue.objects.get(id=issue_id)
            return issue
        except Issue.DoesNotExist:
            return Response({"message": "Issue not found"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # get Comment to Issue
        comments = Comment.objects.filter(issue=instance)

        # Use pagination to paginate Comment
        page = self.paginate_queryset(comments)
        if page is not None:
            comment_serializer = CommentSerializer(page, many=True)
            # Return issue details and paginated list of comments
            return self.get_paginated_response({
                'issue_details': serializer.data,
                'issue_comments': comment_serializer.data,
            })

        return Response({
            'issue_details': serializer.data,
            'issue_comments': [],
        })

    def update(self, request, *args, **kwargs):
        issue = self.get_object()
        project = issue.project  # get id du projet de l'Issue

        if issue.creator == request.user or issue.project.creator == request.user:
            serializer = self.get_serializer(issue, data=request.data, partial=True)
            if serializer.is_valid():
                assigned_to_username = request.data.get('assigned_to')

                if assigned_to_username is not None:
                    if not ProjectContributor.objects.filter(project=project, contributor=request.user).exists():
                        return Response({
                            "message": "You are not a contributor to this project"
                        }, status=status.HTTP_403_FORBIDDEN)

                    if assigned_to_username:
                        user = User.objects.get(username=assigned_to_username)

                        if not user:
                            return Response({
                                "message": "The specified user does not exist"
                            }, status=status.HTTP_400_BAD_REQUEST)

                        contributor = ProjectContributor.objects.filter(project=project, contributor=user).first()
                        if not contributor:
                            return Response({
                                "message": "The specified user is not a contributor to this project"
                            }, status=status.HTTP_400_BAD_REQUEST)

                        serializer.validated_data['assigned_to'] = contributor.contributor
                    else:
                        serializer.validated_data['assigned_to'] = None
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "detail": "You do not have permission to update this issue!"
        }, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        issue = self.get_object()
        if issue.creator == request.user or issue.project.creator == request.user:
            issue.delete()
            return Response({"detail": "Issue successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "detail": "You do not have permission to delete this issue !"
        }, status=status.HTTP_403_FORBIDDEN)


class CreateCommentView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('issue_id')
        user = self.request.user

        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return Response({"message": "Issue not found"}, status=status.HTTP_404_NOT_FOUND)

        # check if user is contributor to project issue
        project = issue.project
        contributor = ProjectContributor.objects.filter(project=project, contributor=user).first()

        if contributor:
            serializer.save(creator=contributor.contributor, issue=issue)
        else:
            return Response({
                "message": "You are not a contributor to this project and cannot create a comment"
            }, status=status.HTTP_403_FORBIDDEN)


class CommentView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.creator == request.user or comment.issue.project.creator == request.user:
            serializer = self.get_serializer(comment)
            return Response(serializer.data)
        else:
            return Response({
                "detail": "You do not have permission to get this comment !"
            }, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.creator == self.request.user or comment.issue.project.creator == self.request.user:
            serializer.save()
            return Response({"detail": "Comment successfully updated"}, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "You do not have permission to update this comment !"
            }, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.creator == request.user or comment.issue.project.creator == request.user:
            comment.delete()
            return Response({"detail": "Comment successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "detail": "You do not have permission to delete this comment !"
            }, status=status.HTTP_403_FORBIDDEN)
