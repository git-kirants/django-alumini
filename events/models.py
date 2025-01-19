from django.db import models
from django.utils import timezone
from users.models import User

class Event(models.Model):
    EVENT_TYPES = (
        ('networking', 'Networking Event'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('career_fair', 'Career Fair'),
        ('social', 'Social Gathering'),
        ('other', 'Other'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    registration_deadline = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    participants = models.ManyToManyField(User, through='EventRegistration', related_name='registered_events')

    def __str__(self):
        return self.title

    @property
    def is_past_event(self):
        return timezone.now() > self.date

    @property
    def is_registration_open(self):
        return timezone.now() <= self.registration_deadline

    @property
    def available_spots(self):
        return self.capacity - self.participants.count()

class EventRegistration(models.Model):
    REGISTRATION_STATUS = (
        ('registered', 'Registered'),
        ('waitlisted', 'Waitlisted'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS, default='registered')
    attendance_marked = models.BooleanField(default=False)

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
