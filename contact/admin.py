from django.contrib import admin

from .models import ContactMessage, SampleRequest


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """إدارة رسائل الأسئلة والاستفسارات العامة."""

    list_display = (
        "name",
        "email",
        "phone",
        "subject",
        "is_read",
        "created_at",
    )

    # تغيير حالة القراءة مباشرة من قائمة الرسائل.
    list_editable = ("is_read",)

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "subject",
        "message",
    )

    # الحفاظ على بيانات الرسالة كما أرسلها الزائر.
    readonly_fields = (
        "name",
        "email",
        "phone",
        "subject",
        "message",
        "created_at",
    )

    ordering = ("-created_at", "-pk")

    def has_add_permission(self, request):
        """الرسائل تُنشأ من فورم الموقع."""
        return False


@admin.register(SampleRequest)
class SampleRequestAdmin(admin.ModelAdmin):
    """إدارة طلبات تجربة المنتجات."""

    list_display = (
        "name",
        "phone",
        "organization",
        "city",
        "product",
        "is_read",
        "created_at",
    )

    # تغيير حالة القراءة مباشرة من قائمة الطلبات.
    list_editable = ("is_read",)

    list_filter = (
        "is_read",
        "product",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "organization",
        "city",
        "product__name",
        "notes",
    )

    # تحميل بيانات المنتج مع الطلب لتقليل استعلامات الداتابيز.
    list_select_related = ("product",)

    # بيانات العميل للعرض فقط؛ حالة القراءة قابلة للتعديل.
    readonly_fields = (
        "name",
        "phone",
        "email",
        "organization",
        "city",
        "product",
        "notes",
        "created_at",
    )

    fieldsets = (
        ("Contact Details", {
            "fields": (
                "name",
                "phone",
                "email",
            ),
        }),
        ("Trial Request", {
            "fields": (
                "organization",
                "city",
                "product",
                "notes",
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
        """طلبات التجربة تُنشأ من فورم الموقع."""
        return False