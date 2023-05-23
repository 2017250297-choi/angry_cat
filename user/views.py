from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from user.serializers import UserSerializer


class UserSignView(APIView):
    """유저 가입 뷰

    회원가입, 탈퇴, 유저정보 조회, 유저정보 수정을 처리하는 View입니다.
    """

    def post(self, request):
        """회원가입

        post요청과 username, email, password, password2를 입력받습니다.
        정상 시 201 상태코드 / "회원가입성공" 메세지를 반환합니다.
        비정상 시 400 / error내용을 반환합니다.
        """
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response({"message": "회원가입성공"}, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
