from django.db import models

class Exotic(models.Model):
    EXOTIC_TYPES=[
        ('weapon', 'Weapon'),
        ('armor', 'Armor')
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=EXOTIC_TYPES)

    def __str__(self):
        return f"Exotic: {self.name} | Type: {self.type}"