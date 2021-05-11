from django.urls import path

from .api_views import (
    CategoryAPIView,
    SmartphoneListAPIView,
    NotebookListAPIView,
    SmartphoneDetailAPIView,
    NotebookDetailAPIView,
    CustomersListAPIView,
)

urlpatterns = [
    path(
        'categories/<str:id>/',
        CategoryAPIView.as_view(),
        name='categories'
    ),
    path('smartphones/', SmartphoneListAPIView.as_view(), name='smartphones'),
    path('notebooks/', NotebookListAPIView.as_view(), name='notebooks'),
    path('customers/', CustomersListAPIView.as_view(), name='customers'),
    path(
        'smartphones/<str:id>/',
        SmartphoneDetailAPIView.as_view(),
        name='smartphones_detail'
    ),
    path(
        'notebooks/<str:id>/',
        NotebookDetailAPIView.as_view(),
        name='notebooks_detail'
    ),
]
