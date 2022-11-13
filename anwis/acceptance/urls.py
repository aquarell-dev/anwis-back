from django.urls import path

from acceptance.views import AcceptanceListCreateView, AcceptanceRetrieveUpdateDestroyView, StaffMemberListCreateView, \
    StaffMemberRetrieveDestroyRetrieveView

urlpatterns = [
    path('acceptances/', AcceptanceListCreateView.as_view()),
    path('acceptances/<int:pk>/', AcceptanceRetrieveUpdateDestroyView.as_view()),

    path('members/', StaffMemberListCreateView.as_view()),
    path('members/<int:pk>/', StaffMemberRetrieveDestroyRetrieveView.as_view()),
]
