from django.db import models
from accounts.models import User
from posts.models import Post
from comments.models import Comment

class Report(models.Model):
    REPORT_TYPES = (
        ('spam', 'Спам'),
        ('abuse', 'Оскорбления'),
        ('rules', 'Нарушение правил'),
        ('other', 'Другое'),
    )
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Report on {self.post or self.comment} by {self.reporter}"