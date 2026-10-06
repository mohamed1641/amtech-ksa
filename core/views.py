from django.db.models import Min, Prefetch, Q
from django.shortcuts import render

from catalog.models import Product, ProductVariant


def home(request):
    """عرض الصفحة الرئيسية بالمنتجات المميزة النشطة."""

    # تحميل اختيارات المنتج النشطة فقط، مرتبة من الأقل سعرًا.
    active_variants = (
        ProductVariant.objects
        .filter(is_active=True)
        .order_by("price")
    )

    featured_products = (
        Product.objects.filter(
            is_active=True,
            is_featured=True,
        )
        .select_related("category")
        .prefetch_related(
            Prefetch("variants", queryset=active_variants)
        )
        .annotate(
            # حساب أقل سعر من الاختيارات النشطة فقط.
            # لو مفيش اختيارات نشطة، تكون القيمة None.
            price_from=Min(
                "variants__price",
                filter=Q(variants__is_active=True),
            )
        )
        .order_by("name")[:6]
    )

    context = {
        "featured_products": featured_products,
    }

    return render(request, "core/index.html", context)


def about(request):
    """عرض صفحة التعريف بالشركة."""
    return render(request, "core/about.html")


def policies(request):
    """عرض صفحة السياسات."""
    return render(request, "core/policies.html")