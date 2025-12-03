from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.


def welcome(req):
    return HttpResponse("welcome to mani app from render")


def sample(req):
    return JsonResponse({"msg":"json response from render"})