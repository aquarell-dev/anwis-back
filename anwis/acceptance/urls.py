from django.urls import path

from acceptance.views import AcceptanceListCreateView, AcceptanceRetrieveUpdateDestroyView, StaffMemberListCreateView, \
    StaffMemberRetrieveDestroyRetrieveView, ProductListCreateView, AcceptanceCreateFromOrder, AcceptanceUpdateFromOrder, \
    CategoryDetailedView, CategoryView, ProductRetrieveDestroyUpdateView, GenerateLabelsView, \
    UpdateProductLeftoversView, \
    UpdateProductColorsView, UpdateMultipleCategoriesView

urlpatterns = [
    path('acceptances/', AcceptanceListCreateView.as_view()),
    path('acceptances/<int:pk>/', AcceptanceRetrieveUpdateDestroyView.as_view()),
    path('acceptances/from-order/', AcceptanceCreateFromOrder.as_view()),
    path('acceptances/update/from-order/', AcceptanceUpdateFromOrder.as_view()),

    path('members/', StaffMemberListCreateView.as_view()),
    path('members/<int:pk>/', StaffMemberRetrieveDestroyRetrieveView.as_view()),

    path('acceptance/products/', ProductListCreateView.as_view()),
    path('acceptance/products/<int:pk>/', ProductRetrieveDestroyUpdateView.as_view()),

    path('acceptance/categories/', CategoryView.as_view()),
    path('acceptance/categories/<int:pk>/', CategoryDetailedView.as_view()),

    path('acceptance/generate-labels/', GenerateLabelsView.as_view()),

    path('acceptance/update-leftovers/', UpdateProductLeftoversView.as_view()),
    path('acceptance/update-colors/', UpdateProductColorsView.as_view()),
    path('acceptance/update-categories/', UpdateMultipleCategoriesView.as_view()),
]
