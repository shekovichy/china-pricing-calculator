"""
يولّد أيقونات التطبيق بصيغ مختلفة لدعم التثبيت على الموبايل واللابتوب.
اللوجو بقى صورة جاهزة (branding/logo-source.png) بدل ما يتترسم بالكود —
السكريبت ده بيربّعها ويعمل resize لكل مقاس، مش بيصمم حاجة من عنده.
شغّله مرة واحدة لو الصورة اتغيّرت، ثم سيبه — مش جزء من التطبيق نفسه.
"""
from PIL import Image

SOURCE = "C:/Projects/china-pricing-calculator/branding/logo-source.png"
OUT = "C:/Projects/china-pricing-calculator/icons"


def load_squared_source():
    """يحمّل الصورة الأصلية ويربّعها (لو مش مربعة بالظبط) بلون الخلفية نفسه، من غير ما يشوّه المحتوى."""
    img = Image.open(SOURCE).convert("RGBA")
    w, h = img.size
    if w == h:
        return img
    bg = img.getpixel((2, 2))
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), bg)
    canvas.paste(img, ((side - w) // 2, (side - h) // 2), img)
    return canvas


def load_mark_only():
    """قصّ الأيقونة (السفينة+الآلة الحاسبة) لوحدها من غير النص — النص كامل مبيبقاش مقروء في مقاسات
    الفافيكون الصغيرة (٣٢/٤٨ بكسل) أيًّا كان تصميمه، فالمقاسات الصغيرة دي بس بتاخد الرمز من غير النص،
    والمقاسات الكبيرة (192/512/ماسكابل/آبل) بتاخد اللوجو الكامل زي ما هو."""
    img = Image.open(SOURCE).convert("RGBA")
    bg = img.getpixel((2, 2))
    cropped = img.crop((15, 5, 490, 255))
    w, h = cropped.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), bg)
    canvas.paste(cropped, ((side - w) // 2, (side - h) // 2), cropped)
    return canvas


def make_icon(size, rounded_source, filename, safe_padding=0.0):
    if safe_padding:
        bg = rounded_source.getpixel((2, 2))
        canvas = Image.new("RGBA", (size, size), bg)
        content_size = int(size * (1 - safe_padding * 2))
        resized = rounded_source.resize((content_size, content_size), Image.LANCZOS)
        offset = (size - content_size) // 2
        canvas.paste(resized, (offset, offset), resized)
        canvas.save(filename)
    else:
        rounded_source.resize((size, size), Image.LANCZOS).save(filename)
    print("saved", filename, size)


if __name__ == "__main__":
    src = load_squared_source()
    mark = load_mark_only()
    make_icon(192, src, f"{OUT}/icon-192.png")
    make_icon(512, src, f"{OUT}/icon-512.png")
    make_icon(512, src, f"{OUT}/icon-maskable-512.png", safe_padding=0.1)
    make_icon(180, src, f"{OUT}/apple-touch-icon.png")
    make_icon(48, mark, f"{OUT}/favicon-48.png", safe_padding=0.06)
    make_icon(32, mark, f"{OUT}/favicon-32.png", safe_padding=0.06)
