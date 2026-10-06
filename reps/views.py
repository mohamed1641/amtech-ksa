from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .choices import FRAME_COLOR_CHOICES
from .forms import ContractForm
from .models import Contract

from django.http import FileResponse, HttpResponseBadRequest
from django.views.decorators.cache import never_cache

from .pdf import build_contract_pdf


def is_sales_rep(user):
    """التأكد إن الحساب نشط ومسجل دخول وضمن جروب المناديب."""
    return (
        user.is_authenticated
        and user.is_active
        and user.groups.filter(name="Sales Reps").exists()
    )


def rep_login(request):
    """عرض صفحة الدخول حتى لو المستخدم عنده جلسة مفتوحة."""

    # نعرض الفورم بدون تحويل تلقائي للمستخدم المسجل.
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        # التحقق من بيانات الدخول باستخدام Django.
        user = authenticate(
            request,
            username=username,
            password=password,
        )

        # السماح بالدخول للحسابات التابعة لجروب المناديب فقط.
        if user is not None and is_sales_rep(user):
            login(request, user)
            return redirect("reps:form")

        error = (
            "Invalid login details or this account "
            "does not have sales rep access."
        )

    return render(request, "reps/login.html", {"error": error})


def rep_form(request):
    """التحقق من البيانات وإمكانية توليد PDF قبل حفظ العقد."""

    # منع الوصول لغير المناديب المصرّح لهم.
    if not is_sales_rep(request.user):
        return redirect("reps:login")

    if request.method == "POST":
        form = ContractForm(request.POST)

        if form.is_valid():
            # تجهيز العقد في الذاكرة بدون حفظه في الداتابيز.
            contract = form.save(commit=False)
            contract.sales_rep = request.user

            try:
                # التأكد من أن البيانات مناسبة لخانات العقد الأصلي.
                preview_pdf = build_contract_pdf(contract)
            except ValueError as error:
                # تظهر الرسالة ضمن أخطاء الفورم مع بقاء المدخلات.
                form.add_error(
                    None,
                    f"Please review the contract before saving: {error}",
                )
            else:
                # ملف التجربة غير مطلوب بعد نجاح التحقق.
                preview_pdf.close()

                # الحفظ يتم فقط بعد نجاح التحقق وتوليد PDF.
                contract.save()
                request.session["current_contract_id"] = contract.pk

                return redirect("reps:print")
    else:
        form = ContractForm()

    # إعادة البيانات والأخطاء وخريطة الألوان إلى الصفحة.
    return render(
        request,
        "reps/form.html",
        {
            "form": form,
            "frame_color_choices": FRAME_COLOR_CHOICES,
        },
    )
    """عرض فورم العقد والتحقق من بياناته وحفظه."""

    # حماية الصفحة من المستخدمين غير المصرّح لهم.
    if not is_sales_rep(request.user):
        return redirect("reps:login")

    if request.method == "POST":
        form = ContractForm(request.POST)

        if form.is_valid():
            # تجهيز العقد وربطه بالمندوب الحالي قبل الحفظ.
            contract = form.save(commit=False)
            contract.sales_rep = request.user
            contract.save()

            # حفظ رقم العقد الحالي داخل الجلسة لاستخدامه في الطباعة.
            request.session["current_contract_id"] = contract.pk

            return redirect("reps:print")

        # الفورم يحتفظ بالبيانات والأخطاء عند فشل التحقق.
    else:
        form = ContractForm()

        # إرسال خريطة الألوان للقالب من نفس مصدر تحقق الباك إند.
    return render(
        request,
        "reps/form.html",
        {
            "form": form,
            "frame_color_choices": FRAME_COLOR_CHOICES,
        },
    )


def rep_print(request):
    """جلب العقد المحفوظ وعرضه للمندوب الذي أنشأه فقط."""

    # حماية صفحة الطباعة.
    if not is_sales_rep(request.user):
        return redirect("reps:login")

    # قراءة رقم العقد الذي تم حفظه في الجلسة.
    contract_id = request.session.get("current_contract_id")

    # فتح فورم جديد إذا لم يوجد عقد حالي في الجلسة.
    if not contract_id:
        return redirect("reps:form")

    # جلب العقد مع التأكد من أنه تابع للمندوب الحالي.
    # العقد المحذوف أو التابع لمندوب آخر يرجع 404.
    contract = get_object_or_404(
        Contract.objects.select_related("sales_rep"),
        pk=contract_id,
        sales_rep=request.user,
    )

    # إرسال بيانات العقد إلى قالب الطباعة.
    return render(
        request,
        "reps/print.html",
        {"contract": contract},
    )


# تسجيل الخروج يقبل POST فقط مع csrf_token داخل الفورم.
@require_POST
def rep_logout(request):
    """إنهاء الجلسة الحالية والرجوع لصفحة الدخول."""
    logout(request)
    return redirect("reps:login")

# منع تخزين صفحة العقد في كاش المتصفح.
@never_cache
def rep_pdf(request, contract_id):
    """عرض أو تحميل العقد الأصلي بعد تعبئته بالبيانات المحفوظة."""

    # السماح للمناديب المصرح لهم فقط.
    if not is_sales_rep(request.user):
        return redirect("reps:login")

    # المندوب يقدر يفتح العقود التابعة له فقط.
    contract = get_object_or_404(
        Contract.objects.select_related("sales_rep"),
        pk=contract_id,
        sales_rep=request.user,
    )

    try:
        pdf_file = build_contract_pdf(contract)
    except ValueError as error:
        # عرض سبب تعذر التوليد كنص، مثل بيانات أطول من الخانة.
        # دعم النص العربي في البيانات المدخلة لم يُضف بعد.
        return HttpResponseBadRequest(
            f"Unable to generate the contract PDF: {error}",
            content_type="text/plain; charset=utf-8",
        )

    # بدون download=1 نعرض الملف، ومعها ننزله على الجهاز.
    download = request.GET.get("download") == "1"

    return FileResponse(
        pdf_file,
        content_type="application/pdf",
        as_attachment=download,
        filename=f"AMTECH_Contract_{contract.pk}.pdf",
    )