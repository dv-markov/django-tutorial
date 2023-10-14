from django.urls import path
from . import views

urlpatterns = [
    path("generate-code/", views.GenerateCodeView.as_view(), name='generate-code'),
    path("verify-code/", views.VerifyCodeView.as_view(), name='verify-view'),
]
