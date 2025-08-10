from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('members/', views.members, name='members'),
    path('news/', views.news_list, name='news_list'),
    path('news/search/', views.search_news, name='search_news'),
    path('news/category/<str:category>/', views.news_by_category, name='news_by_category'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('join-clan/', views.join_clan, name='join_clan'),
    path('useful/', views.useful_materials_list, name='useful_materials_list'),
    path('useful/search/', views.search_useful_materials, name='search_useful_materials'),
    path('useful/category/<str:category>/', views.useful_materials_by_category, name='useful_materials_by_category'),
    path('useful/<slug:slug>/', views.useful_material_detail, name='useful_material_detail'),
    path('useful/<slug:slug>/download/', views.download_material, name='download_material'),
] 