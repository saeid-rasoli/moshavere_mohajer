from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import UserLoginForm

app_name = 'moshavere'
user_login_form = UserLoginForm

urlpatterns = [
    path('', views.index, name='index'),
    # path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html',
         authentication_form=user_login_form), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('employee/', views.employee, name='employee'),
    path('consulation/', views.consulation, name='consulation'),
    path('consulation/<slug:slug>/', views.consulation_detail, name='consulation_detail'),
    path('consulation/<slug:slug>/export/', views.export_form, name='export_form'),
    path('students/', views.students_view, name='students')
]
