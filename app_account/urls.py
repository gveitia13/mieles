from django.urls import path

from app_account import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path("password-reset/", views.MyPasswordResetView.as_view(), name="my_password_reset"),
]
