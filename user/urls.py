from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path("sign/", views.UserSignView.as_view(), name="sign"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    # refresh token으로 post요청. 토큰 확인. 유효할시 200. {"access":"<토큰문자열>"}
    # 유효하지 않을시 401 {"detail":"설명", "code":"token_not_valid"}
    path("verify/", TokenVerifyView.as_view(), name="verify"),
    # access token으로 post요청. 토큰이 expire하지 않았는지 확인. 유효할시 200.
    # 유효하지 않을시 401 {"detail":"설명", "code":"token_not_valid"}
]
