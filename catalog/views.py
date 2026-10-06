from django.db.models import Min, Prefetch, Q
from django.shortcuts import get_object_or_404, render

from .models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductVariant,
)


def product_list(request):
    """عرض المنتجات مع البحث والفلاتر والترتيب."""

    search_query = request.GET.get("q", "").strip()
    current_category = request.GET.get("category", "").strip()
    current_system = request.GET.get("system", "").strip()
    current_magnification = request.GET.get("magnification", "").strip()
    current_sort = request.GET.get("sort", "featured").strip()

    # الخيارات المفعّلة فقط هي التي تظهر داخل كروت المنتجات.
    active_variants = ProductVariant.objects.filter(
        is_active=True
    ).order_by("price")

    products = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related(
            Prefetch("variants", queryset=active_variants)
        )
        .annotate(
            # حساب أقل سعر من الخيارات المفعّلة فقط.
            # لو مفيش خيارات مفعّلة، النتيجة تكون None.
            price_from=Min(
                "variants__price",
                filter=Q(variants__is_active=True),
            )
        )
    )

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(short_description__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__name__icontains=search_query)
            | Q(system__icontains=search_query)
        )

    if current_category:
        products = products.filter(category__slug=current_category)

    if current_system:
        products = products.filter(system=current_system)

    if current_magnification:
        # الشرطان في نفس filter لضمان أن خيار التكبير نفسه مفعّل.
        products = products.filter(
            variants__magnification=current_magnification,
            variants__is_active=True,
        )

    products = products.distinct()

    # ترتيب السعر يعتمد على أقل سعر مفعّل المحسوب أعلاه.
    if current_sort == "low":
        products = products.order_by("price_from", "name")
    elif current_sort == "high":
        products = products.order_by("-price_from", "name")
    elif current_sort == "name":
        products = products.order_by("name")
    else:
        products = products.order_by("-is_featured", "name")

    categories = Category.objects.filter(
        is_active=True
    ).order_by("name")

    # اختيارات فلتر التكبير تأتي من خيارات ومنتجات مفعّلة.
    magnifications = (
        ProductVariant.objects.filter(
            is_active=True,
            product__is_active=True,
        )
        .exclude(magnification="")
        .values_list("magnification", flat=True)
        .distinct()
        .order_by("magnification")
    )

    context = {
        "products": products,
        "product_count": products.count(),
        "categories": categories,
        "systems": Product.SYSTEM_CHOICES,
        "magnifications": magnifications,
        "search_query": search_query,
        "current_category": current_category,
        "current_system": current_system,
        "current_magnification": current_magnification,
        "current_sort": current_sort,
    }

    return render(request, "catalog/products.html", context)


def product_detail(request, slug):
    """عرض تفاصيل منتج مفعّل وأسعاره ومواصفاته."""

    active_variants = ProductVariant.objects.filter(
        is_active=True
    ).order_by("price")

    product_images = ProductImage.objects.order_by("order", "id")
    product_specs = ProductSpecification.objects.order_by("order", "id")

    product = get_object_or_404(
        Product.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related(
            Prefetch("variants", queryset=active_variants),
            Prefetch("images", queryset=product_images),
            Prefetch("specifications", queryset=product_specs),
        )
        .annotate(
            # السعر المبدئي في صفحة التفاصيل من الخيارات المفعّلة فقط.
            price_from=Min(
                "variants__price",
                filter=Q(variants__is_active=True),
            )
        ),
        slug=slug,
    )

    related_products = (
        Product.objects.filter(
            is_active=True,
            category=product.category,
        )
        .exclude(id=product.id)
        .select_related("category")
        .prefetch_related(
            Prefetch("variants", queryset=active_variants)
        )
        .annotate(
            # تطبيق نفس القاعدة على المنتجات المرتبطة.
            price_from=Min(
                "variants__price",
                filter=Q(variants__is_active=True),
            )
        )
        .order_by("-is_featured", "name")[:3]
    )

    context = {
        "product": product,
        "variants": product.variants.all(),
        "specifications": product.specifications.all(),
        "gallery_images": list(product.images.all()),
        "related_products": related_products,
    }

    return render(request, "catalog/product_detail.html", context)