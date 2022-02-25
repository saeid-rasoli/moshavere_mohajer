from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

JOB_CHOICES = (
    ('مشاور', 'مشاور'),
    ('ناظر', 'ناظر')
)

ARZYABI_CHOICES = (
    ('عادی', 'عادی'),
    ('وسواس', 'وسواس'),
    ('مضطرب', 'مضطرب')
)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    meli_code = models.IntegerField(unique=True, blank=True)
    job = models.CharField(max_length=8, choices=JOB_CHOICES, default='مشاور')
    is_authorized = models.BooleanField(default=False)

    def __str__(self):
        return self.job


class Consulation(models.Model):
    author = models.OneToOneField(Employee, on_delete=models.CASCADE)
    mashroot_len = models.IntegerField(default=0)
    moadel = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    arzyabi = models.CharField(max_length=20, choices=ARZYABI_CHOICES, default='عادی')
    erja_moshavere_tahsili = models.BooleanField(default=False)
    erja_moshavere_shoghli = models.BooleanField(default=False)
    erja_moshavere_balini = models.BooleanField(default=False)
    nobat = models.DateField(default=timezone.now)
    hozor = models.BooleanField(default=False)
    model_term_baad = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    moshkel_asli = models.TextField(max_length=500, blank=True)
    neshanehaye_raftari = models.TextField(max_length=500, blank=True)
    ahdaf_modakhele = models.TextField(max_length=500, blank=True)
    farayande_modakhele = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.author.user.username