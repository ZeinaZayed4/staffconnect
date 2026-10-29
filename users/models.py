from django.db import models
from django.conf import settings
from django.templatetags.static import static


class Profile(models.Model):
    class Department(models.TextChoices):
        HR = "HR", "Human Resources"
        IT = "IT", "Information Technology"
        FINANCE = "FIN", "Finance"
        MARKETING = "MKT", "Marketing"
        SALES = "SAL", "Sales"
        OPERATIONS = "OPS", "Operations"
        OTHER = "OTH", "Other"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    department = models.CharField(
        max_length=3,
        choices=Department.choices,
        default=Department.OTHER,
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static("img/default_avatar.png")
    
