from todos.models import Todo, TodoManager


class CreateNewTodo:
    def execute(self, title, owner, due_date=None):
        new_todo = Todo.objects.create(title=title, owner=owner, due_date=due_date)
        return new_todo


class ListAllTodos:
    def execute(self):
        return Todo.objects.all()


class ListOwnTodos:
    def execute(self, owner_id):
        return Todo.objects.get_user_todos(owner_id)

class ListOwnOverdueTodos:
    def execute(self, owner_id, now):
        return Todo.objects.get_user_todos(owner_id).filter(due_date__lt=now)