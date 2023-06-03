from django.shortcuts import render
from django.http import HttpResponse


def print_http_request(request):
    print("HttpRequest headers:\n", request.headers)
    print("HttpRequest scheme:\n", request.scheme)
    print("HttpRequest body:\n", request.body)
    print("HttpRequest path:\n", request.path)
    print("HttpRequest path_info:\n", request.path_info)
    print("HttpRequest method:\n", request.method)
    print("HttpRequest encoding:\n", request.encoding)
    print("HttpRequest GET:\n", request.GET)
    print("HttpRequest POST:\n", request.POST)
    # print("HttpRequest META:\n", request.META)  # need DB
    # print("HttpRequest session:\n", request.session)
    # print("HttpRequest user:\n", request.user)
    print("HttpRequest get_host():\n", request.get_host())
    print("HttpRequest get_full_path():\n", request.get_full_path())
    print("HttpRequest build_absolute_uri():\n", request.build_absolute_uri())
    # print("HttpRequest get_signed_cookie():\n", request.get_signed_cookie("name"))  # need security - HTTPS, etc


def index(request):
    print_http_request(request)
    return HttpResponse("Hello, world! You are in the polls index.")
