from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import UserLoginForm

app_name = 'moshavere'
user_login_form = UserLoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html',
         authentication_form=user_login_form), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('signup/', views.daneshjoo_signup, name='signup'),
    path('employee/', views.employee, name='employee'),
    path('consulation/', views.consulation, name='consulation'),
    path('nazer/', views.nazer, name='nazer'),
    path('consulation/<slug:slug>/', views.consulation_detail, name='consulation_detail'),
    path('consulation/<slug:slug>/export/', views.export_form, name='export_form'),
    path('students/', views.students_view, name='students'),
    path('markaz-moshavere/<city>/', views.marakez_moshavere, name='markaz_moshavere'),
    path('markaz-moshavere/', views.marakez_moshavere_all, name='markaz_moshavere_all'),
    path('reservation/', views.reservation_view, name='reservation'),
    path('reservation/<daneshkadeh>/', views.reservation_daneshkadeh_view, name='reservation_daneshkadeh'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('reserved-requests/<moshaver>/', views.reserved_requests, name='reserved_requests')

]
