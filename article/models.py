from django.db import models
from user.models import User


# Create your models here.
class Article(models.Model):
    """Article 모델

    ai가 변조할 사진, 유저의 설명, ai의 코멘트, 제목 등 을 담습니다.

    Attributes:
        author (ForeignKey): 아이디, 외래키, CASCADE
        title (varchar): 아티클의 제목. 필수입력. 30자 제한, str
        image (Image): AI가 변형한 이미지
        origin_image (Image): AI가 변형하지 않은 이미지
        description (text): 사용자가 작성한 이미지에 대한 설명. 필수입력.
        cat_says (text): GPT가 생성해준 코멘트
        created_at (date): 생성일자
        updated_at (date): 수정일자
        likes (ManyToManyField): 해당 글에 좋아요를 표시한 사용자들(역참조: like_articles)
        bookmarks (ManyToManyField): 해당 글을 북마크한 사용자들(역참조: bookmarked_articles)
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to="%Y/%m/edited/")
    origin_image = models.ImageField(upload_to="%Y/%m/origin/")
    description = models.TextField()
    cat_says = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, related_name="like_articles")
    bookmarks = models.ManyToManyField(User, related_name="bookmarked_articles")

    def __str__(self):
        return str(self.title)


# def()파이썬에서 함수 또는 메소드를 정의하기 위해 사용디는 키워드
#'return self.comment'는 'self.comment' 값을 문자열로 변환하고
# 변환된 문자열을 변환하는 구몬
