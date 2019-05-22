from django.db import models
from django.contrib.auth.models import User
from di import resolve


class TodoTitleGenerator:
    def __init__(self, title_prefix, now):
        '''
        Another example of DI. We use this class to
        generate titles for todos. 

        __init__ will be called once on application startup
        '''
        self.title_prefix = title_prefix
        self.now = now

    def __call__(self):
        '''
        This method is required, because models.CharField
        default arg expects a callable
        '''
        return '{}-{}'.format(self.title_prefix, self.now())


class TodoManager(models.Manager):
    def get_all_todos(self):
        return super().get_queryset()

    def get_user_todos(self, owner_id):
        return super().get_queryset().filter(owner_id=owner_id)

    def get_user_todos_count(self, owner_id):
        return super().get_queryset().filter(owner_id=owner_id).count()


class Todo(models.Model):
    title = models.CharField(max_length=200,
                             default=resolve(TodoTitleGenerator))
    due_date = models.DateTimeField(null=True, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = TodoManager()

    def is_overdue(self):
        # this method is not testable unless you use
        # FreezeGun or simiar to mock datetime
        from datetime import datetime
        return self.due_date > datetime.now()


class TodoService:
    def __init__(self, now_fn):
        self.now_fn = now_fn

    def is_overdue(self, todo):
        return todo.due_date > self.now_fn()

