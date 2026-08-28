import os
import uuid
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


def movie_image_file_path(instance, filename):
    _, ext = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "movies", filename)


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    image = models.ImageField(null=True, upload_to=movie_image_file_path)
        null=True,
        upload_to=movie_image_file_path,
    )

    def __str__(self):
        return self.title


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="movie_sessions"
    )
    cinema_hall = models.ForeignKey(
        CinemaHall, on_delete=models.CASCADE, related_name="movie_sessions"
    )

    def __str__(self):
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    movie_session = models.ForeignKey(
        MovieSession, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )

    @staticmethod
    def validate_ticket(row, seat, cinema_hall, error_to_raise):
        for ticket_attr_value, ticket_attr_range, ticket_attr_name in [
            (row, cinema_hall.rows, "row"),
            (seat, cinema_hall.seats_in_row, "seat"),
        ]:
            if not (1 <= ticket_attr_value <= ticket_attr_range):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} number must be in available range: (1, {ticket_attr_range})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.movie_session.cinema_hall,
            ValidationError,
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{str(self.movie_session)} (row: {self.row}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ("movie_session", "row", "seat")
