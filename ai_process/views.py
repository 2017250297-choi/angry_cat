from rest_framework import status, permissions
from rest_framework.decorators import APIView
from rest_framework.response import Response
import openai
import os

openai.api_key = os.environ.get("api_key")


class MentgenView(APIView):
    """MentgenView

    chat gpt로 고양이 멘트를 생성합니다.

    Attributes:
        permission (permissions): IsAuthenticated 로그인한 사용자만 접속을 허용합니다.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Mentgen.post

        post요청 시 입력받은 description으로 cat_says를 생성하여 반환합니다.

        정상 시 200 / "unlike했습니다." || "like했습니다." 메시지 반환
        오류 시 401 / 권한없음(비로그인)
        오류 시 404 / 존재하지않는 게시글
        """
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "사진의 제목과 설명을 보고 고양이가 화난 이유를 한문장으로 만들어줘."},
                {"role": "user", "content": request.POST.get("description", "")},
            ],
        )
        message = result.choices[0].message.content
        return Response({"message": message}, status=status.HTTP_200_OK)