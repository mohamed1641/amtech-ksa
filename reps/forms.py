from decimal import Decimal

from django import forms

from .choices import FRAME_COLOR_CHOICES
from .models import Contract


# الاختيارات المسموح بها في الفورم.
MAGNIFICATION_CHOICES = [
    ("2.5x Galilean", "2.5x Galilean"),
    ("3.0x Galilean", "3.0x Galilean"),
    ("3.5x Galilean", "3.5x Galilean"),
    ("4.0x Prismatic", "4.0x Prismatic"),
    ("5.0x Prismatic", "5.0x Prismatic"),
    ("6.0x Ergo", "6.0x Ergo"),
    ("8.0x Ergo", "8.0x Ergo"),
]

LENS_TYPE_CHOICES = [
    ("TTL1", "TTL1"),
    ("TTL2", "TTL2"),
    ("TTL3", "TTL3"),
    ("TTL5", "TTL5"),
    ("TTLA1", "TTLA1"),
    ("TTLA2", "TTLA2"),
    ("TTLA3", "TTLA3"),
]

LIGHT_CHOICES = [
    ("HLP03", "HLP03"),
    ("USB LED Mini Light", "USB LED Mini Light"),
    ("WHLP01", "WHLP01"),
    ("Energy I", "Energy I"),
]

FRAME_CHOICES = [
    ("", "Select a frame"),
    ("AM559", "AM559"),
    ("ESPORT", "ESPORT"),
    ("AM280Ti", "AM280Ti"),
    ("AM260Ti", "AM260Ti"),
    ("AM100Ti", "AM100Ti"),
    ("AM320", "AM320"),
    ("AM310", "AM310"),
]

# تجميع الألوان من الملف المشترك بدون تكرار.
# التحقق من توافق اللون مع الفريم يتم داخل clean.
COLOR_CHOICES = [
    ("", "Select a color"),
] + list({
    value: label
    for choices in FRAME_COLOR_CHOICES.values()
    for value, label in choices
}.items())


class ContractForm(forms.ModelForm):
    """التحقق من بيانات العقد قبل حفظها في الداتابيز."""

    # الاختيارات المتعددة تُحفظ كقوائم.
    # Django يرفض أي قيمة غير موجودة ضمن الاختيارات المسموحة.
    magnification = forms.MultipleChoiceField(
        choices=MAGNIFICATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    lens_type = forms.MultipleChoiceField(
        choices=LENS_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    lights = forms.MultipleChoiceField(
        choices=LIGHT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    # اختيار فريم واحد ولون واحد.
    frame = forms.ChoiceField(
        choices=FRAME_CHOICES,
        required=False,
    )

    color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        required=False,
    )

    class Meta:
        model = Contract

        # المندوب يُحدد من request.user عند الحفظ.
        # الإجماليات يحسبها الموديل ولا نستقبلها من المتصفح.
        fields = [
            # بيانات العقد والعميل.
            "place",
            "date",
            "name",
            "speciality",
            "mobile",
            "email",
            "city",
            "country",
            "address",

            # وصفة العين اليمنى.
            "r_sph",
            "r_cyl",
            "r_axis",
            "r_add",

            # وصفة العين اليسرى.
            "l_sph",
            "l_cyl",
            "l_axis",
            "l_add",

            # Distance P.D: أربعة صفوف بأعمدة R / L / T.
            # الخانات اختيارية حسب الحالة.
            "distance_pd_1_r",
            "distance_pd_1_l",
            "distance_pd_1_t",
            "distance_pd_2_r",
            "distance_pd_2_l",
            "distance_pd_2_t",
            "distance_pd_3_r",
            "distance_pd_3_l",
            "distance_pd_3_t",
            "distance_pd_4_r",
            "distance_pd_4_l",
            "distance_pd_4_t",

            # W.D.P.P: أربعة صفوف بأعمدة R / L / T.
            "wdpp_1_r",
            "wdpp_1_l",
            "wdpp_1_t",
            "wdpp_2_r",
            "wdpp_2_l",
            "wdpp_2_t",
            "wdpp_3_r",
            "wdpp_3_l",
            "wdpp_3_t",
            "wdpp_4_r",
            "wdpp_4_l",
            "wdpp_4_t",

            # اختيارات المنتج.
            "magnification",
            "lens_type",
            "frame",
            "color",
            "lights",

            # الأسعار والخصم بالريال السعودي.
            "loupes_price",
            "prescription_price",
            "led_price",
            "discount",
        ]

        # القياسات القديمة محفوظة في الموديل،
        # لكنها ليست ضمن مدخلات العقود الجديدة.
        widgets = {
            "date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
            "address": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # السماح بترك السعر فارغًا؛ نحوله لصفر أثناء التحقق.
        price_fields = (
            "loupes_price",
            "prescription_price",
            "led_price",
            "discount",
        )

        for field_name in price_fields:
            self.fields[field_name].required = False
            self.fields[field_name].min_value = Decimal("0.00")
            self.fields[field_name].widget.attrs.update({
                "min": "0",
                "step": "0.01",
            })

        # تطبيق تنسيق المشروع على الحقول العادية.
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs["class"] = "form-control"

    def clean(self):
        """التحقق من الأسعار وتوافق اللون مع الفريم."""
        cleaned_data = super().clean()

        price_fields = (
            "loupes_price",
            "prescription_price",
            "led_price",
            "discount",
        )

        for field_name in price_fields:
            # نحتفظ برسالة الخطأ الأصلية للقيمة غير الصالحة.
            if field_name not in cleaned_data:
                continue

            value = cleaned_data[field_name]

            if value is None:
                cleaned_data[field_name] = Decimal("0.00")
            elif value < 0:
                self.add_error(
                    field_name,
                    "Enter an amount greater than or equal to zero.",
                )

        # السماح بلون فقط عندما يكون تابعًا للفريم المختار.
        frame = cleaned_data.get("frame")
        color = cleaned_data.get("color")

        if color:
            if not frame:
                self.add_error(
                    "color",
                    "Select a frame before choosing a color.",
                )
            else:
                allowed_colors = {
                    value
                    for value, label in FRAME_COLOR_CHOICES.get(frame, [])
                }

                if color not in allowed_colors:
                    self.add_error(
                        "color",
                        "This color is not available for the selected frame.",
                    )

        # ModelForm يشغّل تحقق الموديل بعد هذه المرحلة،
        # بما فيه رفض الخصم الذي يتجاوز مجموع الأسعار.
        return cleaned_data