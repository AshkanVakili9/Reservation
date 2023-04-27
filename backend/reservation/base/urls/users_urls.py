from django.urls import path
from reservation.base.views import user_views as views



urlpatterns = [
    
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),


    path('register/', views.registerUser, name='register'),
    path('verifycode/', views.verifyCode, name='verify-sms-code'),
    path('sendSms/', views.sendSms, name='send-sms-code'),
    
    path('profile/', views.getUserProfile, name='user-profile'),
    path('profile/update/', views.updateUserProfile, name='user-profile-update'),
    path('', views.getUsers, name='users'),
    
    path('<str:pk>/', views.getUserById, name='user'), 
    
    # only admin can use this one      
    path('update/<str:pk>/', views.updateUser, name='user-update'),       
    
    path('delete/<str:pk>/', views.deleteUser, name='user-delete'),
]
