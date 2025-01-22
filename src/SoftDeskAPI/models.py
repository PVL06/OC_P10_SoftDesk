from django.db import models
from django.contrib.auth import get_user_model
import uuid


class Project(models.Model):
    
    class ProjectType(models.TextChoices):
        BACKEND = 'backend'
        FRONTEND = 'frontend'
        IOS = 'ios'
        ANDROID = "android"

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    type = models.CharField(choices=ProjectType.choices, max_length=16)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Contributors(models.Model):

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='project'
    )
    contributor = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='contributor'
    )

    class Meta:
        unique_together = ('project', 'contributor')

    @classmethod
    def check_user_in_project(cls, user, project_pk):
        return cls.objects.filter(
            contributor_id=user,
            project_id=project_pk
        ).exists()


class Issue(models.Model):

    class PriorityType(models.TextChoices):
        LOW = 'low'
        MEDIUM = 'medium'
        HIGH = 'high'

    class TagType(models.TextChoices):
        BUG = 'bug'
        FEATURE = 'feature'
        TASK = 'task'

    class StatusType(models.TextChoices):
        TODO = 'todo'
        IN_PROGRESS = 'in_progress'
        FINISHED = 'finished'

    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField()
    priority = models.CharField(choices=PriorityType.choices, max_length=16)
    tag = models.CharField(choices=TagType.choices, max_length=16)
    status = models.CharField(choices=StatusType.choices, max_length=16)
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='issue_author'
    )
    assigned_user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='issue_assigned_user'
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @classmethod
    def check_issue_in_project(cls, project_id, issue_id):
        return cls.objects.filter(
            id=issue_id,
            project=project_id
        ).exists()


class Comment(models.Model):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    description = models.TextField()
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='comment_author'
    )
    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name='issue'
    )
    issue_link =  models.URLField()
    created_time = models.DateTimeField(auto_now_add=True)
