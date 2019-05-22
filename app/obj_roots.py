'''
This module contains resolvers for all the classes that use dependency
injection. A path to this module must be provided in settings.py

We are using constructor injection, so all dependencies for
foo.bar.Baz should be provided in any of the following function:
- resolve_foo_bar_Baz
- resolve_Baz
- resolve_common
'''


def resolve_common(expected_params):
    '''
    This function contains all depencies which are shared
    across all classes that use DI
    '''
    import datetime
    return {
        'now': datetime.datetime.now,
        'title_prefix': 'content',
    }


def resolve_IndexView(expected_params):
    '''
    A resolver for IndexView
    '''
    return {
        'service1': 'productionService1',
        'service2': 'productionService2',
    }


def resolve_TodoTitleGenerator(expected_params):
    return {
        'title_prefix': 'todo',
    }
