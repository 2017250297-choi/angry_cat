from rest_framework import status, permissions
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import generics
from article.models import Article, Comment
from article.serializers import (
    ArticleSerializer,
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleEditSerializer,
    CommentCreateSerializer,
    CommentSerializer,
)
from article.permissions import (
    IsOwnerOrReadOnly,
    IsAuthenticatedOrReadOnlyExceptBookMark,
)
from article.paginations import ArticlePagination, CommentPagination
from django.db.models import Count
from datetime import timedelta
from user.models import User
from rest_framework.generics import get_object_or_404
from django.utils import timezone


# Create your views here.
class ArticleView(generics.ListCreateAPIView):
    """ArticleView

    get 요청시 querystring에 따라 원하는 조건에 맞는 게시글의 목록을 불러옵니다.
    post 요청시 게시글을 작성하여 DB에 저장합니다.

    Attributes:
        permission_classes (list): 퍼미션의 리스트
        paginations_class (Pagination): 페이지네이션
        serializer_class (Serializer): 어떤 시리얼라이저를 이용하여 응답 데이터 형성할지 지정
        queryset (QuerySet): 기본으로 get_queryset이 반환할 쿼리 셋(최신순 정렬된 전체게시글)

    """

    permission_classes = [IsAuthenticatedOrReadOnlyExceptBookMark]
    pagination_class = ArticlePagination
    serializer_class = ArticleListSerializer
    queryset = Article.objects.all().order_by("-created_at")

    def trending(self):
        """ArticleView.trending

        3일이내 글들을 좋아요 갯수 순으로 정렬해 보여줍니다.

        Args:
            없음
        Return:
            (QuerySet): Article들중 created_at이 3일이내인 글들을 like_count갯수 내림차순으로 정렬해 반환
        """
        queryset = (
            Article.objects.filter(created_at__gte=timezone.now() - timedelta(days=3))
            .annotate(like_count=Count("likes"))
            .order_by("-like_count", "-created_at")
        )
        return queryset

    def bookmarked(self):
        """ArticleView.bookmarked

        로그인한 유저가 북마크한 글만 모아 최신순으로 보여줍니다.

        Args:
            없음
        Return:
            (QuerySet): request의 user에서 역참조해 bookmarked_articles 전체를 보여줍니다.
            비로그인 유저는 빈 쿼리셋을 반환합니다.
        """
        queryset = self.request.user.bookmarked_articles.all()
        return queryset.order_by("-created_at")

    def of_user(self):
        """ArticleView.of_user

        특정 유저가 작성한 글을 모아 보여줍니다.

        Args:
            없음
        Return:
            (QuerySet): request에서 user_id 쿼리파라미터를 이용해 유저의 작성글을 역참조해 반환
        Raises:
            Http404: 쿼리파라미터가 존재하지 않거나 존재하지 않는 유저 참조 시도
        """
        user_id = int(self.request.GET.get("user_id", 0))
        user = get_object_or_404(User, id=user_id)
        return user.article_set.all().order_by("-created_at")

    def get_queryset(self):
        """ArticleView.get_queryset

        부모클래스의 get_queryset을 커스텀하였습니다.
        url쿼리파라미터를 통해 조회에 걸 조건을 선택합니다.

        Args:
            없음
        Return:
            (QuerySet): 조건에 맞는 쿼리셋을 반환
        Raises:
            Http404: 쿼리파라미터가 존재하지 않거나 존재하지 않는 유저 참조 시도
        """
        query_select = {
            "trending": self.trending,
            "bookmarked": self.bookmarked,
            "user": self.of_user,
        }
        selection = self.request.GET.get("filter", None)
        return query_select.get(selection, super().get_queryset)()

    def post(self, request, *args, **kwargs):
        """ArticleView.post

        request body로 title,description,pictures(Picture모델 객체의 id),cat_says를 받습니다.
        serializer를 통해 검증된 정보를 만들어 Article을 저장합니다.

        정상 시 201 / "작성완료" 메세지를 반환합니다.
        비정상 시 400 / error내용을 반환합니다.
        """
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)

            return Response(
                {"message": "작성완료"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    """ArticleDetailView

    게시글 상세보기, 게시글 수정, 게시글 삭제를 수행합니다.

    Attributes:
        permission (permissions): IsOwnerOrReadOnly은 요청자가 게시글의 작성자일 경우와 아닐 경우를 판단하여 권한을 부여. 기본적으로 읽기 권한만을 주어 게시글을 관리.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, article_id):
        """ArticleDetailView.get

        get요청 시 제시한 article_id의 게시글을 보여줍니다.

        Args:
            article_id (int): 게시글의 id를 지정한다.

        정상 시 200 / ArticleSerializer의 data(created_at,updated_at,author,author_id,likes_count,comment_count,image,origin_image,cat_says,likes,bookmarks)를 json으로 반환
        오류 시 404 / 존재하지않는 게시글 조회
        """
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, article_id):
        """ArticleDetailView.put

        put요청 시 제시한 article_id의 게시글의 title,description,cat_says를 입력받아 수정합니다.

        Args:
            article_id (int): 게시글의 id를 지정한다.

        정상 시 200 / 수정완료 메시지 반환
        오류 시 400 / 올바르지 않은 입력
        오류 시 401 / 권한없음
        오류 시 404 / 존재하지않는 게시글
        """
        article = get_object_or_404(Article, id=article_id)
        self.check_object_permissions(self.request, article)
        serializer = ArticleEditSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "수정완료"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id):
        """ArticleDetailView.delete

        delete요청 시 제시한 article_id의 게시글을 삭제합니다.
        게시글과 연결된 Picture모델도 삭제합니다.

        Args:
            article_id (int): 게시글의 id를 지정한다.

        정상 시 204 / 삭제완료 메시지 반환
        오류 시 401 / 권한없음
        오류 시 404 / 존재하지않는 게시글
        """
        article = get_object_or_404(Article, id=article_id)
        self.check_object_permissions(self.request, article)
        article.pictures.delete()
        article.delete()
        return Response({"message": "삭제완료"}, status=status.HTTP_204_NO_CONTENT)


class LikeView(APIView):
    """LikeView

    게시글 좋아요 기능을 수행합니다.

    Attributes:
        permission (permissions): IsAuthenticated 로그인한 사용자만 접속을 허용합니다.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, article_id):
        """LikeView.post

        post요청 시 제시한 article_id와 일치하는 article의 likes 필드에서 request.user를 넣었다 뺐다 한다.

        Args:
            article_id (int): 게시글의 id를 지정한다.

        정상 시 200 / "unlike했습니다." || "like했습니다." 메시지 반환
        오류 시 401 / 권한없음(비로그인)
        오류 시 404 / 존재하지않는 게시글
        """
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response({"message": "unlike했습니다."}, status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response({"message": "like했습니다."}, status=status.HTTP_200_OK)


class BookmarkView(APIView):
    """BookmarkView

    게시글 북마크 기능을 수행합니다. 유저는 자신이 북마크 한 글만 모아볼 수 있습니다.

    Attributes:
        permission (permissions): IsAuthenticated 로그인한 사용자만 접속을 허용합니다.

    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, article_id):
        """BookmarkView.post

        post요청 시 제시한 article_id와 일치하는 article의 bookmarks 필드에서 request.user를 넣었다 뺐다 한다.

        Args:
            article_id (int): 게시글의 id를 지정한다.

        정상 시 200 / "북마크가 해제되었습니다." || "북마크가 추가되었습니다." 메시지 반환
        오류 시 401 / 권한없음(비로그인)
        오류 시 404 / 존재하지않는 게시글
        """
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.bookmarks.all():
            article.bookmarks.remove(request.user)
            return Response({"message": "북마크가 해제되었습니다."}, status=status.HTTP_200_OK)
        else:
            article.bookmarks.add(request.user)
            return Response({"message": "북마크가 추가되었습니다."}, status=status.HTTP_200_OK)


class CommentView(generics.ListCreateAPIView):
    """CommentView

    get 요청시 querystring에 따라 원하는 조건에 맞는 게시글의 목록을 불러옵니다.
    post 요청시 게시글을 작성하여 DB에 저장합니다.

    Attributes:
        permission_classes (list): 퍼미션의 리스트
        paginations_class (Pagination): 페이지네이션
        serializer_class (Serializer): 어떤 시리얼라이저를 이용하여 응답 데이터 형성할지 지정
        queryset (QuerySet): 기본으로 get_queryset이 반환할 쿼리 셋(최신순 정렬된 전체게시글)

    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CommentPagination
    serializer_class = CommentSerializer
    queryset = None

    def get(self, request, *args, **kwargs):
        """CommentView.get

        get요청 시 제시한 article_id와 일치하는 article의 댓글 목록을 불러옵니다.

        Args:
            article_id (int): 게시글의 id를 지정합니다.

        정상 시 200 / 코멘트 목록 반환
        오류 시 401 / 토큰 만료
        오류 시 404 / 존재하지 않는 게시글
        """
        comments = (
            get_object_or_404(Article, id=kwargs.get("article_id"))
            .comment_set.all()
            .order_by("-created_at")
        )
        self.queryset = comments
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """CommentView.post

        request body로 content를 받습니다.
        path variable로 댓글을 달 article에 접근합니다.

        Args:
            article_id (int): 게시글의 id를 지정합니다.

        정상 시 201 / "작성완료" 메세지를 반환합니다.
        비정상 시 401 / 토큰만료,비로그인
        비정상 시 400 / error내용을 반환합니다.
        """
        serializer = CommentCreateSerializer(
            data=request.data, context={"request": request}
        )
        article = get_object_or_404(Article, id=kwargs.get("article_id"))
        if serializer.is_valid():
            serializer.save(author=request.user, article=article)
            return Response(
                {"message": "작성완료"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    """commentDeatilview
    댓글 수정/삭제를 위한 View입니다.

        Attributes:
            permission_classes (list): 권한설정을 위한 permission클래스들의 리스트입니다. 댓글작성자만 수정/삭제가능하도록 설정되었습니다.

    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def put(self, request, **kwargs):
        """CommentDetailView.put

        댓글 수정.

        KwArg:
            comment_id (int): 수정할 댓글의 id로 지정.

        정상 시 200 / "수정완료" 메시지 반환
        오류 시 401 / 권한없음(비로그인, 만료, 작성자 아님)
        오류 시 400 / 존재하지 않는 댓글
        """
        comment = get_object_or_404(Comment, id=kwargs.get("comment_id"))
        serializer = CommentCreateSerializer(comment, data=request.data)
        self.check_object_permissions(self.request, comment)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "수정완료"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        """CommentDetailView.delete

        댓글 삭제.

        KwArg:
            comment_id (int): 삭제할 댓글의 id로 지정.

        정상 시 200 / "삭제완료" 메시지 반환
        오류 시 401 / 권한없음(비로그인, 만료, 작성자 아님)
        오류 시 400 / 존재하지 않는 댓글
        """
        comment = get_object_or_404(Comment, id=kwargs.get("comment_id"))
        self.check_object_permissions(self.request, comment)
        comment.delete()
        return Response({"message": "삭제완료"}, status=status.HTTP_204_NO_CONTENT)
