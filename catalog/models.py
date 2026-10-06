from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Product category.
    Example: Loupes, Headlights, Accessories.
    """

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Main product model.

    This stores the public product information shown on:
    - Products page
    - Product details page
    """

    SYSTEM_CHOICES = [
    ("ergo", "Ergo"),
    ("ttl", "TTL"),
    ("prismatic", "Prismatic"),
    ("led_headlight", "LED Headlight"),
    ("wireless_headlight", "Wireless Headlight"),
]

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)

    system = models.CharField(
        max_length=30,
        choices=SYSTEM_CHOICES,
        blank=True,
    )

    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    main_image = models.ImageField(
        upload_to="products/main/",
        blank=True,
        null=True,
    )

    # Optional reference to catalog page number.
    catalog_page = models.PositiveIntegerField(blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})

    @property
    def starting_price(self):
        """
        Returns the lowest active variant price.
        Used later to show: From 3050 SAR.
        """
        variant = self.variants.filter(is_active=True).order_by("price").first()
        return variant.price if variant else None


class ProductVariant(models.Model):
    """
    Product price/options model.

    Example:
    Product: ErgoZM
    Variant: 3.5x - 7850 SAR
    Variant: 5.0x - 9100 SAR
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    magnification = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    working_distance = models.CharField(max_length=120, blank=True)
    depth_of_focus = models.CharField(max_length=120, blank=True)
    field_of_view = models.CharField(max_length=120, blank=True)
    weight = models.CharField(max_length=120, blank=True)

    standard_frame = models.CharField(max_length=160, blank=True)
    standard_case = models.CharField(max_length=160, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["product", "price"]

    def __str__(self):
        return f"{self.product.name} - {self.magnification} - {self.price} SAR"


class ProductImage(models.Model):
    """
    Extra product gallery images.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=160, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductSpecification(models.Model):
    """
    Flexible product specifications.

    Example:
    Name: Optical System
    Value: Upgraded optical system delivers clearer visual experience.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specifications",
    )

    name = models.CharField(max_length=120)
    value = models.CharField(max_length=255)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.product.name} - {self.name}"