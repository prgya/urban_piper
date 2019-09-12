import json
import requests
from django.shortcuts import render
from rest_framework import generics
from .models import hackernews
from .serializers import NewsSerializer


class ListTopNews(generics.ListAPIView):
    top_news_response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty').json()
    top_ten_id = top_news_response[:10]

    header = {
    	"Accept": "application/json",
    	"Content-type": "application/x-www-form-urlencoded",
    	"X-AYLIEN-TextAPI-Application-Key":"ad28144f0c72d534a81f24c548c9c6c1",
    	"X-AYLIEN-TextAPI-Application-ID":"d39a3fa1"}

    stored_ids = hackernews.objects.values('story_id')
    for i in top_ten_id:
        if i not in stored_ids:
            url = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(i)
            story_details = requests.get(url).json()
            tmp_var = story_details[u'title']
            tmp_url="url not found"
            if story_details[u'url']:
                tmp_url=story_details[u'url']
            sentiment_analysis =  requests.post('https://api.aylien.com/api/v1/sentiment',headers = header, params={'text':tmp_var,'mode':'tweet'}).json()
            sentiment = sentiment_analysis[u'polarity']
            hckr = hackernews(story_id = story_details[u'id'], username=story_details['by'], title=story_details[u'title'], sentiment=sentiment, upvotes = story_details[u'score'], url = tmp_url)
            hckr.save()
    queryset = hackernews.objects.filter(story_id__in=top_ten_id)
    serializer_class = NewsSerializer


def search(request):
    fetched_detail = {}
    flag = 0
    if 'searched_text' in request.GET:
        #request.GET['searched_text']:
        result = request.GET['searched_text']
        try:
            response = hackernews.objects.get(title=result)
            fetched_detail=response
            flag = 1
        except hackernews.DoesNotExist:
            flag = -1
            fetched_detail={}
    return render(request, 'search.html', {'fetched_detail': fetched_detail, 'flag':flag})
