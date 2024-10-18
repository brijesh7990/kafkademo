from django.urls import path
from .views import *

urlpatterns = [
    path('submit/', UserDataView.as_view(), name='user-create-view')
]
