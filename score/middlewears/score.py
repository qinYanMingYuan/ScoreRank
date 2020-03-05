from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect, reverse


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user:
            return
        return redirect(reverse('score:login'))



