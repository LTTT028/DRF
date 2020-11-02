from django.urls import path

from demo01 import views

urlpatterns = [
    path('users/', views.user),
    path('user_view/', views.UserView.as_view()),
    path('user_view/<str:id>/', views.UserView.as_view()),
    path('userApi/', views.UserAPIView.as_view()),
    path('userApi/<str:id>', views.UserAPIView.as_view()),
]
