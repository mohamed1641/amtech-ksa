from django.db import models


class ContactMessage(models.Model):
    """رسالة سؤال أو استفسار عام من زائر الموقع."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)

    # نحتفظ بالحقل للحفاظ على الرسائل القديمة.
    # الفورم الجديد لن يحتوي على اختيار منتج.
    subject = models.CharField(max_length=180, blank=True)

    message = models.TextField()

    # لمتابعة الرسائل من لوحة الإدارة.
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.email}"


class SampleRequest(models.Model):
    """طلب عينة أو تجربة منتج، مستقل عن رسائل الاستفسارات."""

    # بيانات صاحب الطلب.
    name = models.CharField(
        "Full name",
        max_length=120,
    )
    phone = models.CharField(
        "Mobile",
        max_length=30,
    )
    email = models.EmailField()

    # مكان التجربة.
    organization = models.CharField(
        "Clinic / organization",
        max_length=200,
    )
    city = models.CharField(
        max_length=100,
    )

    # ربط الطلب بالمنتج المختار من الكتالوج.
    # منع حذف منتج له طلبات تجربة؛ يمكن تعطيله بدلًا من حذفه.
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.PROTECT,
        related_name="sample_requests",
        verbose_name="Product to try",
    )

    # الملاحظات اختيارية.
    notes = models.TextField(
        blank=True,
    )

    # متابعة الطلبات داخل لوحة الإدارة.
    is_read = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ("-created_at", "-pk")
        verbose_name = "Sample Request"
        verbose_name_plural = "Sample Requests"

    def __str__(self):
        return f"{self.name} - {self.product}"