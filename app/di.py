import importlib
import inspect
from functools import update_wrapper
from django.conf import settings
from django.utils.decorators import classonlymethod


class InjectedViewMixin:
    @classonlymethod
    def as_injected_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(request, *args, **kwargs):
            dependencies = resolve_dependencies_for_class(cls)
            merged_kwargs = {**initkwargs, **dependencies}
            self = cls(**merged_kwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)
        view.view_class = cls
        view.view_initkwargs = initkwargs

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view


def resolve_dependencies_for_class(cls):
    init_args = set(inspect.signature(cls).parameters.keys())
    init_args.discard('args')
    init_args.discard('kwargs')

    module_name = settings.DEPENDENCY_INJECTION_RESOLVER
    obj_root_module = importlib.import_module(module_name)
    full_name = f'{cls.__module__}.{cls.__name__}'
    short_fn_name = 'resolve_{}'.format(cls.__name__)
    long_fn_name = 'resolve_{}'.format(full_name.replace('.', '_'))

    # find the right runction
    fn = None
    resolved = {}
    lookup_list = [long_fn_name, short_fn_name, 'resolve_common']
    for f in lookup_list:
        if hasattr(obj_root_module, f):
            fn = getattr(obj_root_module, f)
            result = fn(init_args)
            if type(result) is not dict:
                raise TypeError(f"Expected {fn.__name__} to return dict, got {type(result)}")
            resolved = {**result, **resolved}

    # filter dependencies by class params
    dependencies = {}
    for p in init_args:
        try:
            dependencies[p] = resolved[p]
        except KeyError:
            raise ValueError(f'Cannot resolve {cls.__name__} argument {p} in {lookup_list}')

    return dependencies


def resolve(callableClass):
    kwargs = resolve_dependencies_for_class(callableClass)
    return callableClass(**kwargs)