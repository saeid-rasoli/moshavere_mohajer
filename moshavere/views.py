import io

import xlsxwriter
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import redirect, render
from jalali_date import date2jalali

from .forms import (
    ConsulationForm,
    EmployeeProfileForm,
    DaneshjooSignupForm,
    ReservationForm,
)
from .models import (
    Consulation,
    MarakezMoshavere,
    MoshaverProfile,
    Daneshkadeh,
    City,
    Nobat,
    Reservation,
    Time,
)
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
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect("moshavere:index")
    else:
        form = EmployeeProfileForm()
    context = {"form": form, "profile": profile}
    return render(request, "profile/employee.html", context)


@login_required
def nazer(request):
    search_post = request.GET.get("search")
    print("search:", search_post)
    if search_post:
        if len(search_post.split()) == 2:
            consulation_model = Consulation.objects.filter(
                Q(author__first_name__startswith=search_post.split()[0])
                & Q(author__last_name__startswith=search_post.split()[1])
            )
        else:
            consulation_model = Consulation.objects.filter(
                Q(author__first_name__icontains=search_post)
                | Q(author__last_name__icontains=search_post)
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
        "دانشجو",
        "شماره دانشجویی",
        "کُد ملی دانشجو",
        "ترم های مشروطی",
        "معدل",
        "معدل ترم بعد",
        "ارجاع به روانپزشک",
        "ارجاع به مشاوره بالینی",
        "ارجاع به مشاوره تحصیلی",
        "ارجاع به مشاوره شغلی",
        "تاریخ مشاوره حضوری",
        "ساعت مشاوره",
        "تعداد جلسات مشاوره",
        "مشکل اصلی",
        "مشکل فعلی",
        "ارزیابی",
        "نشانه های رفتاری",
        "اهداف مداخله",
        "فرایند مداخله",
    ]
    cols = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
    ]
    cdr = ""
    cde = ""
    cds = ""
    cdt = ""
    if consulation_detail_model.erja_ravanpezeshk == True:
        cdr = "بله"
    else:
        cdr = "خیر"
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

    header_format = workbook.add_format(
        {"bg_color": "yellow", "align": "center", "font_size": 13}
    )
    value_format = workbook.add_format(
        {"bg_color": "#8fe7ff", "align": "center", "font_size": 13}
    )
    for i in range(len(headers)):
        worksheet.write(f"{cols[i]}1", f"{headers[i]}", header_format)

    student_full_name = f"{consulation_detail_model.daneshjoo_first_name} {consulation_detail_model.daneshjoo_last_name}"
    moshaver_full_name = f"{consulation_detail_model.author.first_name} {consulation_detail_model.author.last_name}"
    jalali_join = date2jalali(consulation_detail_model.nobat).strftime("%Y/%m/%d")

    worksheet.write("A2", moshaver_full_name, value_format)
    worksheet.write("B2", student_full_name, value_format)
    worksheet.write(
        "C2", consulation_detail_model.daneshjoo_student_number, value_format
    )
    worksheet.write("D2", consulation_detail_model.daneshjoo_meli_number, value_format)
    worksheet.write("E2", consulation_detail_model.mashroot_len, value_format)
    worksheet.write("F2", consulation_detail_model.moadel, value_format)
    worksheet.write("G2", consulation_detail_model.model_term_ghabl, value_format)
    worksheet.write("H2", cdr, value_format)
    worksheet.write("I2", cdb, value_format)
    worksheet.write("J2", cdt, value_format)
    worksheet.write("K2", cds, value_format)
    worksheet.write("L2", jalali_join, value_format)
    worksheet.write("M2", consulation_detail_model.time, value_format)
    worksheet.write(
        "N2", consulation_detail_model.tedad_jalasat_moshavere, value_format
    )
    worksheet.write("O2", consulation_detail_model.moshkel_asli, value_format)
    worksheet.write("P2", consulation_detail_model.moshkel_feli, value_format)
    worksheet.write("Q2", consulation_detail_model.arzyabi, value_format)
    worksheet.write("R2", consulation_detail_model.neshanehaye_raftari, value_format)
    worksheet.write("S2", consulation_detail_model.ahdaf_modakhele, value_format)
    worksheet.write("T2", consulation_detail_model.farayande_modakhele, value_format)

    # increase width column
    worksheet.set_column("A:N", 30)
    worksheet.set_column("O:T", 90)
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
def reservation_moshaver(request, daneshkadeh):
    moshaver = MoshaverProfile.objects.filter(daneshkadeh__name=daneshkadeh)
    moshaver_username = request.POST.get("moshaver")
    if request.method == "POST":
        return redirect(
            "moshavere:reservation_moshaver",
            daneshkadeh=daneshkadeh,
            moshaver=moshaver_username,
        )
    context = {"moshaver": moshaver}
    return render(request, "students/reservation_moshaver.html", context)


@login_required
def reservation_daneshkadeh_view(request, daneshkadeh, moshaver):
    success_message = "درخواست مشاوره شما با موفقیت ثبت شد."
    moshaver = MoshaverProfile.objects.filter(user__username=moshaver).first()
    reserved_all = Reservation.objects.filter(moshaver=moshaver)
    if request.method == "POST":
        moshaver_pk = request.POST.get("moshaver")
        city_pk = request.POST.get("city")
        daneshkadeh_pk = request.POST.get("daneshkadeh")
        reserved_value = request.POST.get(f"reserved")
        time, day = reserved_value.split(",")
        reserved_day = moshaver.roozhaye_hozor.all()[int(day) - 1]

        form = ReservationForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.daneshjoo = request.user
            instance.moshaver = MoshaverProfile.objects.filter(pk=moshaver_pk).first()
            instance.city = City.objects.filter(pk=city_pk).first()
            instance.time = Time.objects.filter(times=time).first()
            instance.daneshkadeh = Daneshkadeh.objects.filter(pk=daneshkadeh_pk).first()
            Nobat.objects.create(
                day=reserved_day,
                daneshjoo=request.user,
                moshaver=MoshaverProfile.objects.filter(pk=moshaver_pk).first(),
            )

            instance.save()
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect("moshavere:index")
    else:
        form = ReservationForm()

    context = {"moshaver": moshaver, "form": form}
    return render(request, "students/reservation_daneshkadeh.html", context)


def about_us(request):
    return render(request, "about_us.html", {})


def contact_us(request):
    return render(request, "contact_us.html", {})


@login_required
def reserved_requests(request, moshaver):
    reserved_requests_model = Reservation.objects.filter(
        moshaver__user__username=moshaver
    )
    context = {
        "reserved_requests_model": reserved_requests_model,
    }
    return render(request, "students/reserved_requests.html", context)

def reserved_requests_detail(request, moshaver, daneshjoo):
    nobat = Nobat.objects.filter(daneshjoo__username=daneshjoo).first()
    reservation = Reservation.objects.filter(daneshjoo__username=daneshjoo).first()
    context = {
        'nobat': nobat,
        'reservation': reservation
    }
    return render(request, "students/reserved_requests_detail.html", context)