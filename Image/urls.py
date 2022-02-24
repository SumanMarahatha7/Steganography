from django.urls import path
from . import views

urlpatterns = [
    path('', views.EncryptImage.as_view(), name='index'),
    path('decrypt/<int:i>', views.DecryptImage.as_view(), name='decrypt')
]
