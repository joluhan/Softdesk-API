# Import the admin module from Django.contrib package.
from django.contrib import admin
# Import the models Comment, Issue, Project, and ProjectContributor from the softdesk.models module.
from softdesk.models import Comment, Issue, Project, ProjectContributor

# Register the models Project, ProjectContributor, Issue, and Comment with the admin site.
admin.site.register(Project)
admin.site.register(ProjectContributor)
admin.site.register(Issue)
admin.site.register(Comment)
