from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext as _

# Create your models here.

class User(AbstractUser):
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    date_of_birth = models.DateField()
    groups = models.ManyToManyField(Group, verbose_name=_('groups'),
        blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(
        Permission, verbose_name=_('user permissions'),
        blank=True, related_name='custom_user_permissions',
        help_text=_('Specific permissions for this user.'),
    )

    def __str__(self):
        return self.username