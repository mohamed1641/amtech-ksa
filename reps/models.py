from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Contract(models.Model):
    """بيانات العقد الذي يسجله المندوب."""

    # ربط العقد بالمندوب ومنع حذف حساب له عقود محفوظة.
    sales_rep = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="contracts",
    )

    # بيانات العقد الأساسية.
    place = models.CharField(max_length=150, blank=True)
    date = models.DateField(default=timezone.localdate)

    # بيانات العميل؛ الاسم والموبايل مطلوبان.
    name = models.CharField("Doctor name", max_length=200)
    speciality = models.CharField(max_length=150, blank=True)
    mobile = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    # وصفة العين اليمنى.
    # النص يسمح بتسجيل الإشارات والقيم كما تظهر في الوصفة.
    r_sph = models.CharField("R SPH", max_length=30, blank=True)
    r_cyl = models.CharField("R CYL", max_length=30, blank=True)
    r_axis = models.CharField("R AXIS", max_length=30, blank=True)
    r_add = models.CharField("R ADD", max_length=30, blank=True)

    # وصفة العين اليسرى.
    l_sph = models.CharField("L SPH", max_length=30, blank=True)
    l_cyl = models.CharField("L CYL", max_length=30, blank=True)
    l_axis = models.CharField("L AXIS", max_length=30, blank=True)
    l_add = models.CharField("L ADD", max_length=30, blank=True)

    # الحقول القديمة محفوظة لحماية بيانات العقود السابقة.
    # سنعرضها كبيانات سابقة عند تحديث الأدمن والطباعة.
    distance_pd = models.CharField(
        "Distance P.D",
        max_length=50,
        blank=True,
    )
    wdpp = models.CharField(
        "W.D.P.P",
        max_length=50,
        blank=True,
    )

    # جدول Distance P.D: أربعة صفوف بأعمدة R / L / T.
    # كل خانة اختيارية؛ المندوب يملأ المطلوب حسب الحالة.

    # الصف الأول.
    distance_pd_1_r = models.CharField(
        "Distance P.D — Row 1 — R", max_length=50, blank=True,
    )
    distance_pd_1_l = models.CharField(
        "Distance P.D — Row 1 — L", max_length=50, blank=True,
    )
    distance_pd_1_t = models.CharField(
        "Distance P.D — Row 1 — T", max_length=50, blank=True,
    )

    # الصف الثاني.
    distance_pd_2_r = models.CharField(
        "Distance P.D — Row 2 — R", max_length=50, blank=True,
    )
    distance_pd_2_l = models.CharField(
        "Distance P.D — Row 2 — L", max_length=50, blank=True,
    )
    distance_pd_2_t = models.CharField(
        "Distance P.D — Row 2 — T", max_length=50, blank=True,
    )

    # الصف الثالث.
    distance_pd_3_r = models.CharField(
        "Distance P.D — Row 3 — R", max_length=50, blank=True,
    )
    distance_pd_3_l = models.CharField(
        "Distance P.D — Row 3 — L", max_length=50, blank=True,
    )
    distance_pd_3_t = models.CharField(
        "Distance P.D — Row 3 — T", max_length=50, blank=True,
    )

    # الصف الرابع.
    distance_pd_4_r = models.CharField(
        "Distance P.D — Row 4 — R", max_length=50, blank=True,
    )
    distance_pd_4_l = models.CharField(
        "Distance P.D — Row 4 — L", max_length=50, blank=True,
    )
    distance_pd_4_t = models.CharField(
        "Distance P.D — Row 4 — T", max_length=50, blank=True,
    )

    # جدول W.D.P.P: أربعة صفوف بأعمدة R / L / T.
    # الخانات الفارغة تظل فارغة ولا تتحول إلى صفر.

    # الصف الأول.
    wdpp_1_r = models.CharField(
        "W.D.P.P — Row 1 — R", max_length=50, blank=True,
    )
    wdpp_1_l = models.CharField(
        "W.D.P.P — Row 1 — L", max_length=50, blank=True,
    )
    wdpp_1_t = models.CharField(
        "W.D.P.P — Row 1 — T", max_length=50, blank=True,
    )

    # الصف الثاني.
    wdpp_2_r = models.CharField(
        "W.D.P.P — Row 2 — R", max_length=50, blank=True,
    )
    wdpp_2_l = models.CharField(
        "W.D.P.P — Row 2 — L", max_length=50, blank=True,
    )
    wdpp_2_t = models.CharField(
        "W.D.P.P — Row 2 — T", max_length=50, blank=True,
    )

    # الصف الثالث.
    wdpp_3_r = models.CharField(
        "W.D.P.P — Row 3 — R", max_length=50, blank=True,
    )
    wdpp_3_l = models.CharField(
        "W.D.P.P — Row 3 — L", max_length=50, blank=True,
    )
    wdpp_3_t = models.CharField(
        "W.D.P.P — Row 3 — T", max_length=50, blank=True,
    )

    # الصف الرابع.
    wdpp_4_r = models.CharField(
        "W.D.P.P — Row 4 — R", max_length=50, blank=True,
    )
    wdpp_4_l = models.CharField(
        "W.D.P.P — Row 4 — L", max_length=50, blank=True,
    )
    wdpp_4_t = models.CharField(
        "W.D.P.P — Row 4 — T", max_length=50, blank=True,
    )

    # اختيارات متعددة؛ كل عقد له قوائم مستقلة.
    magnification = models.JSONField(default=list, blank=True)
    lens_type = models.JSONField(default=list, blank=True)
    lights = models.JSONField(default=list, blank=True)

    # الفريم واللون.
    frame = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)

    # الأسعار والخصم بالريال السعودي.
    loupes_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    prescription_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    led_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    # تواريخ يسجلها Django تلقائيًا.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    @property
    def subtotal(self):
        """حساب مجموع الأسعار قبل الخصم."""
        return (
            self.loupes_price
            + self.prescription_price
            + self.led_price
        )

    @property
    def total(self):
        """حساب الإجمالي بعد الخصم."""
        return self.subtotal - self.discount

    def clean(self):
        """رفض الخصم الذي يتجاوز مجموع الأسعار."""
        super().clean()

        amounts = (
            self.loupes_price,
            self.prescription_price,
            self.led_price,
            self.discount,
        )

        # الحقول الناقصة يعالجها التحقق الأساسي في Django.
        if all(amount is not None for amount in amounts):
            if self.discount > self.subtotal:
                raise ValidationError({
                    "discount": "Discount cannot exceed the subtotal."
                })

    def __str__(self):
        return f"Contract #{self.pk or 'New'} - {self.name}"