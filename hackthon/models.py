from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = [
        ("citizen", "Citizen"),
        ("officer", "Officer"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="citizen"
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Complaint(models.Model):

    CATEGORY_CHOICES = [
        ("road", "Road & Infrastructure"),
        ("water", "Water Supply"),
        ("electricity", "Electricity"),
        ("waste", "Waste Management"),
        ("fire", "Fire Emergency"),
        ("health", "Healthcare"),
        ("other", "Other"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("analysed", "AI Analysed"),
        ("assigned", "Assigned"),
        ("progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    citizen = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="complaints"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_complaints"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="complaints/",
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="other"
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    ai_summary = models.TextField(
        blank=True
    )

    is_emergency = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submitted"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"#{self.id} - {self.title}"

