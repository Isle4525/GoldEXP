from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('<int:post_id>/', views.comment_list, name='comment_list'),
    path('add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('reply/<int:comment_id>/', views.reply_comment, name='reply_comment'),
]
