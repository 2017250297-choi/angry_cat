from rest_framework.pagination import PageNumberPagination

"""
pagination을 커스텀 하거나, 필요한 곳에 지정하여 사용할 수 있습니다.
"""


class ArticlePagination(PageNumberPagination):
    """ArticlePagination: 페이지네이션을 위한 클래스

    Attributes:
        page_size (int): 한 페이지에 몇 개의 게시글을 담을지 결정합니다.
        page_query_param (str): 페이지 이름(query string에서 페이지를 지정할 파라미터) ex)http://127.0.0.1:8000/article/?page=2 를 사용하면 2페이지로 이동
        max_page_size(int): 최대 페이지 수
    """

    page_size = 10
    page_query_param = "page"
    max_page_size = 100
