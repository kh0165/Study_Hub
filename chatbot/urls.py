from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.chat,
        name='chatbot'
    ),

    path(
        'send/',
        views.send_message,
        name='chatbot_send'
    ),

    path(
        'new/',
        views.new_conversation,
        name='chatbot_new'
    ),

]