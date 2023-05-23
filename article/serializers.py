from rest_framework import serializers
from article.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """ArticleSerializer: Article의 상세정보

    Article을 상세조회하여 모든 정보를 조회할때 사용합니다.

    Attributes:
        created_at (DateTime): 작성일의 형식을 바꿔 표현합니다.
        author (str): 작성자 username
        author (int): 작성자 id(pk)
        likes_count (int): 좋아요 수
        comment_count (int): 댓글 수
    """

    created_at = serializers.DateTimeField(format="%m월%d일 %H:%M", read_only=True)
    author = serializers.SerializerMethodField()
    author_id = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        """get_comment_count 댓글 갯수세기

        댓글의 수를 int형태로 출력합니다.

        Args:
            obj (Article): ORM객체
        Return:
            (int): 댓글을 역참조해 그 갯수를 센만큼의 값을 반환합니다.
        Raises:
            없음
        """
        return obj.comment_set.count()

    def get_author(self, obj):
        """get_author 작성자 username 가져오기

        작성자의 username을 가져옵니다.

        Args:
            obj (Article): ORM객체
        Return:
            (str): 작성자 username 반환합니다.
        Raises:
            없음
        """
        return obj.author.username

    def get_author_id(self, obj):
        """get_author_id 작성자 id 가져오기

        작성자의 id를 가져옵니다.

        Args:
            obj (Article): ORM객체
        Return:
            (str): 작성자 id 반환합니다.
        Raises:
            없음
        """
        return obj.author.id

    def get_likes_count(self, obj):
        """get_comment_count 댓글 갯수세기

        좋아요 수를 int형태로 출력합니다.

        Args:
            obj (Article): ORM객체
        Return:
            (int): 게시글의 like필드를 참조해 쿼리셋의 길이만큼의 값을 반환합니다.
        Raises:
            없음
        """
        return obj.likes.count()

    class Meta:
        model = Article
        fields = "__all__"


class ArticleListSerializer(ArticleSerializer):
    """ArticleListSerializer: Article의 개략적인 정보

    Article의 일부 정보만 조회하여 목록을 형성할 때 사용합니다.
    """

    class Meta:
        """
        id는 aticle_id 입니다.
        """

        model = Article
        fields = (
            "id",
            "author_id",
            "title",
            "author",
            "likes_count",
            "comment_count",
            "created_at",
            "image",
        )


class ArticleEditSerializer(serializers.ModelSerializer):
    """ArticleEditSerializer: Article의 title,description,cat_says 수정

    Article의 정보 중 title, description, cat_says만 수정할 수 있도록 제한된 시리얼라이저입니다.
    """

    class Meta:
        model = Article
        fields = (
            "title",
            "description",
            "cat_says",
        )


class ArticleCreateSerializer(serializers.ModelSerializer):
    """ArticleCreateSerializer Article 최초 작성시 사용

    게시글을 작성할 때 사용합니다, title, description, origin_image, image, cat_says 값이 필요합니다.
    """

    class Meta:
        model = Article
        fields = (
            "title",
            "description",
            "origin_image",
            "image",
            "cat_says",
        )
