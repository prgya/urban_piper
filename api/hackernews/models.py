from django.db import models

# Create your models here.

class hackernews(models.Model):

	story_id = models.CharField(max_length=20, primary_key=True)
	username = models.CharField(max_length=40)
	title = models.TextField()
	sentiment = models.CharField(max_length=20)
	url = models.TextField(max_length=100)
	upvotes = models.IntegerField()
	
	
	class Meta:
		db_table = "app_hackernews"
	
	# def __str__(self):
	# 	return '{}-{}-{} {} {} {}'.format(self.story_id,self.username,self.title,self.sentiment,self.url,self.upvotes)