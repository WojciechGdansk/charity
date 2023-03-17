from django.db import models
from django.contrib.auth.models import User
# Create your models here.
FUND_CHOICES = [
    (1, "fundacja"),
    (2, "organizacja pozarządowa"),
    (3, "zbiórka lokalna")
]

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Insitution(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(choices=FUND_CHOICES, default=1, max_length=255)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Insitution, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=0, on_delete=models.CASCADE)
