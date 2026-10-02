from django.db import models
from django.conf import settings
from django.urls import reverse


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.CharField(max_length=240)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    poster = models.ImageField(upload_to="posters/", blank=True)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="events",
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"slug": self.slug})
