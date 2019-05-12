from django.db import models
from django.utils import timezone
import markdown


class Topic(models.Model):
	"""Model for topics of blog"""
	title = models.CharField(max_length=500, unique=True, verbose_name='наименованием')
	image = models.ImageField(upload_to='themes/', default='/SET_DEFAULT/')

	def __str__(self):
		return self.title

	def image_url(self):
		if self.image == '/SET_DEFAULT/':
			return '/static/default_images/hashtag-black.jpg'
		else:
			return self.image.url

	class Meta(object):
		verbose_name = 'Тематика'


class Post(models.Model):
	"""Model for publications of blog"""
	author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	title = models.CharField(max_length=500)
	text = models.TextField()
	create_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	published = models.BooleanField(default=False, verbose_name='Опубликовать')
	topics = models.ManyToManyField(Topic, verbose_name='Тематика публикации')
	image = models.ImageField(upload_to='posts/', default='/SET_DEFAULT/')

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def from_markdown(self):
		return markdown.markdown(self.text)

	def __str__(self):
		return self.title

	def image_url(self):
		if self.image == '/SET_DEFAULT/':
			return '/static/default_images/post-default-image.jpg'
		else:
			return self.image.url
			
		

# Create your models here.
