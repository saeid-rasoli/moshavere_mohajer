from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee

class UserSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'نام کاربری'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'نام کاربری با زبان انگلیسی',
        })
        self.fields['first_name'].label = 'نام'
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'نام با زبان فارسی',
        })
        self.fields['last_name'].label = 'نام خانوادگی'
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'نام خانوادگی با زبان فارسی',
        })
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password2'].label = 'تکرار رمز عبور'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control'
        })

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError('رمز ها با هم همخوانی ندارند')
        elif len(password2) < 8:
            raise forms.ValidationError('حداقل رمز باید شامل ۸ کاراکتر باشد')
    
    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('کاربری با این نام وجود دارد')
        return username

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'password1', 'password2']


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
