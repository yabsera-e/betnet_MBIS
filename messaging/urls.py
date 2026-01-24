from django.urls import path
from. import views

urlpatterns = [
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('start-conversation/<int:listing_id>/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('send-message/<int:pk>/', views.send_message, name='send_message'),
]
