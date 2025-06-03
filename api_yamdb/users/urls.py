from django.urls import path
# Код из этого файла стоит унести в api/urls.py, т.к. именно там мы прописываем все, что связано с API
from api.views import signup, token

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token'),
]
