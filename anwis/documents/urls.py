from django.urls import path

from documents.views import PhotoView, DocumentView

urlpatterns = [
    path('document/', DocumentView.as_view()),
    path('photo/', PhotoView.as_view()),
]
