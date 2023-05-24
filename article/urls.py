from django.urls import path
from article import views


urlpatterns = [
    path("", views.ArticleView.as_view(), name="article"),
    path("<int:article_id>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("<int:article_id>/like/", views.LikeView.as_view(), name="like"),
    path("<int:article_id>/bookmark/", views.BookmarkView.as_view(), name="bookmark"),
    path("<int:article_id>/comment/",views.CommentView.as_view(),name="comment_view"),
    path("<int:article_id>/comment/<int:comment_id>/", views.CommentDetailView.as_view(),name="article_comment_detail_view"),
]

