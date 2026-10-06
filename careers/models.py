from uuid import uuid4

from django.core.validators import FileExtensionValidator
from django.db import models

from .storage import PrivateCVStorage


def cv_upload_path(instance, filename):
    """اسم عشوائي للملف لمنع التعارض وتجنب استخدام اسم المستخدم."""
    return f"cvs/{uuid4().hex}.pdf"


class JobApplication(models.Model):
    """طلب توظيف مقدم من خلال الموقع."""

    # بيانات التواصل.
    name = models.CharField(
        "Full name",
        max_length=120,
    )
    phone = models.CharField(
        "Mobile",
        max_length=30,
    )
    email = models.EmailField()
    city = models.CharField(max_length=100)

    # الوظيفة التي يرغب المتقدم في التقديم عليها.
    position = models.CharField(
        "Position applied for",
        max_length=150,
    )

    # النبذة اختيارية.
    message = models.TextField(
        "Cover message",
        blank=True,
    )

    # الملف مطلوب ويُحفظ في التخزين الخاص.
    # فحص محتوى PDF وحجمه سنضيفه في فورم التقديم.
    cv = models.FileField(
        "CV",
        upload_to=cv_upload_path,
        storage=PrivateCVStorage(),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf"],
            ),
        ],
    )

    # متابعة الطلب داخل لوحة الإدارة.
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", "-pk")
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"

    def __str__(self):
        return f"{self.name} - {self.position}"