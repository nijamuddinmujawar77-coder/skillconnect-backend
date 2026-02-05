from django.urls import path
from .views import SubscribeView, ContactView

urlpatterns = [
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('contact/', ContactView.as_view(), name='contact'),
]
