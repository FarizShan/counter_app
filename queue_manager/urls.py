from django.urls import path
from queue_manager import views
from django.shortcuts import redirect  # ✅ ADD THIS


urlpatterns = [
    path('', lambda request: redirect('login')),  # root redirect
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('display/', views.display, name='display'),
    path('generate_token/', views.generate_token, name='generate_token'),
    path('api/queue-stats/', views.queue_stats_api, name='queue_stats_api'),
    path("api/start-service/", views.start_service, name="start_service"),
    path('api/complete-service/', views.complete_service, name='complete_service'),

]