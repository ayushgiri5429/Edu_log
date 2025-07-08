from django.urls import path
from .views import chat_response, chat_page

urlpatterns = [
    path('', chat_page, name='chat_page'),           # Chat UI page: /chatbot/
    path('chat/', chat_response, name='chat_response'),  # Chatbot API: /chatbot/chat/
]
