from django.urls import path, re_path

from . import views


app_name = 'chat'

urlpatterns = [
    path('', views.ChatListView.as_view()),
    path('<pk>', views.ChatDetailView.as_view()),
]
