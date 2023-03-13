from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('create/', create, name='create'),
    # path('token/', CreateTokenView.as_view(), name='token'),
    # path('me/', ManageUserView.as_view(), name='me'),
]
