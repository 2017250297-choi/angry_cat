from django.db import models
from user.models import User


from user.models import User
from ai_process.models import Picture

# Create your models here.


class Article(models.Model):

    """Article 모델

    ai가 변조할 사진, 유저의 설명, ai의 코멘트, 제목 등 을 담습니다.

    Attributes:
        author (ForeignKey): 아이디, 외래키, CASCADE
        title (varchar): 아티클의 제목. 필수입력. 30자 제한, str
        pictures (ForeignKey): Picture객체 id,외래키,CASCADE. 원본이미지와 변경이미지를 저장.
        description (text): 사용자가 작성한 이미지에 대한 설명. 필수입력.
        cat_says (text): GPT가 생성해준 코멘트
        created_at (date): 생성일자
        updated_at (date): 수정일자
        likes (ManyToManyField): 해당 글에 좋아요를 표시한 사용자들(역참조: like_articles)
        bookmarks (ManyToManyField): 해당 글을 북마크한 사용자들(역참조: bookmarked_articles)

    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    pictures = models.OneToOneField(
        Picture, on_delete=models.CASCADE, related_name="article"
    )
    description = models.TextField()
    cat_says = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="like_articles")
    bookmarks = models.ManyToManyField(User, related_name="bookmarked_articles")

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    """Comment 모델

    아티클에대한 사용자의 짧은 의견을 담은 코멘트 모델입니다.

    Attributes:
        author (ForeignKey): 아이디, 외래키, CASCADE
        article (ForeignKey): 댓글이 달린 아티클, 외래키, CASCADE
        content (text): 댓글내용
        created_at (date): 생성일자
        updated_at (date): 수정일자

    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comment_set"
    )
    content = models.TextField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)
