from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth.models import User
from todos.models import Todo
from todos.use_cases import CreateNewTodo, ListAllTodos, ListOwnTodos


# # Integration Tests, we are using a database
# class CreateNewTodoTestCase(TestCase):
#     def setUp(self):
#         self.owner = User.objects.create_user(username='John')

#     def test_create_todo(self):
#         use_case = CreateNewTodo()
#         result = use_case.execute(title='Run unit tests', owner=self.owner)

#         self.assertIsNotNone(result.id)
#         self.assertEqual(result.title, 'Run unit tests')
#         self.assertEqual(result.owner_id, self.owner.id)


# class ListTodosTestCase(TestCase):
#     def setUp(self):
#         Todo.objects.create(title='Todo #1', owner_id=1)
#         Todo.objects.create(title='Todo #2', owner_id=2)

#     def test_list_all_todos(self):
#         use_case = ListAllTodos()
#         result = use_case.execute()
#         self.assertEqual(len(result), 2)

#     def test_list_own_todos(self):
#         use_case = ListOwnTodos()
#         result = use_case.execute(owner_id=1)
#         self.assertEqual(len(result), 1)


from django.conf import settings


@override_settings(DEPENDENCY_INJECTION_RESOLVER='obj_roots_test')
class IntegrationTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.content, b'index testService1 testService2')

    def test_default_fields_in_model(self):
        from obj_roots_test import fake_datetime
        
        x = Todo.objects.create(owner_id=1)
        self.assertEqual(x.title, '2018-01-01')
        
        fake_datetime.current_time = '2019-01-01'
        x = Todo.objects.create(owner_id=2)
        self.assertEqual(x.title, '2019-01-01')



    