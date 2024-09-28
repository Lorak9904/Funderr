from django.db import models


# create event model here
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    partners = models.CharField(max_length=255, null=True, blank=True)
    

    def __str__(self):
        return self.name