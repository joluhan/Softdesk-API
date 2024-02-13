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

# Decorator to specify Swagger documentation for the endpoint.
@swagger_auto_schema(methods=['DELETE'], request_body=RemoveContributorSerializer)
# Decorator to specify that this view requires authentication.
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_contributor(request, id):
    # Trying to retrieve the project object with the given ID.
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        # Returning a 404 response if the project does not exist.
        return Response({
            "message": "Project does not exist"
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Checking if the requester is the creator of the project.
    if project.creator == request.user:
        try:
            # Trying to retrieve the contributor object for the specified project and username.
            contributor = ProjectContributor.objects.get(project=project, contributor__username=request.data['username'])
            if contributor.contributor == project.creator:
                # If the contributor is the project creator, returning a 400 response.
                return Response({
                    "message": f"{contributor.contributor} is project creator and cannot be removed"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Deleting the contributor object if found.
                contributor.delete()
                return Response({
                    "message": f"{request.data['username']} has been removed from the project"
                }, status=status.HTTP_204_NO_CONTENT)
        except ProjectContributor.DoesNotExist:
            # If the contributor does not exist, returning a 400 response.
            return Response({
                "message": "User not a contributor to this project"
            }, status=status.HTTP_400_BAD_REQUEST)
    # If the requester is not the project creator, returning a 403 response.
    return Response({
            "detail": "You do not have permission to remove project contributors!"
        }, status=status.HTTP_403_FORBIDDEN)

class ProjectView(RetrieveUpdateDestroyAPIView):
    # Queryset containing all projects.
    queryset = Project.objects.all()
    
    # Serializer class to use for project details.
    serializer_class = ProjectDetailSerializer
    
    # Field to use for looking up projects.
    lookup_field = 'id'
    
    # Permission classes required for accessing the view.
    permission_classes = [IsAuthenticated, IsContributor]
    
    # Pagination class for paginating issues.
    pagination_class = CustomPagination

    # Override the default destroy method to handle project deletion.
    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        # Check if the requester is the creator of the project.
        if project.creator == request.user:
            project.delete()
            return Response({
                "detail": "Project successfully deleted"
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "detail": "You do not have permission to delete this project !"
        }, status=status.HTTP_403_FORBIDDEN)

    # Override the default update method to handle project updates.
    def update(self, request, *args, **kwargs):
        project = self.get_object()
        # Check if the requester is the creator of the project.
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

    # Override the default retrieve method to include related issues.
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Retrieve all issues related to the project.
        issues = instance.issue_set.all()

        # Use pagination to paginate issues and add them to 'project_details'.
        page = self.paginate_queryset(issues)
        if page is not None:
            issue_serializer = IssueListSerializer(page, many=True)
            return self.get_paginated_response({
                'project_details': serializer.data,
                'project_issues': issue_serializer.data,
            })

class CreateIssueView(CreateAPIView):
    # Serializer class for creating issues.
    serializer_class = IssueSerializer
    
    # Permission classes required for accessing the view.
    permission_classes = [IsAuthenticated, IsContributor]

    # Override the default create method to handle issue creation.
    def create(self, request, *args, **kwargs):
        # Get the project ID from URL parameters.
        project_id = self.kwargs.get('project_id')
        
        # Try to retrieve the project object.
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            # Return a 404 response if the project does not exist.
            return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requester is a contributor to the project.
        if not ProjectContributor.objects.filter(project=project, contributor=request.user).exists():
            return Response({"message": "You are not a contributor to this project"},
                            status=status.HTTP_403_FORBIDDEN)

        # Validate the incoming data using the serializer.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract the assigned_to username from the request data.
        assigned_to_username = serializer.validated_data.get('assigned_to')
        if assigned_to_username:
            # Find the User by username.
            user = User.objects.filter(username=assigned_to_username).first()

            if not user:
                return Response({
                    "message": "The specified user does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Ensure that the user is a contributor of the project.
            contributor = ProjectContributor.objects.filter(project=project, contributor=user).first()
            if not contributor:
                return Response({
                    "message": "The specified user is not a contributor to this project"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Set the assigned_to field to the Contributor instance.
            serializer.validated_data['assigned_to'] = contributor.contributor
        
        # Save the issue with creator and project information.
        serializer.save(creator=request.user, project=project)

        # Return a success response with the serialized issue data.
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class IssueView(RetrieveUpdateDestroyAPIView):
    # Serializer class for listing issues.
    serializer_class = IssueListSerializer
    
    # Queryset containing all issues.
    queryset = Issue.objects.all()
    
    # Permission classes required for accessing the view.
    permission_classes = [IsAuthenticated, IsContributor]
    
    # Pagination class for paginating comments.
    pagination_class = CustomPagination

    # Custom method to get the issue object based on the URL parameter.
    def get_object(self):
        # Extract the issue ID from the URL parameters.
        issue_id = self.kwargs.get('issue_id')
        try:
            # Try to retrieve the issue object with the given ID.
            issue = Issue.objects.get(id=issue_id)
            return issue
        except Issue.DoesNotExist:
            # Return a 404 response if the issue does not exist.
            return Response({"message": "Issue not found"}, status=status.HTTP_404_NOT_FOUND)

    # Override the default retrieve method to include related comments.
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Retrieve all comments related to the issue.
        comments = Comment.objects.filter(issue=instance)

        # Paginate comments if necessary and add them to the response.
        page = self.paginate_queryset(comments)
        if page is not None:
            comment_serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response({
                'issue_details': serializer.data,
                'issue_comments': comment_serializer.data,
            })

        # If there are no comments, return only the issue details.
        return Response({
            'issue_details': serializer.data,
            'issue_comments': [],
        })

    # Override the default update method to handle issue updates.
    def update(self, request, *args, **kwargs):
        issue = self.get_object()
        project = issue.project  # Get the project ID of the issue

        # Check if the requester is the creator of the issue or the project creator.
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

    # Override the default destroy method to handle issue deletion.
    def destroy(self, request, *args, **kwargs):
        issue = self.get_object()
        # Check if the requester is the creator of the issue or the project creator.
        if issue.creator == request.user or issue.project.creator == request.user:
            issue.delete()
            return Response({"detail": "Issue successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "detail": "You do not have permission to delete this issue !"
        }, status=status.HTTP_403_FORBIDDEN)

class CreateCommentView(CreateAPIView):
    # Serializer class for creating comments.
    serializer_class = CommentSerializer
    
    # Permission classes required for accessing the view.
    permission_classes = [IsAuthenticated, IsContributor]

    # Custom method to perform the creation of a new comment.
    def perform_create(self, serializer):
        # Extract the issue ID from URL parameters.
        issue_id = self.kwargs.get('issue_id')
        # Get the current user.
        user = self.request.user

        try:
            # Try to retrieve the issue object with the given ID.
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            # Return a 404 response if the issue does not exist.
            return Response({"message": "Issue not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is a contributor to the project of the issue.
        project = issue.project
        contributor = ProjectContributor.objects.filter(project=project, contributor=user).first()

        if contributor:
            # If the user is a contributor, save the comment with their information.
            serializer.save(creator=contributor.contributor, issue=issue)
        else:
            # If the user is not a contributor, return a 403 response.
            return Response({
                "message": "You are not a contributor to this project and cannot create a comment"
            }, status=status.HTTP_403_FORBIDDEN)


class CommentView(RetrieveUpdateDestroyAPIView):
    # Queryset containing all comments.
    queryset = Comment.objects.all()
    
    # Serializer class for comments.
    serializer_class = CommentSerializer
    
    # Permission classes required for accessing the view.
    permission_classes = [IsAuthenticated]

    # Custom method to retrieve a comment.
    def retrieve(self, request, *args, **kwargs):
        # Get the comment object.
        comment = self.get_object()
        # Check if the requester is the creator of the comment or the project creator.
        if comment.creator == request.user or comment.issue.project.creator == request.user:
            serializer = self.get_serializer(comment)
            return Response(serializer.data)
        else:
            # If the requester does not have permission, return a 403 response.
            return Response({
                "detail": "You do not have permission to get this comment !"
            }, status=status.HTTP_403_FORBIDDEN)

    # Custom method to perform an update on a comment.
    def perform_update(self, serializer):
        # Get the comment object.
        comment = self.get_object()
        # Check if the requester is the creator of the comment or the project creator.
        if comment.creator == self.request.user or comment.issue.project.creator == self.request.user:
            serializer.save()
            return Response({"detail": "Comment successfully updated"}, status=status.HTTP_200_OK)
        else:
            # If the requester does not have permission, return a 403 response.
            return Response({
                "detail": "You do not have permission to update this comment !"
            }, status=status.HTTP_403_FORBIDDEN)

    # Custom method to delete a comment.
    def destroy(self, request, *args, **kwargs):
        # Get the comment object.
        comment = self.get_object()
        # Check if the requester is the creator of the comment or the project creator.
        if comment.creator == request.user or comment.issue.project.creator == request.user:
            comment.delete()
            return Response({"detail": "Comment successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            # If the requester does not have permission, return a 403 response.
            return Response({
                "detail": "You do not have permission to delete this comment !"
            }, status=status.HTTP_403_FORBIDDEN)
