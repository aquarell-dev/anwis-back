from django.urls import path

from .views import OrderListCreateView, ChinaDistributorView, OrderForProjectView, StatusView, \
    IndividualEntrepreneurView, ProductListCreateView, CategoryListCreateView, OrderRetrieveView, OrderUpdateView, TaskListCreateView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view()),
    path('orders/<int:pk>/', OrderRetrieveView.as_view()),
    path('order/<int:pk>/', OrderUpdateView.as_view()),
    path('china-distributors/', ChinaDistributorView.as_view()),
    path('order-for-projects/', OrderForProjectView.as_view()),
    path('statuses/', StatusView.as_view()),
    path('individual-entrepreneurs/', IndividualEntrepreneurView.as_view()),
    path('products/', ProductListCreateView.as_view()),
    path('categories/',  CategoryListCreateView.as_view()),
    path('tasks/', TaskListCreateView.as_view()),
]
