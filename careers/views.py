from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import JobApplicationForm


@require_http_methods(["GET", "POST"])
def apply(request):
    """عرض فورم التوظيف والتحقق من الطلب وحفظه."""

    if request.method == "POST":
        # الملفات المرفوعة موجودة في request.FILES.
        form = JobApplicationForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            # حفظ بيانات الطلب والـCV في التخزين الخاص.
            form.save()

            messages.success(
                request,
                "Your application has been submitted successfully. "
                "Our team will review it and contact you if there "
                "is a suitable opportunity.",
            )

            # منع تكرار الإرسال عند تحديث الصفحة.
            return redirect("careers:apply")

    else:
        form = JobApplicationForm()

    # عند وجود أخطاء، نحتفظ بالحقول النصية المدخلة.
    # المتقدم سيحتاج لإعادة اختيار الملف بسبب قيود المتصفح.
    return render(
        request,
        "careers/apply.html",
        {"form": form},
    )