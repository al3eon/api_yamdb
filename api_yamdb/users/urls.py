from django.urls import path
from api.views import signup, token

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token'),
]
