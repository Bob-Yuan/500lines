import time

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse


class ReturnView(View):
    def get(self, request):
        str1 = "helloworld"
        time.sleep(15)
        return HttpResponse(str1)
    def post(self, request):
        pass

