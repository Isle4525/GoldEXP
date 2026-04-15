from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('<int:pk>/rate/<int:value>/', views.rate_post, name='rate_post'),
    path('category/<str:category>/', views.post_list, name='post_list_category'),
    path('tag/<str:tag>/', views.post_list, name='post_list_tag'),
]