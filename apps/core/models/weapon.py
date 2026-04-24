from django.db import models

class Weapon(models.Model):
    WEAPON_TYPES=[
        ('primary', 'Primary'),
        ('special', 'Special'),
        ('heavy', 'Heavy')
    ]

    WEAPON_RARITIES=[
        ('common', 'Common'),
        ('uncommon', 'Uncommon'),
        ('rare', 'Rare'),
        ('legendary', 'Legendary'),
        ('exotic', 'Exotic'),
    ]

    thumbnail = models.ImageField(upload_to='weapons/', blank=True, null=True)
    name = models.CharField(max_length=100)
    weapon_rarity = models.CharField(max_length=20, choices=WEAPON_RARITIES, default='unassigned')
    weapon_type = models.CharField(max_length=50, choices=WEAPON_TYPES)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Weapon: {self.name} | Type: {self.weapon_type}"