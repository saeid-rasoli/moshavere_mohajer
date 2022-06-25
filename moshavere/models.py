from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify

TYPE_HAMKARI = (
    ("مدعو", "مدعو"),
    ("رسمی", "رسمی"),
    ("پروژه ای", "پروژه ای"),
    ("قراردادی", "قراردادی"),
)
S_P_B = (
    ("سازمان نظام روانشناسی", "سازمان نظام روانشناسی"),
    ("پروانه اشتغال تخصصی", "پروانه اشتغال تخصصی"),
    ("بهزیستی", "بهزیستی"),
    ("ندارد", "ندارد"),
)


class City(models.Model):
    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهر ها'

    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Daneshkadeh(models.Model):
    class Meta:
        verbose_name = 'دانشکده'
        verbose_name_plural = 'دانشکده ها'

    name = models.CharField(max_length=200, blank=True, null=True)
    daneshgah_code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Time(models.Model):
    class Meta:
        verbose_name = 'زمان'
        verbose_name_plural = 'زمان ها'

    times = models.CharField(max_length=30)

    def __str__(self):
        return self.times


class Days(models.Model):
    class Meta:
        verbose_name = 'روز'
        verbose_name_plural = 'روز ها'

    days = models.CharField(max_length=30)
    times = models.ManyToManyField(Time, blank=True)

    def __str__(self):
        return self.days


class MoshaverProfile(models.Model):
    class Meta:
        verbose_name = 'پروفایل مشاور'
        verbose_name_plural = 'پروفایل مشاور ها'

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    meli_code = models.IntegerField(unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    daneshkadeh = models.ForeignKey(Daneshkadeh, on_delete=models.CASCADE)
    roozhaye_hozor = models.ManyToManyField(Days)
    saghfe_mojaz_hafte = models.IntegerField(default=0)
    hours_weekly_authorized = models.IntegerField(default=0)
    type_hamkari_ba_daneshgah = models.CharField(
        max_length=100, choices=TYPE_HAMKARI, default="پروژه ای"
    )
    akharin_maghta_tahsili = models.CharField(max_length=100)
    akharin_reshte_tahsili = models.CharField(max_length=150)
    sazman_parvane_behzisti = models.CharField(
        max_length=150, default="ندارد", choices=S_P_B
    )
    tarikh_shoro_faliyat = models.DateTimeField(auto_now_add=True)
    pedar_name = models.CharField(max_length=250, blank=True, null=True)
    birthday = models.DateField()
    shaba_number = models.CharField(max_length=250, blank=True, null=True)
    hesab_number = models.IntegerField(default=0)
    molahezat = models.TextField(max_length=9000, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Nobat(models.Model):
    class Meta:
        verbose_name = 'نوبت'
        verbose_name_plural = 'نوبت ها'

    day = models.CharField(max_length=50, blank=True, null=True)
    daneshjoo = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    moshaver = models.ForeignKey(
        MoshaverProfile, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.day}"


class Consulation(models.Model):
    class Meta:
        verbose_name = 'گزارش مشاوره'
        verbose_name_plural = 'گزارشات مشاوره ها'

    author = models.OneToOneField(MoshaverProfile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    daneshjoo_first_name = models.CharField(max_length=60, null=True, blank=True)
    daneshjoo_last_name = models.CharField(max_length=60, null=True, blank=True)
    daneshjoo_student_number = models.CharField(max_length=50, default=0, null=True, blank=True)
    daneshjoo_meli_number = models.IntegerField(default=0, null=True, blank=True)
    mashroot_len = models.IntegerField(default=0)
    moadel = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    model_term_ghabl = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    nobat = models.DateField(blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    tedad_jalasat_moshavere = models.IntegerField(default=0, null=True, blank=True)
    erja_ravanpezeshk = models.BooleanField(default=False)
    erja_moshavere_balini = models.BooleanField(default=False)
    erja_moshavere_tahsili = models.BooleanField(default=False)
    erja_moshavere_shoghli = models.BooleanField(default=False)
    moshkel_asli = models.TextField(max_length=900, blank=True)
    moshkel_feli = models.TextField(max_length=9000, blank=True)
    arzyabi = models.CharField(max_length=200)
    neshanehaye_raftari = models.TextField(max_length=9000, blank=True)
    ahdaf_modakhele = models.TextField(max_length=9000, blank=True)
    farayande_modakhele = models.TextField(max_length=9000, blank=True)
    slug = models.SlugField(max_length=200, allow_unicode=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            slug_name = f"{self.author.user.username}-{self.nobat}-{self.id}"
            self.slug = slugify(slug_name)

        super(Consulation, self).save(*args, **kwargs)

    def __str__(self):
        return self.author.user.username


class MarakezMoshavere(models.Model):
    class Meta:
        verbose_name = 'مرکز مشاوره'
        verbose_name_plural = 'مراکز مشاوره'

    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    daneshgah_name = models.ForeignKey(Daneshkadeh, on_delete=models.CASCADE)
    karbari_markaz_moshavere = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self):
        return self.daneshgah_name.name


class Reservation(models.Model):
    class Meta:
        verbose_name = 'رزرو'
        verbose_name_plural = 'رزرو ها'

    daneshjoo = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.ForeignKey(Time, blank=True, null=True, on_delete=models.CASCADE)
    moshaver = models.ForeignKey(MoshaverProfile, on_delete=models.CASCADE)
    meli_code = models.IntegerField()
    student_number = models.CharField(max_length=50, default=0)
    phone_number = models.IntegerField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    daneshkadeh = models.ForeignKey(Daneshkadeh, on_delete=models.CASCADE)
    tarikh = models.DateField(blank=True, null=True)
    slug = models.SlugField(max_length=200, allow_unicode=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            slug_name = f"{self.student_number}-{self.id}"
            self.slug = slugify(slug_name)

        super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.daneshjoo.username} - مشاور({self.moshaver})"
