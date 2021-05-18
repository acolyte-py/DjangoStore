from django.urls import path

from .views import (
    BaseView,
    ProductDetailView,
    CategoryDetailView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQTYView,
    CheckoutView,
    MakeOrderView,
    LoginView,
)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path(
        'products/<str:slug>/',
        ProductDetailView.as_view(),
        name='product_detail'
    ),
    path(
        'category/<str:slug>/',
        CategoryDetailView.as_view(),
        name='category_detail'
    ),
    path('cart/', CartView.as_view(), name='cart'),
    path(
        'add-to-cart/<str:slug>/',
        AddToCartView.as_view(),
        name='add_to_cart'
    ),
    path(
        'delete-from-cart/<str:slug>/',
        DeleteFromCartView.as_view(),
        name='delete_from_cart'
    ),
    path(
        'change-qty/<str:slug>/',
        ChangeQTYView.as_view(),
        name='change_qty'
    ),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('login/', LoginView.as_view(), name='login'),
]
