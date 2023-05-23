from rest_framework import permissions


class IsAuthenticatedOrReadOrSignUp(permissions.BasePermission):
    def has_permission(self, request, view):
        """UserSingview 전용 퍼미션
        
        UserSingview는 GET과 POST(회원가입)요청을 허용해야 합니다.
        이외에는 로그인 여부를 확인합니다.
        
        Returns:
            True: GET, POST요청이거나 로그인 정상
            False: 그외의 경우
        """
        return bool(
            request.method in ('GET', 'POST') or
            request.user and
            request.user.is_authenticated
        )