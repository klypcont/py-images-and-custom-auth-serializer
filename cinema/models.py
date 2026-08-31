from django.db import models
from django.utils.text import slugify
import uuid
import os


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.rows}x{self.seats_in_row})"

# Убедись, что пустая строка есть в самом конце файла
