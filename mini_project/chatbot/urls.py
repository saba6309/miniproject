from django.urls import path
from .views import send_message, list_messages, home, train_chatbot

urlpatterns = [
    path('', home, name='home'),  # New route for the home page
    path('send', send_message, name='send_message'),
    path('list', list_messages, name='list_messages'),
    path('train', train_chatbot, name='train_chatbot'),  # New route for training
]
