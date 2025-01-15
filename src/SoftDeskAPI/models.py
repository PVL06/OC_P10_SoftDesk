from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(UserManager):

    def _create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    age = models.IntegerField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['age', 'can_be_contacted', 'can_data_be_shared']

    def __str__(self):
        return self.username

    @classmethod
    def get_user_by_username(cls, username):
        return cls.objects.get(username=username)


class Project(models.Model):

    class ProjectType(models.TextChoices):
        BACKEND = 'backend'
        FRONTEND = 'frontend'
        IOS = 'ios'
        ANDROID = "android"

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    type = models.CharField(choices=ProjectType.choices, max_length=16)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Contributors(models.Model):

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        name='project_id'
    )
    contributor = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        name='contributor_id'
    )

    class Meta:
        unique_together = ('project_id', 'contributor_id')

    @classmethod
    def check_user_in_project(cls, user, project_pk):
        return cls.objects.filter(
            contributor_id=user,
            project_id=project_pk
        ).exists()
