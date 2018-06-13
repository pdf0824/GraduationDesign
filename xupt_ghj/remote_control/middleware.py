from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect

try:

    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class LoginFilterMiddleware(MiddlewareMixin):
    def process_request(self, request):

        if 'login' not in request.path and 'reset' not in request.path:
            if request.session.get('user', None):
                pass
            else:
                return HttpResponseRedirect('/login')
        else:
            pass
