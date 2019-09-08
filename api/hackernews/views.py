from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework import generics
from .models import hackernews
from .serializers import NewsSerializer


class ListTopNews(generics.ListAPIView):
	import requests
	import json

	res = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')

	res2 = res.json()
	top_ten_id = res2[:10]

	d = {}

	header = {
		"Accept": "application/json",
		"Content-type": "application/x-www-form-urlencoded",
		"X-AYLIEN-TextAPI-Application-Key":"ad28144f0c72d534a81f24c548c9c6c1",
		"X-AYLIEN-TextAPI-Application-ID":"d39a3fa1"}

	stored_ids = hackernews.objects.values('story_id')

	print(stored_ids)

	print(top_ten_id)

	tmp_lis = []
	for i in top_ten_id:
		if i not in stored_ids:
		
			url1 = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(i)
			tmp = requests.get(url1)
				
			tmp2 = tmp.json()
			tmp_var = tmp2[u'title']
				
				#sentiment analysis
				# https://api.aylien.com/api/v1
			senti =  requests.post('https://api.aylien.com/api/v1/sentiment',headers = header, params={'text':tmp_var,'mode':'tweet'}).json()

			sentiment = senti[u'polarity']

				#print(sentiment.json())
			tmp_lis.append(tmp2[u'id'])
			#d[i] = {'sentiment':sentiment, 'title': tmp2[u'title'], 'by': tmp2[u'by'], 'url' : tmp2[u'url'], 'upvote': tmp2[u'score']}


			hckr = hackernews(story_id = tmp2[u'id'], username=tmp2['by'], title=tmp2[u'title'], sentiment=sentiment, upvotes = tmp2[u'score'], url=tmp2[u'url'])
			hckr.save()

			# top_ten_id
			#import pdb; pdb.set_trace()
	# queryset = hackernews.objects.all()
	#list(Car.objects.filter(id__in=(1,2)))
	queryset = hackernews.objects.filter(story_id__in=top_ten_id) 
	# import pdb; pdb.set_trace()
		
	serializer_class = NewsSerializer
	