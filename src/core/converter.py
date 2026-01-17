from pathlib import Path
from PIL import Image, ImageFont, ImageDraw


def photo_converter(image: Image.Image, scale: float, chars: str, name_font: str, filling: str) \
        -> tuple[Image.Image, str]:
    """
    Выполняет преобразование фото в ASCII рисунок.

    Args:
        image: входящее необработанное изображение
        scale: масштаб возвращаемого фото, влияет на его качество, scale ∈ (0; 0.5]
        chars: набор символов для заполнения
        name_font: путь к шрифту, который идёт на вход
        filling: цветовое заполнение

    Returns:
        tuple: готовый ASCII рисунок, текстовый файл с ASCII рисунком
    """

    image = image.convert("RGB")

    current_file = Path(__file__).resolve()
    fonts_dir = current_file.parent.parent / "assets" / "fonts"

    ratio_font = 2 if name_font == fonts_dir / "RobotoMono.ttf" else 1

    width, height = image.size
    aspect_ratio = height / width  # соотношение сторон промежуточного результата
    new_width = int(width * scale)
    new_height = int(new_width * aspect_ratio // ratio_font)  # если шрифт не квадратный, то сплющиваем фото
    img_resized = image.resize((new_width, new_height))

    pixels = img_resized.load()  # разбиваем фото по пикселям

    font_size = int(scale * 200)
    font = ImageFont.truetype(font=name_font, size=font_size)

    char_width = (font_size // ratio_font) + 2
    char_height = char_width * ratio_font
    # финальные и настоящие размеры готового изображения
    # почти один в один с оригинальным фото
    ascii_width = new_width * char_width
    ascii_height = new_height * char_height

    ascii_art = Image.new("RGB", (ascii_width, ascii_height), "black")
    draw = ImageDraw.Draw(ascii_art)  # модуль, рисующий на фото

    text_art = ""

    for i in range(new_height):
        for j in range(new_width):
            r, g, b = pixels[j, i]
            average = int((r + g + b) / 3)  # находим среднее цветовое значение каждого пикселя
            pixels[j, i] = (average, average, average)  # закрашиваем каждый пиксель "новым" цветом
            # вычисление наиболее подходящего символа для каждого пикселя по его цветовому значению
            char = chars[int((average / 255) * (len(chars) - 1))]

            x = j * char_width
            y = i * char_height
            # рисуем символ на конкретном месте одним из "цветовых фильтров"
            if filling == "colored":
                draw.text((x, y), char, font=font, fill=(r, g, b))
            elif filling == "monochrome1":
                draw.text((x, y), char, font=font, fill=(average, average, average))
            else:
                draw.text((x, y), char, font=font, fill=(255, 255, 255))

            text_art += char
        text_art += "\n"

    return ascii_art, text_art
