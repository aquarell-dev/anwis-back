from django.urls import path

from .views import (
    OrderListCreateView, OrderRetrieveView, OrderUpdateView, OrderPartialUpdateView,

    ChinaDistributorView, ChinaDistributorRetrieveDestroyUpdateView,

    OrderForProjectRetrieveDestroyUpdateView, OrderForProjectView,

    StatusView,

    IndividualEntrepreneurView,

    ProductListCreateView, ProductUpdateView,

    CategoryListCreateView, CategoryRetrieveUpdateDestroyView,

    TaskListCreateView,

    FormExcelView,
)

urlpatterns = [
    path('orders/', OrderListCreateView.as_view()),
    path('orders/<int:pk>/', OrderRetrieveView.as_view()),
    path('order/<int:pk>/', OrderUpdateView.as_view()),
    path('order/partial/<int:pk>/', OrderPartialUpdateView.as_view()),

    path('china-distributors/', ChinaDistributorView.as_view()),
    path('china-distributors/<int:pk>/', ChinaDistributorRetrieveDestroyUpdateView.as_view()),

    path('order-for-projects/', OrderForProjectView.as_view()),
    path('order-for-projects/<int:pk>/', OrderForProjectRetrieveDestroyUpdateView.as_view()),

    path('statuses/', StatusView.as_view()),

    path('individual-entrepreneurs/', IndividualEntrepreneurView.as_view()),

    path('products/', ProductListCreateView.as_view()),
    path('products/<int:pk>/', ProductUpdateView.as_view()),

    path('form-excel/', FormExcelView.as_view()),

    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view()),

    path('tasks/', TaskListCreateView.as_view()),
]
