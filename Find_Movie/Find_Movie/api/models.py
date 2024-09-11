from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model


class User(AbstractUser):
    # Podesi related_name za grupe i dozvole da izbegneš konflikte
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', null=True, blank=True)

    # Ostatak modela...


class SavedMovie(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'saved_movies'

    def __str__(self):
        return f"Movie {self.movie_id} saved by {self.user.username}"
