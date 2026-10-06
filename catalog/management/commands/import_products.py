from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from catalog.models import Category, Product, ProductVariant, ProductSpecification


PRODUCTS = [
    {
        "slug": "ergozm",
        "name": "ErgoZM",
        "category": "Loupes",
        "system": "ergo",
        "image": "products/main/ergozm.jpg",
        "featured": True,
        "short_description": "New ergonomic loupe system.",
        "description": "The all-new Amtech ErgoZM magnifier keeps Amtech ergonomic design while advancing feature quality. It offers a wider working distance range and precise optical comfort for clinical work.",
        "features": [
            "Ergonomic working posture",
            "Wide working distance range",
            "High comfort optics",
            "Recommended frames: Am100Ti, Am260Ti, Am280Ti, Am310, Am320, Am559",
        ],
        "variants": [
            {"magnification": "3.5x", "price": 7850, "working_distance": "400–600mm", "depth_of_focus": "90–140mm", "field_of_view": "80–130mm", "weight": "59.0g"},
            {"magnification": "5.0x", "price": 9100, "working_distance": "400–600mm", "depth_of_focus": "60–90mm", "field_of_view": "60–160mm", "weight": "61.0g"},
            {"magnification": "6.0x", "price": 9700, "working_distance": "400–600mm", "depth_of_focus": "50–70mm", "field_of_view": "100–135mm", "weight": "63.0g"},
        ],
    },
    {
        "slug": "ergoam",
        "name": "ErgoAM",
        "category": "Loupes",
        "system": "ergo",
        "image": "products/main/ergoam.jpg",
        "featured": True,
        "short_description": "Multi-power ergonomic loupe system.",
        "description": "ErgoAM is a clarity, comfort and magnification focused loupe series designed to support neck and musculoskeletal health through an ergonomic structure.",
        "features": [
            "Ergonomic structure",
            "Precision mechanical design",
            "Multiple magnification options",
            "Recommended frames: Am100Ti, Am260Ti, Am280Ti, Am310, Am320, Am559",
        ],
        "variants": [
            {"magnification": "3.5x", "price": 6050, "working_distance": "Customized", "depth_of_focus": "100–140mm", "field_of_view": "90–110mm", "weight": "54.50g"},
            {"magnification": "4.0x", "price": 7250, "working_distance": "Customized", "depth_of_focus": "90–120mm", "field_of_view": "85–110mm", "weight": "54.50g"},
            {"magnification": "5.0x", "price": 7850, "working_distance": "Customized", "depth_of_focus": "75–120mm", "field_of_view": "75–90mm", "weight": "55.50g"},
            {"magnification": "6.0x", "price": 8500, "working_distance": "Customized", "depth_of_focus": "60–80mm", "field_of_view": "55–75mm", "weight": "59.50g"},
        ],
    },
    {
        "slug": "ttla1",
        "name": "TTL-A1",
        "category": "Loupes",
        "system": "ttl",
        "image": "products/main/ttla1.jpg",
        "featured": True,
        "short_description": "Light metal-barrel TTL loupes.",
        "description": "TTL-A1 custom-craft loupes offer enhanced visual clarity with a wide field of view and superior depth of field in a fashionable metal-barrel design.",
        "features": [
            "Metal barrel design",
            "Wide field of view",
            "Superior depth of field",
            "Standard frame: E sport frame",
            "Standard case: Metal case or Fabric case C",
        ],
        "variants": [
            {"magnification": "2.5x", "price": 3050, "working_distance": "Customized", "depth_of_focus": "100–150mm", "field_of_view": "110–190mm", "weight": "46.0g"},
            {"magnification": "3.0x", "price": 3050, "working_distance": "Customized", "depth_of_focus": "90–130mm", "field_of_view": "75–170mm", "weight": "46.0g"},
            {"magnification": "3.5x", "price": 3650, "working_distance": "Customized", "depth_of_focus": "70–120mm", "field_of_view": "65–160mm", "weight": "46.0g"},
        ],
    },
    {
        "slug": "ttla3",
        "name": "TTL-A3",
        "category": "Loupes",
        "system": "ttl",
        "image": "products/main/ttla3.jpg",
        "featured": False,
        "short_description": "Ultra-light aluminum TTL loupes.",
        "description": "TTL-A3 loupes use ultra-light aluminum barrels for all-day comfort and precision, with sharpness and freedom of movement for focused work.",
        "features": [
            "Ultra-light aluminum barrels",
            "High comfort",
            "Excellent sharpness",
            "Standard frame: TR90 or Alu-mag frame",
            "Standard case: Metal case or Fabric case C",
        ],
        "variants": [
            {"magnification": "2.5x", "price": 3650, "working_distance": "Customized", "depth_of_focus": "90–120mm", "field_of_view": "130–200mm", "weight": "40.0g"},
            {"magnification": "3.0x", "price": 3650, "working_distance": "Customized", "depth_of_focus": "80–110mm", "field_of_view": "110–150mm", "weight": "42.0g"},
        ],
    },
    {
        "slug": "ttla2",
        "name": "TTL-A2",
        "category": "Loupes",
        "system": "prismatic",
        "image": "products/main/ttla2.jpg",
        "featured": False,
        "short_description": "Prismatic TTL loupes.",
        "description": "Ranging from 4.0x to 5.0x, TTL-A2 is designed for healthcare professionals who perform exacting procedures and need compact, comfortable all-day wear.",
        "features": [
            "Prismatic system",
            "Compact metallic ultra-light design",
            "Wide edge-to-edge clear field",
            "Standard frame: TR90 or Alu-mag frame",
            "Standard case: Metal case or Fabric case C",
        ],
        "variants": [
            {"magnification": "4.0x", "price": 4850, "working_distance": "Customized", "depth_of_focus": "65–85mm", "field_of_view": "100–150mm", "weight": "51.0g"},
            {"magnification": "5.0x", "price": 5450, "working_distance": "Customized", "depth_of_focus": "60–75mm", "field_of_view": "80–120mm", "weight": "52.0g"},
        ],
    },
    {
        "slug": "ttl3",
        "name": "TTL 3",
        "category": "Loupes",
        "system": "ttl",
        "image": "products/main/ttl3.jpg",
        "featured": False,
        "short_description": "Mini square TTL loupes.",
        "description": "TTL 3 focuses on comfortable experience and lightest weight, with micro-size design for daily clinical performance.",
        "features": [
            "Mini square design",
            "Micro-size and light weight",
            "Comfort-focused performance",
            "Standard frame: E sport frame",
            "Standard case: Metal case or Fabric case C",
        ],
        "variants": [
            {"magnification": "2.5x", "price": 3050, "working_distance": "Customized", "depth_of_focus": "110–150mm", "field_of_view": "115–180mm", "weight": "42.0g"},
            {"magnification": "3.0x", "price": 3050, "working_distance": "Customized", "depth_of_focus": "90–130mm", "field_of_view": "70–165mm", "weight": "42.0g"},
            {"magnification": "3.5x", "price": 3650, "working_distance": "Customized", "depth_of_focus": "70–120mm", "field_of_view": "65–175mm", "weight": "42.0g"},
        ],
    },
    {
        "slug": "ttl5",
        "name": "TTL 5",
        "category": "Loupes",
        "system": "ttl",
        "image": "products/main/ttl5.jpg",
        "featured": False,
        "short_description": "Mini round TTL loupes.",
        "description": "TTL 5 combines round design with light weight for a comfortable all-day clinical experience and expected visual clarity.",
        "features": [
            "Mini round design",
            "Lightweight build",
            "Wide field of view",
            "Standard frame: TR90 or Alu-mag frame",
            "Standard case: Metal case or Fabric case C",
        ],
        "variants": [
            {"magnification": "2.5x", "price": 3650, "working_distance": "Customized", "depth_of_focus": "90–110mm", "field_of_view": "120–160mm", "weight": "38.0g"},
            {"magnification": "3.0x", "price": 3650, "working_distance": "Customized", "depth_of_focus": "80–100mm", "field_of_view": "110–150mm", "weight": "41.0g"},
        ],
    },
    {
        "slug": "ttl1",
        "name": "TTL 1",
        "category": "Loupes",
        "system": "ttl",
        "image": "products/main/ttl1.jpg",
        "featured": False,
        "short_description": "Classic value TTL loupes.",
        "description": "TTL 1 sets an industry standard for comfort and performance, delivering a strong field of view and depth of field at an economical price.",
        "features": [
            "Classic TTL system",
            "Economical price",
            "Strong field of view",
            "Standard frame: Ni-alloy frame or E sport frame",
            "Standard case: Fabric case B or Fabric case C",
        ],
        "variants": [
            {"magnification": "2.5x", "price": 2450, "working_distance": "Customized", "depth_of_focus": "110–150mm", "field_of_view": "115–180mm", "weight": "51.0g"},
            {"magnification": "3.0x", "price": 2450, "working_distance": "Customized", "depth_of_focus": "90–130mm", "field_of_view": "70–165mm", "weight": "51.0g"},
            {"magnification": "3.5x", "price": 3050, "working_distance": "Customized", "depth_of_focus": "70–120mm", "field_of_view": "65–175mm", "weight": "51.0g"},
        ],
    },
    {
        "slug": "ttl2",
        "name": "TTL 2",
        "category": "Loupes",
        "system": "prismatic",
        "image": "products/main/ttl2.jpg",
        "featured": False,
        "short_description": "High power prismatic loupes.",
        "description": "TTL 2 achieves higher power and higher definition for surgical procedures that require strong resolution and clarity.",
        "features": [
            "Prismatic system",
            "High power magnification",
            "Surgical clarity",
            "Standard frame: E sport frame",
            "Standard case: Fabric case A or Fabric case C",
        ],
        "variants": [
            {"magnification": "4.0x", "price": 4250, "working_distance": "Customized", "depth_of_focus": "65–80mm", "field_of_view": "80–130mm", "weight": "54.0g"},
            {"magnification": "5.0x", "price": 4850, "working_distance": "Customized", "depth_of_focus": "55–70mm", "field_of_view": "70–120mm", "weight": "54.0g"},
        ],
    },
    {
        "slug": "energy-i",
        "name": "Energy I",
        "category": "Headlights",
        "system": "led_headlight",
        "image": "products/main/energy-i.jpg",
        "featured": True,
        "short_description": "Semi-wired LED headlight.",
        "description": "Energy I is a neck-hanging headlight that integrates the battery into a wearable design, reducing head pressure while providing gesture-controlled brightness.",
        "features": [
            "Semi-wired LED headlight",
            "Gesture sensor control",
            "Magnetic headlight connection",
            "Up to 8 hours of continuous work",
        ],
        "variants": [
            {"magnification": "Headlight", "price": 4850, "working_distance": "—", "depth_of_focus": "Brightness ≥55,000lux", "field_of_view": "5500k or 6000k", "weight": "10g headlight / 88.5g battery"},
        ],
    },
    {
        "slug": "whlp01",
        "name": "WHLP01",
        "category": "Headlights",
        "system": "wireless_headlight",
        "image": "products/main/whlp01.jpg",
        "featured": False,
        "short_description": "Wireless LED headlight.",
        "description": "WHLP01 is a wireless LED light with a powerful round focus white light, touchable power switch and brightness adjustment.",
        "features": [
            "Wireless LED light",
            "Touchable power and brightness adjustment",
            "Available in 5500k or 6100k",
            "Up to 3.5 hours run time",
        ],
        "variants": [
            {"magnification": "Headlight", "price": 4250, "working_distance": "—", "depth_of_focus": "Brightness ≥35,000lux", "field_of_view": "5500k or 6100k", "weight": "10g headlight / 20g battery"},
        ],
    },
    {
        "slug": "hlp05",
        "name": "HLP05",
        "category": "Headlights",
        "system": "led_headlight",
        "image": "products/main/hlp05.jpg",
        "featured": False,
        "short_description": "Mini USB LED light.",
        "description": "HLP05 is a mini USB cable connection light with electromagnetic current protection and small, bright design for dental work.",
        "features": [
            "Mini USB cable connection",
            "Curing filter included",
            "6000k light color temp",
            "3–4 hours recharge time",
        ],
        "variants": [
            {"magnification": "Headlight", "price": 3050, "working_distance": "1W power", "depth_of_focus": "Brightness ≥35,000lux", "field_of_view": "6000k", "weight": "8g headlight / 88.35g battery"},
        ],
    },
    {
        "slug": "hlp03",
        "name": "HLP03",
        "category": "Headlights",
        "system": "led_headlight",
        "image": "products/main/hlp03.jpg",
        "featured": False,
        "short_description": "Power supply LED set.",
        "description": "HLP03 provides true white light brightness and shadow-free operation. The reliable power supply keeps surgeries running smoothly all day long.",
        "features": [
            "True white light",
            "Shadow-free operation field",
            "Curing filter included",
            "6–9 hours run time",
        ],
        "variants": [
            {"magnification": "Headlight", "price": 3650, "working_distance": "3W power", "depth_of_focus": "Brightness ≥35,000lux", "field_of_view": "6000k", "weight": "22.35g headlight / 135g battery"},
        ],
    },
]


class Command(BaseCommand):
    help = "Import AMTECH final catalogue products"

    def handle(self, *args, **options):
        for item in PRODUCTS:
            category, _ = Category.objects.get_or_create(
                name=item["category"],
                defaults={
                    "slug": slugify(item["category"]),
                    "is_active": True,
                },
            )

            product, created = Product.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "category": category,
                    "name": item["name"],
                    "system": item["system"],
                    "short_description": item["short_description"],
                    "description": item["description"],
                    "main_image": item["image"],
                    "is_featured": item["featured"],
                    "is_active": True,
                },
            )

            product.variants.all().delete()
            product.specifications.all().delete()

            for variant in item["variants"]:
                ProductVariant.objects.create(
                    product=product,
                    magnification=variant["magnification"],
                    price=Decimal(str(variant["price"])),
                    working_distance=variant["working_distance"],
                    depth_of_focus=variant["depth_of_focus"],
                    field_of_view=variant["field_of_view"],
                    weight=variant["weight"],
                    is_active=True,
                )

            for index, feature in enumerate(item["features"], start=1):
                ProductSpecification.objects.create(
                    product=product,
                    name=f"Feature {index}",
                    value=feature,
                    order=index,
                )

            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action}: {product.name}"))

        self.stdout.write(self.style.SUCCESS("AMTECH products import completed."))