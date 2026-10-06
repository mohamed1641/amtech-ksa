from django.contrib import admin

from .models import Contract


from django.contrib import admin

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """إدارة العقود من Django Admin."""

    # الأعمدة الظاهرة في قائمة العقود.
    list_display = (
        "id",
        "name",
        "mobile",
        "sales_rep",
        "date",
        "total_display",
        "created_at",
    )

    # تصفية العقود حسب المندوب والتاريخ.
    list_filter = (
        "sales_rep",
        "date",
        "created_at",
    )

    # البحث ببيانات العميل أو اسم المندوب.
    search_fields = (
        "name",
        "mobile",
        "email",
        "sales_rep__username",
        "sales_rep__first_name",
        "sales_rep__last_name",
    )

    # جلب بيانات المندوب مع العقود لتقليل الاستعلامات.
    list_select_related = ("sales_rep",)

    # الإجماليات محسوبة والتواريخ تلقائية.
    readonly_fields = (
        "subtotal_display",
        "total_display",
        "created_at",
        "updated_at",
    )

    # الأحدث أولًا.
    ordering = ("-created_at", "-pk")

    # تقسيم صفحة العقد إلى أقسام.
    fieldsets = (
        ("Contract Details", {
            "fields": (
                "sales_rep",
                "place",
                "date",
            ),
        }),

        ("Customer Details", {
            "fields": (
                "name",
                "speciality",
                "mobile",
                "email",
                "city",
                "country",
                "address",
            ),
        }),

        ("Prescription — Right Eye", {
            "fields": (
                "r_sph",
                "r_cyl",
                "r_axis",
                "r_add",
            ),
        }),

        ("Prescription — Left Eye", {
            "fields": (
                "l_sph",
                "l_cyl",
                "l_axis",
                "l_add",
            ),
        }),

        # كل مجموعة تعرض خانات R / L / T في صف واحد.
        ("Distance P.D", {
            "fields": (
                (
                    "distance_pd_1_r",
                    "distance_pd_1_l",
                    "distance_pd_1_t",
                ),
                (
                    "distance_pd_2_r",
                    "distance_pd_2_l",
                    "distance_pd_2_t",
                ),
                (
                    "distance_pd_3_r",
                    "distance_pd_3_l",
                    "distance_pd_3_t",
                ),
                (
                    "distance_pd_4_r",
                    "distance_pd_4_l",
                    "distance_pd_4_t",
                ),
            ),
        }),

        ("W.D.P.P", {
            "fields": (
                ("wdpp_1_r", "wdpp_1_l", "wdpp_1_t"),
                ("wdpp_2_r", "wdpp_2_l", "wdpp_2_t"),
                ("wdpp_3_r", "wdpp_3_l", "wdpp_3_t"),
                ("wdpp_4_r", "wdpp_4_l", "wdpp_4_t"),
            ),
        }),

        # قياسات العقود القديمة تظل متاحة داخل قسم قابل للطي.
        ("Legacy Measurements", {
            "fields": (
                "distance_pd",
                "wdpp",
            ),
            "classes": ("collapse",),
            "description": (
                "Measurements recorded before the detailed "
                "tables were added."
            ),
        }),

        ("Product Options", {
            "fields": (
                "magnification",
                "lens_type",
                "frame",
                "color",
                "lights",
            ),
        }),

        ("Pricing — SAR", {
            "fields": (
                "loupes_price",
                "prescription_price",
                "led_price",
                "subtotal_display",
                "discount",
                "total_display",
            ),
        }),

        ("Record Dates", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    # عرض الحسابات النشطة التابعة لجروب المناديب في قائمة الاختيار.
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sales_rep":
            user_model = db_field.remote_field.model

            kwargs["queryset"] = user_model.objects.filter(
                is_active=True,
                groups__name="Sales Reps",
            ).distinct()

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )

    @admin.display(description="Subtotal (SAR)")
    def subtotal_display(self, obj):
        """عرض مجموع الأسعار قبل الخصم."""
        if obj is None:
            return "—"

        return f"{obj.subtotal:,.2f}"

    @admin.display(description="Total (SAR)")
    def total_display(self, obj):
        """عرض الإجمالي النهائي بعد الخصم."""
        if obj is None:
            return "—"

        return f"{obj.total:,.2f}"

    # قصر اختيار المندوب على الحسابات النشطة داخل Sales Reps.
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sales_rep":
            user_model = db_field.remote_field.model

            kwargs["queryset"] = user_model.objects.filter(
                is_active=True,
                groups__name="Sales Reps",
            ).distinct()

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )

    @admin.display(description="Subtotal (SAR)")
    def subtotal_display(self, obj):
        """عرض الإجمالي قبل الخصم من الأسعار المحفوظة."""
        if obj is None:
            return "—"

        return f"{obj.subtotal:,.2f}"

    @admin.display(description="Total (SAR)")
    def total_display(self, obj):
        """عرض الإجمالي النهائي بعد الخصم."""
        if obj is None:
            return "—"

        return f"{obj.total:,.2f}"