from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify

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
        return f'{self.user.username}-{self.job}'


class Consulation(models.Model):
    author = models.OneToOneField(Employee, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    mashroot_len = models.IntegerField(default=0)
    moadel = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    arzyabi = models.CharField(max_length=20, choices=ARZYABI_CHOICES, default='عادی')
    erja_moshavere_tahsili = models.BooleanField(default=False)
    erja_moshavere_shoghli = models.BooleanField(default=False)
    erja_moshavere_balini = models.BooleanField(default=False)
    nobat = models.DateField(default=timezone.now)
    hozor = models.BooleanField(default=False)
    model_term_baad = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    moshkel_asli = models.TextField(max_length=9000, blank=True)
    neshanehaye_raftari = models.TextField(max_length=9000, blank=True)
    ahdaf_modakhele = models.TextField(max_length=9000, blank=True)
    farayande_modakhele = models.TextField(max_length=9000, blank=True)
    slug = models.SlugField(max_length=200, allow_unicode=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            slug_name = f'{self.author.user.username}-{self.nobat}-{self.pk}'
            self.slug = slugify(slug_name)

        super(Consulation, self).save(*args, **kwargs)

    def __str__(self):
        return self.author.user.username