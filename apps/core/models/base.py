from django.contrib.auth.models import User
from django.db import models

class Base(models.Model):
    STATUSES=[
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ]

    title = models.TextField()
    slug = models.SlugField(unique=True)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    datePublished = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default='draft')

    class Meta:
        abstract = True

    def __str__(self):
        tags = ", ".join(tag.name for tag in self.tags.all())

        return (
            f"ID: {self.id} | "
            f"Title: {self.title} | "
            f"Slug: {self.slug} | "
            f"Author: {self.author} | "
            f"Tags: [{tags}] | "
            f"Published: {self.datePublished} | "
            f"Status: {self.status}"
        )