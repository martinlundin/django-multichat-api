from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.UsernListView.as_view()),
    #path('create/', views.UsernCreateView.as_view()),
    path('<pk>', views.UsernDetailView.as_view()),
    path('<pk>/update/', views.UsernDetailView.as_view()),
    path('<pk>/delete/', views.UsernDetailView.as_view())
]
