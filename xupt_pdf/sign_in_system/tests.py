from sign_in_system import models
from django.http import HttpResponse
from django.shortcuts import render


# Create your tests here.


def s(request):
    response = ''
    list = models.Count.objects.all()
    return HttpResponse(list)


def q(request):
    return render(request, '213.html')


def show(request):
    var = request.GET['test']
    print(var)
    return HttpResponse(var)
