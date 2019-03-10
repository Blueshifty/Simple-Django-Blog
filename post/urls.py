from django.urls import path
from .views import *

app_name = 'post'

urlpatterns =[
    path('index', post_index, name = 'index' ),
    path('create', post_create, name='create'),
    path('<str:slug>/', post_detail, name='detail') ,
    path('<str:slug>/update', post_update, name = 'update'),
    path('<str:slug>/delete', post_delete, name = 'delete'),
]