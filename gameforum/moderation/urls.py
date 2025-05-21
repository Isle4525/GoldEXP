from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('reports/', views.report_list, name='report_list'),  # исправлено с reports_list
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('resolve/<int:report_id>/', views.resolve_report, name='resolve_report'),
    path('ban/<int:user_id>/', views.ban_user, name='ban_user'),
    path('unban/<int:user_id>/', views.unban_user, name='unban_user'),
    path('delete/post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete/comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
