from django.db import models
from django.contrib.auth.models import User

JOB_CHOICES = (
    ('مشاور','مشاور'),
    ('ناظر', 'ناظر')
)

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    meli_code = models.IntegerField(unique=True, default=0)
    job = models.CharField(max_length=8, choices=JOB_CHOICES, default='مشاور')

    def __str__(self):
        return self.job

