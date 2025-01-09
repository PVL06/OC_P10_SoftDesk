from django.db import models


class Project(models.Model):

    class ProjectType(models.TextChoices):
        BACKEND = 'BKE'
        FRONTEND = 'FTE'
        IOS = 'IOS'
        ANDROID = 'AND'

    project_name = models.CharField(max_length=64)
    description = models.CharField(max_length=3000)
    type = models.CharField(choices=ProjectType.choices, max_length=5)
    author = models.ForeignKey('UserAuth.User', on_delete=models.CASCADE, related_name='author')
    created_time = models.DateTimeField(auto_now_add=True)

