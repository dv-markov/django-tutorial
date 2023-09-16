from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Question


def index(request):
    # return HttpResponse("Hello, world! You are in the polls index.")
    # template = loader.get_template("polls/index.html")
    # return HttpResponse(template.render(context, request))
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." % question_id)
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def index2(request):
    print_http_request(request)
    response = generate_http_response(MyNumbers())
    return response


def print_http_request(request):
    print("HttpRequest headers:\n", request.headers)
    print("HttpRequest scheme:\n", request.scheme)
    print("HttpRequest body:\n", request.body)
    print("HttpRequest path:\n", request.path)
    print("HttpRequest path_info:\n", request.path_info)
    print("HttpRequest method:\n", request.method)
    print("HttpRequest encoding:\n", request.encoding)
    print("HttpRequest content_type:\n", request.content_type)
    print("HttpRequest content_params:\n", request.content_params)
    print("HttpRequest GET:\n", request.GET)
    print("HttpRequest POST:\n", request.POST)
    # print("HttpRequest META:\n", request.META)  # need DB
    # print("HttpRequest session:\n", request.session)
    # print("HttpRequest user:\n", request.user)
    print("HttpRequest get_host():\n", request.get_host())
    print("HttpRequest get_full_path():\n", request.get_full_path())
    print("HttpRequest build_absolute_uri():\n", request.build_absolute_uri())
    # print("HttpRequest get_signed_cookie():\n", request.get_signed_cookie("name"))  # need security - HTTPS, etc


def generate_http_response(content=None):
    # response = HttpResponse("Hello, world! You are in the polls index.")  # минимальный ответ по умолчанию
    # response = HttpResponse("Text only, please.", content_type="text/plain")  # возвращает текст в теге <pre>
    # response = HttpResponse(b"Bytestrings are also accepted.")  # отображается как обычный текст
    response = HttpResponse(memoryview(b"Memoryview as well."))  # отображается как обычный текст

    # works with iterators, string or number
    # response = HttpResponse(content) if content else HttpResponse()

    # response = StreamingHttpResponse(content)  # Streaming type of content

    response.write("<p>Hello World!<p>")  # в response можно писать, как в файл
    response.write("<p>How are you doing?<p>")

    response.headers["Age"] = 120  # работа с headers HttpResponse
    del response.headers["Age"]
    response["Age"] = 120  # equal, proxies to HttpResponse.headers
    # del response["Age"]
    response["Worker"] = "Petrov"

    # returns JSON
    response2 = JsonResponse({"foo": "bar"})
    response2.write({"привет": "Петя"})
    response2.write({"privet": "vasya"})

    return response


class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        if self.a <= 36:
            x = self.a
            self.a += 1
            return str(x) + ' '
        else:
            raise StopIteration
