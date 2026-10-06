from io import BytesIO
import unicodedata

import arabic_reshaper
from bidi.algorithm import get_display
from django.conf import settings
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .choices import FRAME_COLOR_CHOICES


# الاحتفاظ بالتشكيل مع ضبط موضعه قبل ترتيب النص بصريًا.
ARABIC_RESHAPER = arabic_reshaper.ArabicReshaper(
    configuration={
        "delete_harakat": False,
        "shift_harakat_position": True,
    }
)

ARABIC_FONT_NAME = "AMTECHDejaVuSans"


def build_contract_pdf(contract):
    """تعبئة العقد الأصلي ببيانات عربية أو إنجليزية."""

    template_path = (
        settings.BASE_DIR
        / "static"
        / "pdfs"
        / "AMTECH_Contract_Form_2026.pdf"
    )

    font_path = (
        settings.BASE_DIR
        / "static"
        / "fonts"
        / "DejaVuSans.ttf"
    )

    if not template_path.is_file():
        raise ValueError("The original contract PDF is missing.")

    if not font_path.is_file():
        raise ValueError(
            "The PDF font is missing: static/fonts/DejaVuSans.ttf"
        )

    # تسجيل الخط مرة واحدة في عملية تشغيل Django.
    if ARABIC_FONT_NAME not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(
            TTFont(ARABIC_FONT_NAME, str(font_path))
        )

    # نقرأ الأصل دون تعديل ملفه على الجهاز.
    original = PdfReader(str(template_path))
    page = original.pages[0]

    width = float(page.mediabox.width)
    height = float(page.mediabox.height)

    # طبقة شفافة نكتب عليها البيانات ثم ندمجها فوق الأصل.
    overlay_buffer = BytesIO()
    layer = canvas.Canvas(
        overlay_buffer,
        pagesize=(width, height),
    )
    layer.setFillColorRGB(0, 0, 0)

    def write_text(value, x, top, max_width, font_size=9):
        """تجهيز النص وكتابته داخل حدوده بدون قص البيانات."""

        text = "" if value is None else str(value)
        text = unicodedata.normalize("NFC", text)
        text = " ".join(text.split())

        if not text:
            return

        # تحديد اتجاه النص من أول حرف ذي اتجاه واضح.
        # الأرقام وعلامات الترقيم لا تحدد الاتجاه بمفردها.
        base_direction = "L"

        for character in text:
            direction = unicodedata.bidirectional(character)

            if direction in ("R", "AL"):
                base_direction = "R"
                break

            if direction == "L":
                break

        contains_rtl = any(
            unicodedata.bidirectional(character) in ("R", "AL")
            for character in text
        )

        # ربط الحروف العربية ثم ترتيب النص المختلط بصريًا.
        if contains_rtl:
            shaped_text = ARABIC_RESHAPER.reshape(text)
            display_text = get_display(
                shaped_text,
                base_dir=base_direction,
            )
        else:
            display_text = text

        # الإبقاء على خط الإنجليزية السابق،
        # واستخدام الخط المدمج للنصوص غير الإنجليزية.
        font_name = (
            "Helvetica" if text.isascii() else ARABIC_FONT_NAME
        )

        size = font_size
        text_width = pdfmetrics.stringWidth(
            display_text, font_name, size
        )

        # تصغير الخط عند الحاجة داخل نفس مساحة الخانة.
        while text_width > max_width and size > 6:
            size = max(6, size - 0.25)
            text_width = pdfmetrics.stringWidth(
                display_text, font_name, size
            )

        if text_width > max_width:
            raise ValueError(
                f"Text is too long for its PDF field: {text}"
            )

        # العربي يبدأ من يمين الخانة، والإنجليزي من يسارها.
        draw_x = x

        if base_direction == "R":
            draw_x = x + max_width - text_width

        # ضبط مسافات الحروف صراحة حتى لا نتأثر بإعدادات الأصل.
        layer.saveState()

        text_object = layer.beginText()
        text_object.setTextOrigin(draw_x, height - top)
        text_object.setFont(font_name, size)
        text_object.setCharSpace(0)
        text_object.setWordSpace(0)
        text_object.setHorizScale(100)
        text_object.setTextRenderMode(0)
        text_object.textOut(display_text)

        layer.drawText(text_object)
        layer.restoreState()

    # بيانات العقد والعميل.
    write_text(contract.place, 268, 99, 275)

    rep_name = (
        contract.sales_rep.get_full_name()
        or contract.sales_rep.username
    )
    write_text(rep_name, 286, 120, 255)
    write_text(contract.name, 80, 141, 270)

    date_text = (
        contract.date.strftime("%d/%m/%Y")
        if contract.date
        else ""
    )
    write_text(date_text, 392, 141, 150)

    write_text(contract.speciality, 104, 165, 435)
    write_text(contract.address, 89, 189, 450)
    write_text(contract.city, 72, 214, 145)
    write_text(contract.country, 274, 214, 265)
    write_text(contract.mobile, 89, 239, 140)
    write_text(contract.email, 270, 239, 269)

    # وصفة العين: مواقع الأعمدة والصفوف التي اختبرناها.
    rx_columns = {
        "sph": (66, 37),
        "cyl": (110, 37),
        "axis": (154, 37),
        "add": (198, 35),
    }

    rx_rows = {
        "r": 308,
        "l": 333,
    }

    for eye, top in rx_rows.items():
        for field, (x, max_width) in rx_columns.items():
            value = getattr(contract, f"{eye}_{field}", "")
            write_text(value, x, top, max_width, font_size=8)

    # مواضع صفوف القياسات الأربعة.
    measurement_rows = {
        1: 302,
        2: 314,
        3: 327,
        4: 340,
    }

    measurement_columns = {
        "distance_pd": {
            "r": (262, 39),
            "l": (308, 39),
            "t": (354, 39),
        },
        "wdpp": {
            "r": (401, 43),
            "l": (453, 43),
            "t": (506, 43),
        },
    }

    # الخانات غير المستخدمة تظل فارغة.
    for prefix, columns in measurement_columns.items():
        for row, top in measurement_rows.items():
            for column, (x, max_width) in columns.items():
                field_name = f"{prefix}_{row}_{column}"
                value = getattr(contract, field_name, "")
                write_text(value, x, top, max_width, font_size=8)

    # الأسعار والإجماليات المحسوبة من الموديل.
    pricing_fields = (
        ("loupes_price", 551),
        ("prescription_price", 566),
        ("led_price", 581),
        ("subtotal", 596),
        ("discount", 611),
        ("total", 626),
    )

    for field_name, top in pricing_fields:
        amount = getattr(contract, field_name, None)

        if amount is not None:
            write_text(
                f"{amount:,.2f}",
                266,
                top,
                77,
                font_size=9,
            )

    def mark_checkbox(x, top):
        """رسم علامة X داخل مربع الاختيار."""
        y = height - top

        layer.saveState()
        layer.setStrokeColorRGB(0, 0, 0)
        layer.setLineWidth(0.8)

        layer.line(x - 1.8, y - 1.8, x + 1.8, y + 1.8)
        layer.line(x - 1.8, y + 1.8, x + 1.8, y - 1.8)

        layer.restoreState()

    # مواقع مربعات التكبير.
    magnification_positions = {
        "2.5x Galilean": (49.7, 397.5),
        "3.0x Galilean": (49.7, 412.5),
        "3.5x Galilean": (49.7, 427.5),
        "4.0x Prismatic": (49.7, 442.5),
        "5.0x Prismatic": (49.7, 457.5),
        "6.0x Ergo": (49.7, 472.5),
        "8.0x Ergo": (49.7, 487.5),
    }

    lens_positions = {
        "TTL1": (146.7, 397.5),
        "TTL2": (146.7, 412.5),
        "TTL3": (146.7, 427.5),
        "TTL5": (146.7, 442.5),
        "TTLA1": (146.7, 457.5),
        "TTLA2": (146.7, 472.5),
        "TTLA3": (146.7, 487.5),
    }

    frame_positions = {
        "AM559": (222, 397.5),
        "ESPORT": (222, 412.5),
        "AM280Ti": (222, 427.5),
        "AM260Ti": (222, 442.5),
        "AM100Ti": (222, 457.5),
        "AM320": (222, 472.5),
        "AM310": (222, 487.5),
    }

    light_positions = {
        "HLP03": (49.7, 547.5),
        "USB LED Mini Light": (49.7, 567.5),
        "WHLP01": (49.7, 587.5),
        "Energy I": (49.7, 608),
    }

    # رفض الخيارات غير المعروفة بدل تجاهلها.
    selection_groups = (
        ("magnification", magnification_positions),
        ("lens_type", lens_positions),
        ("lights", light_positions),
    )

    for field_name, positions in selection_groups:
        selected_values = getattr(contract, field_name, []) or []

        for value in selected_values:
            if value not in positions:
                raise ValueError(
                    f"Unknown PDF option for {field_name}: {value}"
                )

            mark_checkbox(*positions[value])

    # الفريم اختيار واحد.
    selected_frame = getattr(contract, "frame", "")

    if selected_frame:
        if selected_frame not in frame_positions:
            raise ValueError(
                f"Unknown PDF frame: {selected_frame}"
            )

        mark_checkbox(*frame_positions[selected_frame])

    # ترتيب المواقع مطابق لترتيب الألوان في choices.py.
    color_positions = {
        "AM559": [
            (285, 397.5),
            (333.5, 397.5),
            (393.5, 397.5),
            (453.5, 397.5),
        ],
        "ESPORT": [
            (285, 412.5),
            (333.5, 412.5),
            (393.5, 412.5),
            (453.5, 412.5),
            (487, 412.5),
            (519.5, 412.5),
        ],
        "AM280Ti": [
            (285, 427.5),
            (333.5, 427.5),
            (393.5, 427.5),
            (453.5, 427.5),
        ],
        "AM260Ti": [
            (285, 442.5),
            (333.5, 442.5),
            (393.5, 442.5),
            (453.5, 442.5),
        ],
        "AM100Ti": [
            (285, 457.5),
            (333.5, 457.5),
            (393.5, 457.5),
            (453.5, 457.5),
        ],
        "AM320": [
            (285, 472.5),
            (333.5, 472.5),
            (393.5, 472.5),
            (453.5, 472.5),
            (519.5, 472.5),
        ],
        "AM310": [
            (285, 487.5),
            (333.5, 487.5),
            (393.5, 487.5),
            (453.5, 487.5),
        ],
    }

    selected_color = getattr(contract, "color", "")

    if selected_color:
        allowed_colors = [
            value
            for value, label in FRAME_COLOR_CHOICES.get(
                selected_frame, []
            )
        ]

        if selected_color not in allowed_colors:
            raise ValueError(
                f"Color {selected_color!r} is not supported "
                f"for frame {selected_frame!r}."
            )

        positions = color_positions[selected_frame]

        if len(positions) != len(allowed_colors):
            raise ValueError(
                f"PDF color positions do not match {selected_frame}."
            )

        color_index = allowed_colors.index(selected_color)
        mark_checkbox(*positions[color_index])

    # إنهاء طبقة البيانات ودمجها فوق العقد الأصلي.
    layer.save()
    overlay_buffer.seek(0)

    overlay = PdfReader(overlay_buffer)
    page.merge_page(overlay.pages[0])

    writer = PdfWriter()
    writer.add_page(page)

    output = BytesIO()
    writer.write(output)
    output.seek(0)

    return output