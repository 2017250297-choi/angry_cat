from django.urls import path
from user import views

urlpatterns = [
    path("sign/", views.UserSignView.as_view(), name="sign"),
]
