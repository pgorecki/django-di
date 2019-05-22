from django.http import HttpResponse
from django.views import View
from di import InjectedViewMixin


class IndexView(View, InjectedViewMixin):
    '''
    InjectedViewMixin adds as_injected_view() method
    see urls.py
    '''
    def __init__(self, service1, service2):
        self.service1 = service1
        self.service2 = service2

    def get(self, request):
        message = f'Hello, using {self.service1} and {self.service2}'
        return HttpResponse(message)
