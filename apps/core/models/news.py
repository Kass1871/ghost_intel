from django.db import models
from .base import Base

class News(Base):
    CATEGORY_CHOICES = [
        ('patch', 'Patch Notes'),
        ('event', 'Event'),
        ('announcement', 'Announcement'),
        ('update', 'Update'),
        ('weekly', 'Weekly Reset'),
    ]

    anon_edit_token = models.UUIDField(null=True, blank=True, editable=False, unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, blank=True)
    source = models.CharField(max_length=100, blank=True)
    isGameBreaking = models.BooleanField(default=False)
    relatedContent = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        base = super().__str__()
        return (
            f"{base} | "
            f"Category: {self.category} | "
            f"Breaking: {self.isGameBreaking} | "
            f"Source: {self.source}"
        )