"""
يولّد أيقونات التطبيق (سعّرلي) بصيغ مختلفة لدعم التثبيت على الموبايل واللابتوب.
شغّله مرة واحدة عند تغيير التصميم، ثم احذفه أو سيبه — مش جزء من التطبيق نفسه.
"""
from PIL import Image, ImageDraw, ImageFont

PRIMARY = (15, 118, 110)       # #0f766e
PRIMARY_DARK = (11, 90, 84)    # #0b5a54
WHITE = (255, 255, 255)

FONT_PATH = "C:/Windows/Fonts/tahomabd.ttf"
LETTER = "س"

def draw_gradient_bg(size):
    img = Image.new("RGB", (size, size), PRIMARY)
    draw = ImageDraw.Draw(img)
    for y in range(size):
        t = y / size
        r = int(PRIMARY[0] + (PRIMARY_DARK[0] - PRIMARY[0]) * t)
        g = int(PRIMARY[1] + (PRIMARY_DARK[1] - PRIMARY[1]) * t)
        b = int(PRIMARY[2] + (PRIMARY_DARK[2] - PRIMARY[2]) * t)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    return img

def rounded_mask(size, radius_ratio=0.22):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    radius = int(size * radius_ratio)
    draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
    return mask

def add_letter(img, size, letter_scale=0.56):
    draw = ImageDraw.Draw(img)
    font_size = int(size * letter_scale)
    font = ImageFont.truetype(FONT_PATH, font_size)
    bbox = draw.textbbox((0, 0), LETTER, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1] - size * 0.03
    draw.text((x, y), LETTER, font=font, fill=WHITE)
    return img

def make_icon(size, rounded=True, safe_padding=0.0, filename=None):
    canvas_size = size
    content_size = int(size * (1 - safe_padding * 2)) if safe_padding else size
    bg = draw_gradient_bg(content_size)
    add_letter(bg, content_size)

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
    make_icon(192, rounded=True, filename=f"{out}/icon-192.png")
    make_icon(512, rounded=True, filename=f"{out}/icon-512.png")
    # maskable: content must fit within the safe zone (~80% center) since OS crops to its own shape
    make_icon(512, rounded=False, safe_padding=0.1, filename=f"{out}/icon-maskable-512.png")
    # apple touch icon: solid square, iOS rounds corners itself
    make_icon(180, rounded=False, filename=f"{out}/apple-touch-icon.png")
    # favicon
    make_icon(48, rounded=True, filename=f"{out}/favicon-48.png")
    make_icon(32, rounded=True, filename=f"{out}/favicon-32.png")
