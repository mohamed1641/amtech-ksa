from django import forms

from catalog.models import Product

from .models import ContactMessage, SampleRequest


class ContactMessageForm(forms.ModelForm):
    """فورم الأسئلة والاستفسارات العامة بدون اختيار منتج."""

    class Meta:
        model = ContactMessage

        # لا نستقبل subject أو is_read من الزائر.
        fields = (
            "name",
            "phone",
            "email",
            "message",
        )

        labels = {
            "name": "Name",
            "phone": "Mobile",
            "email": "Email",
            "message": "Message",
        }

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your name",
                "autocomplete": "name",
            }),
            "phone": forms.TextInput(attrs={
                "type": "tel",
                "placeholder": "+966...",
                "autocomplete": "tel",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "name@example.com",
                "autocomplete": "email",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "How can we help you?",
                "rows": 5,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # الموبايل مطلوب في الفورم، مع الحفاظ على الموديل القديم.
        self.fields["phone"].required = True

        # تنسيق الحقول بنفس تصميم الموقع.
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class SampleRequestForm(forms.ModelForm):
    """فورم طلب تجربة منتج من المنتجات النشطة في الكتالوج."""

    class Meta:
        model = SampleRequest

        # حالة القراءة وتاريخ الطلب يتحددان داخل النظام.
        fields = (
            "name",
            "phone",
            "email",
            "organization",
            "city",
            "product",
            "notes",
        )

        labels = {
            "name": "Name",
            "phone": "Mobile",
            "email": "Email",
            "organization": "Clinic / organization",
            "city": "City",
            "product": "Product to try",
            "notes": "Notes (optional)",
        }

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Doctor / customer name",
                "autocomplete": "name",
            }),
            "phone": forms.TextInput(attrs={
                "type": "tel",
                "placeholder": "+966...",
                "autocomplete": "tel",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "name@example.com",
                "autocomplete": "email",
            }),
            "organization": forms.TextInput(attrs={
                "placeholder": "Clinic or organization name",
                "autocomplete": "organization",
            }),
            "city": forms.TextInput(attrs={
                "placeholder": "City",
                "autocomplete": "address-level2",
            }),
            "notes": forms.Textarea(attrs={
                "placeholder": "Tell us about your trial request",
                "rows": 5,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # عرض المنتجات النشطة فقط.
        # Django يرفض أيضًا إرسال رقم منتج غير نشط أو غير موجود.
        self.fields["product"].queryset = (
            Product.objects
            .filter(is_active=True)
            .order_by("name")
        )
        self.fields["product"].empty_label = "Select a product"

        # تنسيق الحقول بنفس تصميم الموقع.
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"