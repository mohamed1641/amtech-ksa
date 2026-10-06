from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    Product,
    ProductImage,
    ProductVariant,
    ProductSpecification,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin settings for product categories.
    """

    list_display = ("name", "slug", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


class ProductVariantInline(admin.TabularInline):
    """
    Manage product prices/options inside the product page.
    """

    model = ProductVariant
    extra = 0
    fields = (
        "magnification",
        "price",
        "working_distance",
        "depth_of_focus",
        "field_of_view",
        "weight",
        "standard_frame",
        "standard_case",
        "is_active",
    )


class ProductImageInline(admin.TabularInline):
    """
    Manage product gallery images inside the product page.
    """

    model = ProductImage
    extra = 0


class ProductSpecificationInline(admin.TabularInline):
    """
    Manage custom product specifications inside the product page.
    """

    model = ProductSpecification
    extra = 0
    fields = ("name", "value", "order")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin settings for products.
    """

    list_display = (
        "image_preview",
        "name",
        "category",
        "system",
        "starting_price",
        "variants_count",
        "is_featured",
        "is_active",
        "updated_at",
    )

    list_editable = (
        "is_featured",
        "is_active",
    )

    list_filter = (
        "category",
        "system",
        "is_featured",
        "is_active",
    )

    search_fields = (
        "name",
        "short_description",
        "description",
    )

    prepopulated_fields = {"slug": ("name",)}

    readonly_fields = (
        "created_at",
        "updated_at",
        "image_preview_large",
    )

    ordering = ("name",)

    inlines = [
        ProductVariantInline,
        ProductImageInline,
        ProductSpecificationInline,
    ]

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "category",
                "name",
                "slug",
                "system",
                "short_description",
                "description",
            )
        }),
        ("Media", {
            "fields": (
                "main_image",
                "image_preview_large",
            )
        }),
        ("Catalog", {
            "fields": (
                "catalog_page",
            )
        }),
        ("Display Options", {
            "fields": (
                "is_featured",
                "is_active",
            )
        }),
        ("Dates", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": (
                "collapse",
            ),
        }),
    )

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="width: 55px; height: 55px; object-fit: cover; border-radius: 6px;" />',
                obj.main_image.url,
            )
        return "-"

    @admin.display(description="Preview")
    def image_preview_large(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-width: 220px; height: auto; border-radius: 8px;" />',
                obj.main_image.url,
            )
        return "No image uploaded."

    @admin.display(description="Variants")
    def variants_count(self, obj):
        return obj.variants.count()


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """
    Separate admin page for variants if needed.
    """

    list_display = (
        "product",
        "magnification",
        "price",
        "is_active",
    )

    list_editable = (
        "price",
        "is_active",
    )

    list_filter = (
        "is_active",
        "magnification",
        "product__category",
        "product__system",
    )

    search_fields = (
        "product__name",
        "magnification",
    )

    ordering = (
        "product__name",
        "price",
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "alt_text", "order")
    list_editable = ("order",)
    search_fields = ("product__name", "alt_text")
    ordering = ("product__name", "order")


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "value", "order")
    list_editable = ("order",)
    search_fields = ("product__name", "name", "value")
    ordering = ("product__name", "order")