from django.db import models
from django.contrib.auth.models import User


class TodoManager(models.Manager):
    def get_all_todos(self):
        return super().get_queryset()

    def get_user_todos(self, owner_id):
        return super().get_queryset().filter(owner_id=owner_id)

    def get_user_todos_count(self, owner_id):
        return super().get_queryset().filter(owner_id=owner_id).count()



class Todo(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField(null=True, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = TodoManager()
