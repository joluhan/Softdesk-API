from django.db import models
from accounts.models import User  # Importing the User model from the accounts app
from django.utils.translation import gettext as _  # Importing the gettext function as _

# Create your models here.

# Project model
class Project(models.Model):
    TYPE_CHOICES = (
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('data', 'Data Science'),
        ('ai', 'Artificial Intelligence'),
        ('iot', 'Internet of Things'),
    )
    creator = models.ForeignKey(User, verbose_name=_("author"), on_delete=models.CASCADE)  # ForeignKey relationship with User model, representing the creator of the project
    name = models.CharField(_('name'), max_length=200)  # Name of the project
    description = models.TextField()  # Description of the project
    project_type = models.CharField(max_length=50, choices=TYPE_CHOICES)  # Type of the project chosen from predefined choices
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the project was created

    def __str__(self):
        return self.name  # String representation of the project instance

# Project Contributor model
class ProjectContributor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # ForeignKey relationship with Project model
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey relationship with User model

    def __str__(self):
        return f"{self.contributor.username} - {self.project.name}"  # String representation of the project contributor instance

# Issue model
class Issue(models.Model):
    TAG_CHOICES = (
        ('bug', 'Bug'),
        ('feature', 'Feature'),
        ('task', 'Task')
    )
    STATUS_CHOICES = (
        ('to-do', 'To-Do'),
        ('in progress', 'In Progress'),
        ('finished', 'Finished')
    )
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )
    project =  models.ForeignKey(Project, on_delete=models.CASCADE)  # ForeignKey relationship with Project model
    creator = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey relationship with User model
    name = models.CharField(max_length=100)  # Name of the issue
    description = models.TextField()  # Description of the issue
    tag = models.CharField(max_length=50, choices=TAG_CHOICES, default='Task')  # Tag of the issue chosen from predefined choices
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)  # Priority level of the issue chosen from predefined choices
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='To Do')  # Status of the issue chosen from predefined choices
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to')  # ForeignKey relationship with User model, representing the user to whom the issue is assigned
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the issue was created

    def __str__(self):
        return self.name  # String representation of the issue instance

# Comment model
class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey relationship with User model, representing the creator of the comment
    issue = models.ForeignKey(Issue, verbose_name="related issue", on_delete=models.CASCADE)  # ForeignKey relationship with Issue model, representing the issue to which the comment is related
    comment = models.TextField()  # Text of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the comment was created
    
    def __str__(self):
        return self.comment  # String representation of the comment instance
