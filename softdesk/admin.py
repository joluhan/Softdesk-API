from django.contrib import admin
from softdesk.models import Comment, Issue, Project, ProjectContributor

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectContributor)
admin.site.register(Issue)
admin.site.register(Comment)