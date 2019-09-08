from django.contrib import admin
from django.urls import path
from .views import ListTopNews

urlpatterns = [
    path('hackernews/top_news', ListTopNews.as_view())
    #path('', include('hackernews.urls'))
]
