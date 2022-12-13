from django.urls import path

from .views import (
    OrderListCreateView, OrderRetrieveView, OrderUpdateView, OrderPartialUpdateView,

    ChinaDistributorView, ChinaDistributorRetrieveDestroyUpdateView,

    StatusView,

    ProductListCreateView, ProductUpdateView, ProductRetrieveDestroyView, ProductDestroyMultipleView,

    CategoryListCreateView, CategoryRetrieveUpdateDestroyView,

    FormExcelView,
)

urlpatterns = [
    path('orders/', OrderListCreateView.as_view()),
    path('orders/<int:pk>/', OrderRetrieveView.as_view()),
    path('order/<int:pk>/', OrderUpdateView.as_view()),
    path('order/partial/<int:pk>/', OrderPartialUpdateView.as_view()),

    path('china-distributors/', ChinaDistributorView.as_view()),
    path('china-distributors/<int:pk>/', ChinaDistributorRetrieveDestroyUpdateView.as_view()),

    path('statuses/', StatusView.as_view()),

    path('products/', ProductListCreateView.as_view()),
    path('products/partial/<int:pk>/', ProductUpdateView.as_view()),
    path('products/<int:pk>/', ProductRetrieveDestroyView.as_view()),
    path('products/delete-multiple/', ProductDestroyMultipleView.as_view()),

    path('form-excel/', FormExcelView.as_view()),

    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view()),
]
