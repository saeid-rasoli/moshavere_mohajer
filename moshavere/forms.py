from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UsernameField)
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Employee, Consulation
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


# class UserSignupForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].label = 'نام کاربری'
#         self.fields['username'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'نام کاربری با زبان انگلیسی',
#         })
#         self.fields['first_name'].label = 'نام'
#         self.fields['first_name'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'نام با زبان فارسی',
#         })
#         self.fields['last_name'].label = 'نام خانوادگی'
#         self.fields['last_name'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'نام خانوادگی با زبان فارسی',
#         })
#         self.fields['password1'].label = 'رمز عبور'
#         self.fields['password1'].widget.attrs.update({
#             'class': 'form-control'
#         })
#         self.fields['password2'].label = 'تکرار رمز عبور'
#         self.fields['password2'].widget.attrs.update({
#             'class': 'form-control'
#         })

#     def clean_password2(self):
#         password1 = self.cleaned_data['password1']
#         password2 = self.cleaned_data['password2']

#         if password1 != password2:
#             raise forms.ValidationError('رمز ها با هم همخوانی ندارند')
#         elif len(password2) < 8:
#             raise forms.ValidationError('حداقل رمز باید شامل ۸ کاراکتر باشد')

#     def clean_username(self):
#         username = self.cleaned_data['username']

#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError('کاربری با این نام وجود دارد')
#         return username

#     class Meta:
#         model = User
#         fields = ['username', 'first_name',
#                   'last_name', 'password1', 'password2']


class EmployeeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meli_code'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['job'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = Employee
        fields = ['meli_code', 'job']

    def clean(self):
        meli_code = str(self.cleaned_data['meli_code'])

        if len(meli_code) != 10:
            raise forms.ValidationError('کُد ملی نا معتبر')
        elif Employee.objects.filter(meli_code=meli_code).exists():
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
