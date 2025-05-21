from django.db import models
from accounts.models import User
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    CATEGORIES = (
        ('news', 'Новости'),
        ('guides', 'Гайды'),
        ('creations', 'Творчество'),
        ('bugs', 'Отчёты об ошибках'),
        ('ideas', 'Идеи'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # добавлено поле slug
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # генерируем slug из title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class PostRating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField()  # e.g., -1, 0, 1
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')
