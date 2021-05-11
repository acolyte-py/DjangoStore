from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from .serializer import (
    CategorySerializer,
    SmartphoneSerializer,
    NotebookSerializer,
    CustomerSerializer,
)
from ..models import Category, Smartphone, Notebook, Customer


class Pagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count_objects', self.page.paginator.count),
            ('next_item', self.get_next_link()),
            ('previous_item', self.get_previous_link()),
            ('items', data)
        ]))


class CategoryAPIView(ListCreateAPIView, RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    pagination_class = Pagination
    queryset = Category.object.all()
    lookup_field = 'id'


class SmartphoneListAPIView(ListAPIView):
    serializer_class = SmartphoneSerializer
    pagination_class = Pagination
    queryset = Smartphone.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title', 'accum_volume']


class NotebookListAPIView(ListAPIView):
    serializer_class = NotebookSerializer
    pagination_class = Pagination
    queryset = Notebook.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title', 'video']


class SmartphoneDetailAPIView(RetrieveAPIView):
    serializer_class = SmartphoneSerializer
    pagination_class = Pagination
    queryset = Smartphone.objects.all()
    lookup_field = 'id'


class NotebookDetailAPIView(RetrieveAPIView):
    serializer_class = NotebookSerializer
    pagination_class = Pagination
    queryset = Notebook.objects.all()
    lookup_field = 'id'


class CustomersListAPIView(ListAPIView):
    """Это для практики, в реале такой функционал делать не стоит"""
    serializer_class = CustomerSerializer
    pagination_class = Pagination
    queryset = Customer.objects.all()

