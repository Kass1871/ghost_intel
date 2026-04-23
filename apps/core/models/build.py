import uuid

from django.contrib.auth.models import User
from django.db import models
from .base import Base

class Build(Base):
    CLASSES = [
        ('titan', 'Titan'),
        ('hunter', 'Hunter'),
        ('warlock', 'Warlock')
    ]

    SUBCLASSES = [
        ('void', 'Void'),
        ('solar', 'Solar'),
        ('arc', 'Arc'),
        ('stasis', 'Stasis'),
        ('strand', 'Strand'),
        ('prismatic', 'Prismatic')
    ]

    BUILD_TYPES = [
        ('pve', 'PvE'),
        ('pvp', 'PvP'),
        ('endgame', 'Endgame'),
        ('raid', 'Raid'),
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    anon_edit_token = models.UUIDField(null=True, blank=True, editable=False, unique=True)
    build_class = models.CharField(max_length=20, choices=CLASSES, blank=False)
    subclass = models.CharField(max_length=20, choices=SUBCLASSES, blank=False)
    build_type = models.CharField(max_length=20, choices=BUILD_TYPES, blank=False)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    exotics = models.ManyToManyField('Exotic', blank=True)
    weapons = models.ManyToManyField('Weapon', blank=True)
    armorMods = models.JSONField(null=True, blank=True)
    statsPriority = models.CharField(max_length=50, blank=True)
    expansion = models.CharField(max_length=50)
    likes = models.ManyToManyField(User, related_name='liked_builds', blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        base = super().__str__()

        exotics = ", ".join(e.name for e in self.exotics.all())
        weapons = ", ".join(w.name for w in self.weapons.all())

        return (
            f"{base} | "
            f"Class: {self.build_class} | "
            f"Subclass: {self.subclass} | "
            f"Type: {self.build_type} | "
            f"Difficulty: {self.difficulty} | "
            f"Expansion: {self.expansion} | "
            f"Exotics: [{exotics}] | "
            f"Weapons: [{weapons}] | "
            f"Views: {self.views}"
        )   