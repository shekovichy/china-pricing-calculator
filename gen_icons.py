"""
يولّد أيقونات التطبيق بصيغ مختلفة لدعم التثبيت على الموبايل واللابتوب.
شغّله مرة واحدة عند تغيير التصميم، ثم احذفه أو سيبه — مش جزء من التطبيق نفسه.
"""
from PIL import Image, ImageDraw, ImageFont

WHITE = (255, 255, 255)
FONT_PATH = "C:/Windows/Fonts/tahomabd.ttf"


def draw_gradient_bg(size, primary, primary_dark):
    img = Image.new("RGB", (size, size), primary)
    draw = ImageDraw.Draw(img)
    for y in range(size):
        t = y / size
        r = int(primary[0] + (primary_dark[0] - primary[0]) * t)
        g = int(primary[1] + (primary_dark[1] - primary[1]) * t)
        b = int(primary[2] + (primary_dark[2] - primary[2]) * t)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    return img


def rounded_mask(size, radius_ratio=0.22):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    radius = int(size * radius_ratio)
    draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
    return mask


def add_letter(img, size, letter, letter_scale=0.56):
    draw = ImageDraw.Draw(img)
    font_size = int(size * letter_scale)
    font = ImageFont.truetype(FONT_PATH, font_size)
    bbox = draw.textbbox((0, 0), letter, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1] - size * 0.03
    draw.text((x, y), letter, font=font, fill=WHITE)
    return img


def make_icon(size, primary, primary_dark, letter, rounded=True, safe_padding=0.0, filename=None):
    canvas_size = size
    content_size = int(size * (1 - safe_padding * 2)) if safe_padding else size
    bg = draw_gradient_bg(content_size, primary, primary_dark)
    add_letter(bg, content_size, letter)

    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    offset = (canvas_size - content_size) // 2
    if rounded and not safe_padding:
        mask = rounded_mask(content_size)
        canvas.paste(bg, (offset, offset), mask)
    else:
        canvas.paste(bg, (offset, offset))
    canvas.save(filename)
    print("saved", filename, size)


if __name__ == "__main__":
    out = "C:/Projects/china-pricing-calculator/icons"

    # سعّرلي — زعفران/بابريكا
    SAARLI_PRIMARY = (224, 141, 44)      # #e08d2c
    SAARLI_DARK = (168, 71, 26)          # #a8471a
    make_icon(192, SAARLI_PRIMARY, SAARLI_DARK, "س", rounded=True, filename=f"{out}/icon-192.png")
    make_icon(512, SAARLI_PRIMARY, SAARLI_DARK, "س", rounded=True, filename=f"{out}/icon-512.png")
    make_icon(512, SAARLI_PRIMARY, SAARLI_DARK, "س", rounded=False, safe_padding=0.1, filename=f"{out}/icon-maskable-512.png")
    make_icon(180, SAARLI_PRIMARY, SAARLI_DARK, "س", rounded=False, filename=f"{out}/apple-touch-icon.png")
    make_icon(48, SAARLI_PRIMARY, SAARLI_DARK, "س", rounded=True, filename=f"{out}/favicon-48.png")
    make_icon(32, SAARLI_PRIMARY, SAARLI_DARK, "س", rounded=True, filename=f"{out}/favicon-32.png")

    # عبد الرازق في الصين — نيلي/بنفسجي
    AR_PRIMARY = (124, 58, 237)          # #7c3aed
    AR_DARK = (91, 33, 182)              # #5b21b6
    make_icon(192, AR_PRIMARY, AR_DARK, "ع", rounded=True, filename=f"{out}/icon-abdelrazek-192.png")
