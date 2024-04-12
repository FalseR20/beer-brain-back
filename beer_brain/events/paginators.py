from rest_framework.pagination import LimitOffsetPagination


class EventsPaginator(LimitOffsetPagination):
    default_limit = 40
    # max_limit = 100
