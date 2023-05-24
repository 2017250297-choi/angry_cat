from django.urls import path
from article import views

urlpatterns = [
    path("", views.ArticleView.as_view(), name="article"),
    path("<int:article_id>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("<int:article_id>/like/", views.LikeView.as_view(), name="like"),
    path("<int:article_id>/bookmark/", views.BookmarkView.as_view(), name="bookmark"),
]
