import io

import xlsxwriter
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import redirect, render

from .forms import (
    ConsulationForm,
    EmployeeProfileForm,
    DaneshjooSignupForm,
    ReservationForm,
)
from .models import Consulation, MarakezMoshavere, MoshaverProfile, Daneshkadeh, City
from .scripts import students


def index(request):
    return render(request, "index.html", {})


def login(request):
    return render(request, "auth/login.html", {})


@login_required
def employee(request):
    success_message = "اطاعات شما ثبت شد"
    form = EmployeeProfileForm()
    profile = MoshaverProfile.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = EmployeeProfileForm(request.POST or None)
        if form.is_valid():
            user = request.user
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect("moshavere:index")
    else:
        form = EmployeeProfileForm()
    context = {"form": form, "profile": profile}
    return render(request, "profile/employee.html", context)


@login_required
def nazer(request):
    search_post = request.GET.get("search")
    if search_post:
        if len(search_post.split()) == 2:
            consulation_model = Consulation.objects.filter(
                Q(author__user__first_name__startswith=search_post.split()[0])
                & Q(author__user__last_name__startswith=search_post.split()[1])
            )
        else:
            consulation_model = Consulation.objects.filter(
                Q(author__user__first_name__icontains=search_post)
                | Q(author__user__last_name__icontains=search_post)
                | Q(author__user__username__icontains=search_post)
            )
    else:
        consulation_model = Consulation.objects.all().order_by("-created_date")

    context = {
        "consulation": consulation_model,
    }
    return render(request, "forms/nazer.html", context)


@login_required
def consulation(request):
    success_message = "فرم شما با موفقیت ثبت شد"
    form = ConsulationForm()
    if request.method == "POST":
        form = ConsulationForm(request.POST or None)
        if form.is_valid():
            user = request.user
            instance = form.save(commit=False)
            instance.author = user.moshaverprofile
            instance.save()
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect("moshavere:index")
    else:
        form = ConsulationForm()

    context = {
        "form": form,
    }
    return render(request, "forms/moshaver_consulation.html", context)


@login_required
def consulation_detail(request, slug):
    consulation_detail_model = Consulation.objects.filter(slug=slug).first()
    context = {"consulation_detail": consulation_detail_model}
    return render(request, "forms/consulation_detail.html", context)


@login_required
def export_form(request, slug):
    consulation_detail_model = Consulation.objects.filter(slug=slug).first()
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    headers = [
        "مشاور",
        "ترم های مشروطی",
        "معدل",
        "ارزیابی",
        "ارجاع به مشاوره تحصیلی",
        "ارجاع به مشاوره شغلی",
        "ارجاع به مشاوره بالینی",
        "نوبت",
        "حضور",
        "معدل ترم بعد",
        "مشکل اصلی",
        "نشانه های رفتاری",
        "اهداف مداخله",
        "فرایند مداخله",
    ]
    cols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
    cde = ""
    cds = ""
    cdt = ""
    hozor = ""
    if consulation_detail_model.erja_moshavere_balini == True:
        cdb = "بله"
    else:
        cdb = "خیر"
    if consulation_detail_model.erja_moshavere_shoghli == True:
        cds = "بله"
    else:
        cds = "خیر"
    if consulation_detail_model.erja_moshavere_tahsili == True:
        cdt = "بله"
    else:
        cdt = "خیر"
    if consulation_detail_model.hozor == True:
        hozor = "بله"
    else:
        hozor = "خیر"

    header_format = workbook.add_format(
        {"bg_color": "yellow", "align": "center", "font_size": 13}
    )
    value_format = workbook.add_format(
        {"bg_color": "#8fe7ff", "align": "center", "font_size": 13}
    )
    for i in range(len(headers)):
        worksheet.write(f"{cols[i]}1", f"{headers[i]}", header_format)

    worksheet.write("A2", consulation_detail_model.author.user.username, value_format)
    worksheet.write("B2", consulation_detail_model.mashroot_len, value_format)
    worksheet.write("C2", consulation_detail_model.moadel, value_format)
    worksheet.write("D2", consulation_detail_model.arzyabi, value_format)
    worksheet.write("E2", cdt, value_format)
    worksheet.write("F2", cds, value_format)
    worksheet.write("G2", cdb, value_format)
    worksheet.write("H2", consulation_detail_model.nobat, value_format)
    worksheet.write("I2", hozor, value_format)
    worksheet.write("J2", consulation_detail_model.model_term_ghabl, value_format)
    worksheet.write("K2", consulation_detail_model.moshkel_asli, value_format)
    worksheet.write("L2", consulation_detail_model.neshanehaye_raftari, value_format)
    worksheet.write("M2", consulation_detail_model.ahdaf_modakhele, value_format)
    worksheet.write("N2", consulation_detail_model.farayande_modakhele, value_format)

    # increase width column
    worksheet.set_column("A:J", 30)
    worksheet.set_column("K:N", 90)
    workbook.close()
    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename=f"{consulation_detail_model.author.user.username}-form.xlsx",
    )


def bad_request(request, exception=None):
    return render(request, "error/404.html", {}, status=404)


def server_error(request, exception=None):
    return render(request, "error/500.html", {}, status=500)


@login_required
def students_view(request):
    search_post = request.GET.get("search")
    records = list()
    len_query = None
    if search_post:
        if (
            search_post == "17"
            or search_post == "15"
            or search_post == "13"
            or search_post == "+17"
            or search_post == "-13"
        ):
            for record in students.records:
                if not record[24]:
                    continue
                elif float(record[24]) < int(search_post) + 2 and float(
                    record[24]
                ) > int(search_post):
                    records.append(record)
                elif search_post == "+17" and float(record[24]) > 17:
                    records.append(record)
                elif search_post == "-13" and float(record[24]) < 13:
                    records.append(record)
        elif search_post == "1" or search_post == "2" or search_post == "3":
            for record in students.records:
                if not record[22]:
                    continue
                if int(record[22]) == int(search_post):
                    records.append(record)
        len_query = len(records)
    else:
        records = students.records

    paginator = Paginator(records, 15)
    page_number = request.GET.get("page")
    records = paginator.get_page(page_number)

    context = {"headers": students.headers, "records": records, "len_query": len_query}
    return render(request, "students/students.html", context)


@login_required
def marakez_moshavere_all(request):
    marakez_moshavere_all = MarakezMoshavere.objects.all()
    context = {"markaz_moshavere": marakez_moshavere_all}

    return render(request, "markaz/marakez_moshaver_all.html", context)


@login_required
def marakez_moshavere(request, city):
    marakez_moshavere = MarakezMoshavere.objects.filter(city__name=city).first()
    context = {"markaz_moshavere": marakez_moshavere}

    return render(request, "markaz/markaz_moshavere.html", context)


def daneshjoo_signup(request):
    success_message = "ثبت نام با موفقیت صورت گرفت"
    if request.method == "POST":
        form = DaneshjooSignupForm(request.POST or None)
        if form.is_valid():
            form.save()

            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect("moshavere:login")
    else:
        form = DaneshjooSignupForm()
    context = {"form": form}
    return render(request, "auth/signup.html", context)


@login_required
def reservation_view(request):
    context = {}

    return render(request, "students/reservation.html", context)


@login_required
def reservation_daneshkadeh_view(request, daneshkadeh):
    success_message = "درخواست مشاوره شما با موفقیت ثبت شد."
    moshaver = MoshaverProfile.objects.filter(daneshkadeh__name=daneshkadeh)
    if request.method == "POST":
        moshaver_pk = request.POST.get("moshaver")
        city_pk = request.POST.get("city")
        daneshkadeh_pk = request.POST.get("daneshkadeh")
        form = ReservationForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.daneshjoo = request.user
            instance.moshaver = MoshaverProfile.objects.filter(pk=moshaver_pk).first()
            instance.city = City.objects.filter(pk=city_pk).first()
            instance.daneshkadeh = Daneshkadeh.objects.filter(pk=daneshkadeh_pk).first()

            instance.save()
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect("moshavere:index")
    else:
        form = ReservationForm()

    context = {"moshaver": moshaver, "form": form}
    return render(request, "students/reservation_daneshkadeh.html", context)
