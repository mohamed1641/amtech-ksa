from django import forms
from pypdf import PdfReader

from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    """التحقق من بيانات المتقدم وملف السيرة الذاتية."""

    class Meta:
        model = JobApplication

        # حالة القراءة وتاريخ التقديم يحددهما النظام.
        fields = (
            "name",
            "phone",
            "email",
            "city",
            "position",
            "message",
            "cv",
        )

        labels = {
            "name": "Full name",
            "phone": "Mobile",
            "email": "Email",
            "city": "City",
            "position": "Position applied for",
            "message": "Cover message (optional)",
            "cv": "Upload CV",
        }

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your full name",
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
            "city": forms.TextInput(attrs={
                "placeholder": "Your city",
                "autocomplete": "address-level2",
            }),
            "position": forms.TextInput(attrs={
                "placeholder": "Position you would like to apply for",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Tell us about your experience",
                "rows": 5,
            }),
            "cv": forms.FileInput(attrs={
                "accept": ".pdf,application/pdf",
            }),
        }

        help_texts = {
            "cv": "PDF only. Maximum file size: 5 MB. No password protection.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # استخدام نفس تنسيق حقول الموقع.
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_cv(self):
        """فحص الحجم والامتداد وإمكانية قراءة الملف كـ PDF."""
        cv = self.cleaned_data.get("cv")

        if not cv:
            raise forms.ValidationError("Please upload your CV.")

        # حد الحجم يُطبق على السيرفر، وليس في المتصفح فقط.
        if cv.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "The CV file must be 5 MB or smaller."
            )

        if not cv.name.lower().endswith(".pdf"):
            raise forms.ValidationError(
                "Please upload a PDF file."
            )

        try:
            cv.seek(0)

            # تغيير امتداد ملف آخر إلى PDF لا يكفي لقبوله.
            if cv.read(5) != b"%PDF-":
                raise forms.ValidationError(
                    "The uploaded file is not a valid PDF."
                )

            cv.seek(0)
            reader = PdfReader(cv)

            # الإدارة يجب أن تتمكن من فتح الملف بدون كلمة مرور.
            if reader.is_encrypted:
                raise forms.ValidationError(
                    "Please upload a PDF without password protection."
                )

            if len(reader.pages) == 0:
                raise forms.ValidationError(
                    "The PDF must contain at least one page."
                )

        except forms.ValidationError:
            raise
        except Exception:
            # إظهار رسالة مفهومة بدل خطأ تقني عند تلف الملف.
            raise forms.ValidationError(
                "We could not read this PDF. "
                "Please export your CV as a new PDF and try again."
            )
        finally:
            # إعادة مؤشر الملف للبداية حتى يُحفظ كاملًا لاحقًا.
            cv.seek(0)

        return cv