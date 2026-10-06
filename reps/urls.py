from django.urls import path

from . import views


# اسم التطبيق المستخدم في روابط Django.
app_name = "reps"


urlpatterns = [
    # صفحة تسجيل دخول المندوب.
    path("", views.rep_login, name="login"),

    # تسجيل الخروج باستخدام POST فقط.
    path("logout/", views.rep_logout, name="logout"),

    # صفحة إنشاء عقد جديد.
    path("form/", views.rep_form, name="form"),

    # صفحة العقد بعد الحفظ.
    path("print/", views.rep_print, name="print"),

    # عرض PDF للعقد المحدد.
    # إضافة ?download=1 للرابط تحوّله إلى تحميل مباشر.
    # دالة rep_pdf تتحقق من صلاحية المندوب وملكيته للعقد.
    path(
        "contracts/<int:contract_id>/pdf/",
        views.rep_pdf,
        name="pdf",
    ),
]