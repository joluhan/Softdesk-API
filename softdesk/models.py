from django.db import models
from accounts.models import User
from django.utils.translation import gettext as _

# Create your models here.

# project model
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
    creator = models.ForeignKey(User, verbose_name=_("author"), on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField()
    project_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

# project contributor model
class ProjectContributor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.contributor.username} - {self.project.name}"


# issue model
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
    project =  models.ForeignKey(Project, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    tag = models.CharField(max_length=50, choices=TAG_CHOICES, default='Task')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='To Do')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# comment model
class Comment(models.Model):
    creator = models.ForeignKey(User ,on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue ,verbose_name="related issue" ,on_delete=models.CASCADE )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.comment