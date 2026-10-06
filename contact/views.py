from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ContactMessageForm, SampleRequestForm


@require_http_methods(["GET", "POST"])
def contact(request):
    """عرض فورمي الاستفسارات وطلبات التجربة وحفظ الفورم المرسل."""

    # بادئة مختلفة لكل فورم تمنع تكرار أسماء الحقول ومعرّفاتها.
    enquiry_form = ContactMessageForm(prefix="enquiry")
    sample_form = SampleRequestForm(prefix="sample")

    if request.method == "POST":
        # سنضيف حقلًا مخفيًا في كل فورم يحدد نوع الطلب.
        form_type = request.POST.get("form_type", "")

        if form_type == "enquiry":
            enquiry_form = ContactMessageForm(
                request.POST,
                prefix="enquiry",
            )

            if enquiry_form.is_valid():
                enquiry = enquiry_form.save(commit=False)

                # عنوان ثابت للاستفسارات الجديدة بدل اختيار المنتج.
                enquiry.subject = "General enquiry"
                enquiry.save()

                messages.success(
                    request,
                    "Your message has been sent successfully. "
                    "AMTECH KSA will contact you soon.",
                )

                # إعادة التوجيه تمنع تكرار الإرسال عند تحديث الصفحة.
                return redirect("contact:contact")

        elif form_type == "sample":
            sample_form = SampleRequestForm(
                request.POST,
                prefix="sample",
            )

            if sample_form.is_valid():
                sample_form.save()

                messages.success(
                    request,
                    "Your trial request has been received. "
                    "AMTECH KSA will contact you to arrange the details.",
                )

                return redirect("contact:contact")

        else:
            # لا نحفظ أي بيانات لو نوع الفورم غير معروف.
            messages.error(
                request,
                "We could not identify the form. "
                "Please refresh the page and try again.",
            )

    # عند فشل التحقق، نعيد الفورم ببياناته ورسائل أخطائه.
    context = {
        "enquiry_form": enquiry_form,
        "sample_form": sample_form,
    }

    return render(request, "contact/contact.html", context)