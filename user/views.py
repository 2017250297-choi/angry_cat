from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from user.serializers import (
    UserSerializer,
    UserSignOutSerializer,
)
from rest_framework.generics import get_object_or_404
from user.models import User


class UserSignView(APIView):
    """유저 가입 뷰

    회원가입, 탈퇴, 유저정보 조회, 유저정보 수정을 처리하는 View입니다.
    """

    def post(self, request):
        """회원가입

        post요청과 username, email, password, password2를 입력받습니다.
        입력 값을 검사하여, 정상 시 유저를 생성합니다.
        
        Returns:
            상태코드 201: 회원가입성공. "회원가입성공" 메세지 반환.
            상태코드 400: 입력값 에러. (serialized.error메세지)
        """
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response({"message": "회원가입성공"}, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """회원탈퇴
        
        put요청과 password를 입력받습니다.
        현재 로그인 중인 유저(request.user)를 찾고 password를 검사합니다.
        정상 시 해당 유저의 is_active 값을 False로 바꾸어 저장합니다.
        
        Returns:
            상태코드 200: 탈퇴성공. "회원탈퇴성공" 메세지 반환.
            상태코드 400: 비밀번호 틀림.
            상태코드 401: 만료토큰/로그인안함.
            상태코드 404: 유저가 없음.
        """
        user = request.user
        user = get_object_or_404(User, id=user.id)
        serializer = UserSignOutSerializer(user, request.data)
        if serializer.is_valid():
            user.is_active = False
            user.save()
            return Response({"message": "회원탈퇴성공"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)