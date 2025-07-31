from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone


# Create your models here.

class Profile(models.Model):
    class RelationToPCGF2(models.TextChoices):
        PARENT = "parent", "Parent of PCGF2"
        AFFECTED = "affected", "Person with PCGF2"
        MED_PRO = "medpro", "Medical Professional"
        SIBLING = "sibling", "Sibling of PCGF2"

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    relation_to_PCGF2 = models.CharField(max_length=30, choices=RelationToPCGF2, blank=True, null=True, help_text="How user relates to PCGF2")
    profile_photo = CloudinaryField("image", blank=True, null=True, folder="static\images\PCGF2_defult_profile.png")
    email = models.EmailField(blank=True, null=True, unique=True)
    password = models.CharField(("password"), max_length=128)
    verified = models.BooleanField(default=False)
    joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email or "Unnamed Profile"

    def get_relation_display(self):
        return self.get_relation_to_pcgf2_display()
