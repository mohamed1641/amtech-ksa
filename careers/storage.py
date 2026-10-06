from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible


@deconstructible
class PrivateCVStorage(FileSystemStorage):
    """تخزين ملفات التوظيف بعيدًا عن ملفات الموقع العامة."""

    def __init__(self):
        super().__init__(
            location=settings.PRIVATE_MEDIA_ROOT,
            # صلاحيات الملفات والمجلدات على السيرفر.
            file_permissions_mode=0o600,
            directory_permissions_mode=0o700,
        )

    def url(self, name):
        """منع إنشاء رابط عام للملف."""
        raise ValueError(
            "CV files are private and require an authorized download."
        )