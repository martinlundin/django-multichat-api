from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.UsernListView.as_view()),
    path('<pk>', views.UsernDetailView.as_view()),
]
