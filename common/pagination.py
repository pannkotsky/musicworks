from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class PaginationWithCountHeader(LimitOffsetPagination):
    def get_paginated_response(self, data):
        headers = {'X-Total-Count': self.count}
        return Response(data, headers=headers)

    def get_paginated_response_schema(self, schema):
        # TODO: debug why it's not applied
        return schema
