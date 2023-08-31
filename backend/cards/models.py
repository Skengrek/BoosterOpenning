from django.db import models
from users.models import User

HOLO_CHOICE = [
    ("N", "No Holo"),
    ("H", "Holo")
]


# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=30)

    subType = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=30, null=True)
    superType = models.CharField(max_length=30)

    small_image = models.ImageField(upload_to="images/small/",
                                    default=None,
                                    null=True)
    large_image = models.ImageField(upload_to="images/large/",
                                    default=None,
                                    null=True)
    rarity = models.CharField(max_length=30, null=True)

    number = models.IntegerField()

    extension_id = models.CharField(max_length=10)

    holo_type = models.CharField(
        max_length=2, choices=HOLO_CHOICE, default="N")

    user = models.ManyToManyField(User, blank=True)


class Set(models.Model):
    name = models.CharField(max_length=50)
    series = models.CharField(max_length=50)
    release_date = models.DateField()
    symbol = models.ImageField(
        upload_to="images/Set/symbol",
        default=None,
        null=True
    )
    logo = models.ImageField(
        upload_to="images/Set/Logo",
        default=None,
        null=True
    )
    extension_id = models.CharField(max_length=10)


class Booster(models.Model):
    """
    Represent the number of booster per extension that a User have.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    number = models.IntegerField()
