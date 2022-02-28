from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import UserSignupForm, EmployeeForm, ConsulationForm
from django.contrib.auth.decorators import login_required
from .models import Employee, Consulation
import io
import xlsxwriter
from django.http import FileResponse


def index(request):
    return render(request, 'index.html', {})


def signup(request):
    success_message = 'ثبت نام با موفقیت صورت گرفت'
    if request.method == 'POST':
        form = UserSignupForm(request.POST or None)
        if form.is_valid():
            form.save()

            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect('moshavere:login')
    else:
        form = UserSignupForm()
    context = {
        'form': form
    }
    return render(request, 'auth/signup.html', context)


def login(request):
    return render(request, 'auth/login.html', {})


@login_required
def employee(request):
    success_message = 'اطاعات شما ثبت شد'
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST or None)
        if form.is_valid():
            user = request.user
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect('moshavere:index')
    else:
        form = EmployeeForm()
    context = {
        'form': form
    }
    return render(request, 'profile/employee.html', context)


@login_required
def consulation(request):
    success_message = 'فرم شما با موفقیت ثبت شد'
    employee_model = Employee.objects.filter(user=request.user).first()
    consulation_model = Consulation.objects.all().order_by('-created_date')
    form = ConsulationForm()
    if request.method == 'POST':
        form = ConsulationForm(request.POST or None)
        if form.is_valid():
            user = request.user
            instance = form.save(commit=False)
            instance.author = user.employee
            instance.save()
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect('moshavere:index')
    else:
        form = ConsulationForm()

    context = {
        'employee': employee_model,
        'form': form,
        'consulation': consulation_model
    }
    return render(request, 'forms/consulation.html', context)

@login_required
def consulation_detail(request, slug):
    consulation_detail_model = Consulation.objects.filter(slug=slug).first()
    context = {
        'consulation_detail': consulation_detail_model
    }
    return render(request, 'forms/consulation_detail.html', context)

@login_required
def export_form(request, slug):
    consulation_detail_model = Consulation.objects.filter(slug=slug).first()
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    headers = ['مشاور', 'ترم های مشروطی', 'معدل', 'ارزیابی', 'ارجاع به مشاوره تحصیلی', 'ارجاع به مشاوره شغلی', 'ارجاع به مشاوره بالینی', 'نوبت', 'حضور', 'معدل ترم بعد', 'مشکل اصلی', 'نشانه های رفتاری', 'اهداف مداخله', 'فرایند مداخله']
    cols =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
    cde = ''
    cds = ''
    cdt = ''
    hozor = ''
    if consulation_detail_model.erja_moshavere_balini == True:
        cdb = 'بله'
    else:
        cdb = 'خیر'
    if consulation_detail_model.erja_moshavere_shoghli == True:
        cds = 'بله'
    else:
        cds = 'خیر'
    if consulation_detail_model.erja_moshavere_tahsili == True:
        cdt = 'بله'
    else:
        cdt = 'خیر'
    if consulation_detail_model.hozor == True:
        hozor = 'بله'
    else:
        hozor = 'خیر'
    for i in range(len(headers)):
        worksheet.write(f'{cols[i]}1', f'{headers[i]}')
    worksheet.write('A2', consulation_detail_model.author.user.username)
    worksheet.write('B2', consulation_detail_model.mashroot_len)
    worksheet.write('C2', consulation_detail_model.moadel)
    worksheet.write('D2', consulation_detail_model.arzyabi)
    worksheet.write('E2', cdt)
    worksheet.write('F2', cds)
    worksheet.write('G2', cdb)
    worksheet.write('H2', consulation_detail_model.nobat)
    worksheet.write('I2', hozor)
    worksheet.write('J2', consulation_detail_model.model_term_baad)
    worksheet.write('K2', consulation_detail_model.moshkel_asli)
    worksheet.write('L2', consulation_detail_model.neshanehaye_raftari)
    worksheet.write('M2', consulation_detail_model.ahdaf_modakhele)
    worksheet.write('N2', consulation_detail_model.farayande_modakhele)
    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='report.xlsx')
