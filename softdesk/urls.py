from django.urls import path
from . import views

urlpatterns = [
    path('project/', views.ListProjectsView.as_view({'post': 'create', 'get': 'list'}), name='project-list'),
    path('project/<int:id>/add-contributor/', views.add_contributor, name='add contributor'),
    path('project/<int:id>/remove-contributor/', views.remove_contributor, name='remove contributor'),
    path('project/<int:id>/', views.ProjectView.as_view(), name='retrieve-update-delete-project'),
    path('project/<int:project_id>/create-issue/', views.CreateIssueView.as_view(), name='create-issue'),
    path('issue/<int:issue_id>/', views.IssueView.as_view(), name='retrieve-update-delete-issue'),
    path('issue/<int:issue_id>/create-comment/', views.CreateCommentView.as_view(), name='comment-create'),
    path('comment/<int:id>/', views.CommentView.as_view(), name='retrieve-update-delete-comment'),
]
