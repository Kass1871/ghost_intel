from django.db import models

class Weapon(models.Model):
    WEAPON_TYPES=[
        ('primary', 'Primary'),
        ('special', 'Special'),
        ('heavy', 'Heavy')
    ]

    name = models.CharField(max_length=100)
    weapon_type = models.CharField(max_length=50, choices=WEAPON_TYPES)

    def __str__(self):
        return f"Weapon: {self.name} | Type: {self.weapon_type}"