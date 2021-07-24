from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish') # FIELD OPTION que previene que tengamos dos entradas con el mismo slug y fecha, en la docu pone que admite **options
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') # Many to One, crea una Foreign Key en la tabla, el related_name nos sirve para sacar todos las instancias de Post del User
    protein = models.IntegerField(default=1)
    carbos = models.IntegerField(default=1)
    fat = models.IntegerField(default=1)
    kcal = models.IntegerField(default=1)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
