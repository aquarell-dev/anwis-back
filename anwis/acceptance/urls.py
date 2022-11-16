from django.urls import path

from acceptance.views import AcceptanceListCreateView, AcceptanceRetrieveUpdateDestroyView, StaffMemberListCreateView, \
    StaffMemberRetrieveDestroyRetrieveView, ProductListCreateView, AcceptanceCreateFromOrder, AcceptanceUpdateFromOrder

urlpatterns = [
    path('acceptances/', AcceptanceListCreateView.as_view()),
    path('acceptances/<int:pk>/', AcceptanceRetrieveUpdateDestroyView.as_view()),
    path('acceptances/from-order/', AcceptanceCreateFromOrder.as_view()),
    path('acceptances/update/from-order/', AcceptanceUpdateFromOrder.as_view()),

    path('members/', StaffMemberListCreateView.as_view()),
    path('members/<int:pk>/', StaffMemberRetrieveDestroyRetrieveView.as_view()),

    path('acceptance/products/', ProductListCreateView.as_view())
]
