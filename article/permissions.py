from rest_framework import permissions


class IsAuthenticatedOrReadOnlyExceptBookMark(permissions.BasePermission):
    """IsAuthenticatedOrReadOnlyExceptBookMark

    북마크 조회를 제외한 GET요청은 비로그인시에도 요청가능합니다.
    북마크 조회와 기타 요청(POST)는 로그인이 필요합니다.
    """

    def has_permission(self, request, view):
        if (
            request.GET.get("filter") == "bookmarked"
            or request.method not in permissions.SAFE_METHODS
        ):
            return bool(request.user and request.user.is_authenticated)
        return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    """IsOwnerOrReadOnly 자신의 글만 수정/삭제가능한 퍼미션

    BasePermission을 상속받아 만들었습니다.
    게시글의 작성자가 request.user와 같은 경우 PUT,PATCH,DELETE 메서드에 대한 권한을 허용합니다.
    이외의 요청자일 경우 읽기 권한만 허용됩니다.

    Attributes:
        message (str): 권한이 없을 경우 message를 오버라이딩하여 권한이 없습니다 가 출력됩니다.
    """

    message = "권한이 없습니다"

    def has_object_permission(self, request, view, obj):
        """has_object_permission

        Args:
            request (request): 요청 데이터
            view (View): view 클래스
            obj (Article): 대상이 되는 Article/Comment ORM객체

        Return:
            (bool): True - 요청의 user가 작성자일 경우, False - 요청의 user가 작성자가 아닐 경우

        Raises:
            없음
        """
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author == request.user
