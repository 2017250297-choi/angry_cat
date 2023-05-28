from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from user.models import User
from article.models import Article, Comment
from ai_process.models import Picture


"""article 테스트 요약

총 14개 테스트
1. 게시글 최신순 조회
2. 트렌딩 게시글 조회
3. 북마크 게시글 조회
4. 작성자 게시글 조회
5. 게시글 작성

6. 게시글 상세보기
7. 게시글 수정
8. 게시글 삭제
9. 게시글 좋아요
10. 게시글 북마크

11. 댓글 조회
12. 댓글 생성
13. 댓글 수정
14. 댓글 삭제

15. 멘트생성
16. 이미지생성
"""


class ArticleBaseTestCase(APITestCase):
    """게시글기능 테스트 준비

    게시글기능 테스트를 위한 부모 클래스입니다.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="testuser1",
            email="testuser1@gmail.com",
            password="qhdks111!",
        )
        cls.user_login_data = {"username": "testuser1", "password": "qhdks111!"}

        cls.picture = Picture.objects.create(author=cls.user)
        cls.article = Article.objects.create(author=cls.user, pictures=cls.picture)
        cls.article_create_data = {
            "title": "test",
            "description": "test",
            "cat_says": "test",
        }
        cls.article_edit_data = {
            "title": "edit",
            "description": "edit",
            "cat_says": "edit",
        }

        cls.comment = Comment.objects.create(author=cls.user, article=cls.article)
        cls.comment_create_data = {"content": "test"}
        cls.comment_edit_data = {"content": "edit"}

        image_file = SimpleUploadedFile(
            "test_image.jpg",
            open("static/test_image.jpg", "rb").read(),
            content_type="image/jpeg",
        )
        image_file2 = SimpleUploadedFile(
            "test_image.jpg",
            open("static/test_image.jpg", "rb").read(),
            content_type="image/jpeg",
        )
        cls.pic_gen_test_data = {"input_pic": image_file}
        cls.pic_gen_setup_data = {"input_pic": image_file2}

    def setUp(self) -> None:
        login_user = self.client.post(reverse("token"), self.user_login_data).data
        self.access = login_user["access"]
        self.refresh = login_user["refresh"]

        pic_gen_setup = self.client.post(
            path=reverse("pic_gen"),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=self.pic_gen_setup_data,
        ).data
        self.pic_gen_setup_id = pic_gen_setup["id"]


class ArticleGetTestCase(ArticleBaseTestCase):
    """게시글조회 및 작성 테스트

    게시글조회와 작성을 테스트합니다.
    """

    def test_articles(self):
        """게시글 최신순 조회

        게시글 최신순 조회 테스트입니다.
        """
        url = reverse("article") + "?page=1"
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 200)

    def test_articles_trending(self):
        """트렌딩 게시글 조회

        트렌딩 게시글 조회 테스트입니다.
        """
        url = reverse("article") + "?page=1&filter=trending"
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 200)

    def test_articles_bookmarked(self):
        """북마크 게시글 조회

        북마크 게시글 조회 테스트입니다.
        """
        url = reverse("article") + "?page=1&filter=bookmarked"
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 200)

    def test_articles_user(self):
        """작성자 게시글 조회

        작성자 게시글 조회 테스트입니다.
        """
        url = reverse("article") + "?user=1&filter=user&user_id=1"
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 200)

    def test_article_post(self):
        """게시글 작성

        게시글 작성 테스트입니다.
        """
        url = reverse("article")
        data = self.article_create_data
        data["pictures"] = self.pic_gen_setup_id
        response = self.client.post(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"message": "작성완료"})


class ArticleDetailTestCase(ArticleBaseTestCase):
    """게시글상세 테스트

    게시글상세보기, 수정, 삭제를 테스트합니다.
    """

    def test_article_detail(self):
        """게시글 상세보기

        게시글 상세보기 테스트입니다.
        """
        url = reverse("article_detail", kwargs={"article_id": self.article.id})
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 200)

    def test_article_put(self):
        """게시글 수정

        게시글 수정 테스트입니다.
        """
        url = reverse("article_detail", kwargs={"article_id": self.article.id})
        data = self.article_edit_data
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "수정완료"})

    def test_article_delete(self):
        """게시글 삭제

        게시글 삭제 테스트입니다.
        """
        url = reverse("article_detail", kwargs={"article_id": self.article.id})
        response = self.client.delete(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {"message": "삭제완료"})


class LikeBookMarkTestCase(ArticleBaseTestCase):
    """게시글 좋아요, 북마크 테스트

    게시글 좋아요, 북마크를 테스트합니다.
    """

    def test_article_like(self):
        """게시글 좋아요

        게시글 좋아요 추가 테스트입니다.
        """
        url = reverse("like", kwargs={"article_id": self.article.id})
        response = self.client.post(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "like했습니다."})

    def test_article_bookmark(self):
        """게시글 북마크

        게시글 북마크 추가 테스트입니다.
        """
        url = reverse("bookmark", kwargs={"article_id": self.article.id})
        response = self.client.post(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "북마크가 추가되었습니다."})


class CommentTestCase(ArticleBaseTestCase):
    """댓글 테스트

    댓글 조회, 생성, 수정, 삭제를 테스트합니다.
    """

    def test_comment_list(self):
        """댓글 조회

        댓글 조회 테스트입니다.
        """
        url = (
            reverse("comment_view", kwargs={"article_id": self.article.id}) + "?page=1"
        )
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 200)

    def test_comment_create(self):
        """댓글 생성

        댓글 생성 테스트입니다.
        """
        url = reverse("comment_view", kwargs={"article_id": self.article.id})
        data = self.comment_create_data
        response = self.client.post(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"message": "작성완료"})

    def test_comment_edit(self):
        """댓글 수정

        댓글 수정 테스트입니다.
        """
        url = reverse(
            "article_comment_detail_view", kwargs={"comment_id": self.comment.id}
        )
        data = self.comment_edit_data
        response = self.client.put(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "수정완료"})

    def test_comment_delete(self):
        """댓글 삭제

        댓글 삭제 테스트입니다.
        """
        url = reverse(
            "article_comment_detail_view", kwargs={"comment_id": self.comment.id}
        )
        response = self.client.delete(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {"message": "삭제완료"})


class AiProcessTestCase(ArticleBaseTestCase):
    """AI 처리 테스트

    멘트 생성, 이미지 생성을 테스트합니다.
    """

    def test_mentgen(self):
        """멘트 생성

        멘트 생성 테스트입니다.
        """
        url = reverse("ment_gen")
        data = {"description": "테스트"}
        response = self.client.post(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data,
        )
        self.assertEqual(response.status_code, 200)

    def test_picgen(self):
        """이미지 생성

        이미지 생성 테스트입니다.
        """
        url = reverse("pic_gen")
        data = self.pic_gen_test_data
        response = self.client.post(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
            data=data,
        )
        self.assertEqual(response.status_code, 201)
