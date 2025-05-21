from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_view, name='conversation'),
    path('new/<int:user_id>/', views.new_conversation, name='new_conversation'),
    path('send/<int:conversation_id>/', views.send_message, name='send_message'),
    path('delete/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
]