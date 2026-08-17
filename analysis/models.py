from django.db import models
from django.contrib.auth.models import User


class Analysis(models.Model):

    ANALYSIS_TYPES = [
        ('summarize', 'Summarize'),
        ('explain', 'Explain'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='analyses'
    )

    title = models.CharField(
        max_length=200
    )

    analysis_type = models.CharField(
        max_length=20,
        choices=ANALYSIS_TYPES
    )

    input_data = models.TextField()

    result = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title