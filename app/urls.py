from django.urls import path
from .views import home_view, search_view, detail_view, result_view

app_name = 'app'

urlpatterns = [
    path('', home_view, name='home'),
    path('search/', search_view, name='search'),
    path('detail/<int:pk>/', detail_view, name='detail'),
    path('result/<str:query>/', result_view, name='result')
]
