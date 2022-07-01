from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 10
    
class WatchListLOPPagination(LimitOffsetPagination):
    default_limit = 5
    offset_query_param = 'start'
    max_limit = 10
    
class WatchListCPagination(CursorPagination):
    page_size = 5
    ordering = 'created'
    cursor_query_param = 'record'
