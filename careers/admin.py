from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.urls import path, reverse
from django.utils.html import format_html

from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    """عرض طلبات التوظيف وتحميل ملفات CV بصلاحيات الإدارة."""

    list_display = (
        "name",
        "position",
        "city",
        "phone",
        "is_read",
        "created_at",
        "download_cv",
    )

    list_editable = ("is_read",)

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "city",
        "position",
        "message",
    )

    # نستخدم زر التحميل بدل حقل cv حتى لا يُطلب رابط عام للملف.
    readonly_fields = (
        "name",
        "phone",
        "email",
        "city",
        "position",
        "message",
        "download_cv",
        "created_at",
    )

    fieldsets = (
        ("Applicant Details", {
            "fields": (
                "name",
                "phone",
                "email",
                "city",
            ),
        }),
        ("Application", {
            "fields": (
                "position",
                "message",
                "download_cv",
            ),
        }),
        ("Follow-up", {
            "fields": (
                "is_read",
                "created_at",
            ),
        }),
    )

    ordering = ("-created_at", "-pk")

    def has_add_permission(self, request):
        """طلبات التوظيف تُنشأ من صفحة التقديم."""
        return False

    def get_urls(self):
        """إضافة مسار تحميل محمي داخل لوحة الإدارة."""
        custom_urls = [
            path(
                "<int:object_id>/download-cv/",
                self.admin_site.admin_view(self.download_cv_view),
                name="careers_jobapplication_download_cv",
            ),
        ]

        # المسار المخصص يأتي قبل مسارات الأدمن الافتراضية.
        return custom_urls + super().get_urls()

    @admin.display(description="CV")
    def download_cv(self, obj):
        """عرض زر تحميل بدل كشف مكان الملف."""
        if not obj or not obj.pk or not obj.cv:
            return "No CV uploaded."

        url = reverse(
            f"{self.admin_site.name}:careers_jobapplication_download_cv",
            args=[obj.pk],
        )

        return format_html(
            '<a class="button" href="{}">Download CV</a>',
            url,
        )

    def download_cv_view(self, request, object_id):
        """التحقق من الصلاحية قبل فتح الملف وإرساله."""

        # تسجيل الدخول للأدمن وحده لا يكفي؛ نتحقق من صلاحية الطلبات.
        if not self.has_view_permission(request):
            raise PermissionDenied

        application = self.get_object(request, str(object_id))

        if application is None:
            raise Http404("Application not found.")

        if not self.has_view_permission(request, application):
            raise PermissionDenied

        if not application.cv:
            raise Http404("No CV is attached to this application.")

        try:
            cv_file = application.cv.open("rb")
        except FileNotFoundError:
            raise Http404("The CV file could not be found.")

        # تنزيل الملف كمرفق باسم واضح، بدون رابط ميديا عام.
        response = FileResponse(
            cv_file,
            as_attachment=True,
            filename=f"CV_Application_{application.pk}.pdf",
            content_type="application/pdf",
        )

        # منع تخزين بيانات المتقدم في الكاش.
        response["Cache-Control"] = "private, no-store"
        response["X-Content-Type-Options"] = "nosniff"

        return response