from rest_framework.pagination import CursorPagination

class TapChangePagination(CursorPagination):
    page_size = 5
    ordering = '-timestamp'

class PubListPagination(CursorPagination):
    page_size = 10
    ordering = 'name'

class TapListPagination(CursorPagination):
    page_size = 10
    ordering = 'sort_order'

class BeerPagination(CursorPagination):
    page_size = 10
    ordering = 'name'

class WaitingBeerPagination(CursorPagination):
    page_size = 10
    ordering = 'beer'