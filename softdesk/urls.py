from django.urls import path  # Importing path function from django.urls
from . import views  # Importing views module from the current directory

urlpatterns = [
    # Endpoint for creating a new project and listing all projects
    path('project/', views.ListProjectsView.as_view({'post': 'create', 'get': 'list'}), name='project-list'),
    
    # Endpoint for adding a contributor to a project
    path('project/<int:id>/add-contributor/', views.add_contributor, name='add contributor'),
    
    # Endpoint for removing a contributor from a project
    path('project/<int:id>/remove-contributor/', views.remove_contributor, name='remove contributor'),
    
    # Endpoint for retrieving, updating, and deleting a project
    path('project/<int:id>/', views.ProjectView.as_view(), name='retrieve-update-delete-project'),
    
    # Endpoint for creating an issue under a project
    path('project/<int:project_id>/create-issue/', views.CreateIssueView.as_view(), name='create-issue'),
    
    # Endpoint for retrieving, updating, and deleting an issue
    path('issue/<int:issue_id>/', views.IssueView.as_view(), name='retrieve-update-delete-issue'),
    
    # Endpoint for creating a comment on an issue
    path('issue/<int:issue_id>/create-comment/', views.CreateCommentView.as_view(), name='comment-create'),
    
    # Endpoint for retrieving, updating, and deleting a comment
    path('comment/<int:pk>/', views.CommentView.as_view(), name='retrieve-update-delete-comment'),
]
