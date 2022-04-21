from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UsernameField)
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import ProfileEmployee, Consulation
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


class EmployeeProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['city'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['daneshkadeh'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['saghfe_mojaz_hafte'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['hours_weekly_authorized'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['akharin_maghta_tahsili'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['akharin_reshte_tahsili'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['sazman_parvane_behzisti'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['roozhaye_hozor'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['pedar_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['shaba_number'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['hesab_number'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['molahezat'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['molahezat'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['meli_code'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['job'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['type_hamkari_ba_daneshgah'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['birthday'] = JalaliDateField(label=('تاریخ تولد'),
                                               widget=AdminJalaliDateWidget,
                                               )
        self.fields['birthday'].widget.attrs.update({'class': 'form-control jalali_date-date',
                                                  'placeholder': 'برای انتخاب تاریخ کلیک کنید'})

    class Meta:
        model = ProfileEmployee
        exclude = ['employee', 'tarikh_shoro_faliyat', 'is_authorized', 'user']

    def clean(self):
        meli_code = str(self.cleaned_data['meli_code'])

        if len(meli_code) != 10:
            raise forms.ValidationError('کُد ملی نا معتبر')
        elif ProfileEmployee.objects.filter(meli_code=meli_code).exists():
            raise forms.ValidationError(
                'کاربری با این کُد ملی قبلا ثبت نام کرده است')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Custom error'
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'نام کاربری به انگلیسی'}))
    username.label = 'نام کاربری'
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
    ))
    password.label = 'رمز عبور'


class ConsulationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConsulationForm, self).__init__(*args, **kwargs)
        self.fields['mashroot_len'].label = 'تعداد ترم های مشروطی'
        self.fields['mashroot_len'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['moadel'].label = 'معدل'
        self.fields['moadel'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['arzyabi'].label = 'ارزیابی و تشخیص مشاور'
        self.fields['arzyabi'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['erja_moshavere_tahsili'].label = 'ارجاع مشاوره تحصیلی'
        self.fields['erja_moshavere_tahsili'].widget.attrs.update({
            'class': 'form-check-input'
        })
        self.fields['erja_moshavere_shoghli'].label = 'ارجاع مشاوره شغلی'
        self.fields['erja_moshavere_shoghli'].widget.attrs.update({
            'class': 'form-check-input'
        })
        self.fields['erja_moshavere_balini'].label = 'ارجاع مشاوره بالینی'
        self.fields['erja_moshavere_balini'].widget.attrs.update({
            'class': 'form-check-input'
        })
        self.fields['hozor'].label = 'حضور'
        self.fields['hozor'].widget.attrs.update({
            'class': 'form-check-input'
        })
        self.fields['model_term_ghabl'].label = 'معدل ترم قبل'
        self.fields['model_term_ghabl'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['moshkel_asli'].label = 'مشکل اصلی'
        self.fields['moshkel_asli'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['neshanehaye_raftari'].label = 'نشانه های رفتاری'
        self.fields['neshanehaye_raftari'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['ahdaf_modakhele'].label = 'اهداف مداخله'
        self.fields['ahdaf_modakhele'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['farayande_modakhele'].label = 'فرایند مداخله'
        self.fields['farayande_modakhele'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['nobat'] = JalaliDateField(label=('نوبت'),
                                               widget=AdminJalaliDateWidget,
                                               )
        self.fields['nobat'].widget.attrs.update({'class': 'form-control jalali_date-date',
                                                  'placeholder': 'برای انتخاب تاریخ کلیک کنید'})

    class Meta:
        model = Consulation
        exclude = ['author', 'slug']
