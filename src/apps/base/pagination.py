from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationAPI(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        base = OrderedDict()
        base['count'] = self.page.paginator.count
        base['next'] = self.get_next_link()
        base['previous'] = self.get_previous_link()

        # adiciona summary se existir
        summary = getattr(self, 'summary', None)
        if summary:
            base['summary'] = summary  # fica logo antes de results

        base['results'] = data  # results sempre por último

        return Response(base)
