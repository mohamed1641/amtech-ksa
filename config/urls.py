from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # لوحة الإدارة.
    path("admin/", admin.site.urls),

    # صفحات الموقع.
    path("", include("core.urls")),
    path("products/", include("catalog.urls")),
    path("contact/", include("contact.urls")),

    # صفحة التقديم على الوظائف.
    path("careers/", include("careers.urls")),

    # منطقة المناديب.
    path("reps/", include("reps.urls")),
]


# عرض ملفات الميديا العامة أثناء التطوير فقط.
# ملفات CV موجودة في PRIVATE_MEDIA_ROOT ولا نضيف لها مسارًا عامًا.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )