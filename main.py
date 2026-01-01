from PIL import Image, ImageFont, ImageDraw
import os


folder_path = "tests/photos2"

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', 'webp', 'bmp')):
        file_path = os.path.join(folder_path, filename)
        with Image.open(file_path) as img:
            scale = 0.2  # масштаб, но можно назвать и по-другому -- качество фото (лучше всего 0 < scale <= 1)

            width, height = img.size
            aspect_ratio = height / width  # соотношение сторон
            new_width = int(width * scale)
            new_height = int(new_width * aspect_ratio * 0.5)  # 0.5, потому что высота символа примерно в 2 раза больше, чем ширина
            img_resized = img.resize((new_width, new_height))  # делаем будущее фото сплющенным, необходимо для логики отрисовки символов

            pixels = img_resized.load()  # по-пиксельно разбиваем фото

            # chars = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '[::-1]  # лучше с цветным фильтром и большими фотками
            chars = "#8XOHLTI)i=+;:,. "[::-1]  # лучше с ч/б фильтрами и маленькими фотками

            font_size = int(scale * 200)
            font = ImageFont.truetype("RobotoMono.ttf", font_size)

            char_width = (font_size // 2) + 2
            char_height = char_width * 2
            # финальные и настоящие размеры готового изображения
            # почти один в один с оригинальным фото
            ascii_width = new_width * char_width
            ascii_height = new_height * char_height

            ASCII_Art = Image.new("RGB", (ascii_width, ascii_height), "black")
            draw = ImageDraw.Draw(ASCII_Art)  # модуль, рисующий на фото

            # with open("ASCII_Art.txt", "w") as text_atr:
            for i in range(new_height):
                for j in range(new_width):
                    r, g, b = pixels[j, i]
                    average = int((r + g + b) / 3)  # находим среднее цветовое значение каждого пикселя (0-255)
                    pixels[j, i] = (average, average, average)  # закрашиваем каждый пиксель "новым" цветом
                    char = chars[int((average / 255) * (len(chars) - 1))]  # вычисление наиболее подходящего символа для каждого пикселя

                    x = j * char_width
                    y = i * char_height
                    # рисуем символ на конкретном месте одним из "цветовых фильтров"
                    draw.text((x, y), char, font=font, fill=(r, g, b))  # цветной фильтр
                    # draw.text((x, y), char, font=font, fill=(average, average, average))  # ч/б с тенями фильтр
                    # draw.text((x, y), char, font=font, fill=("#FFFFFF"))  # ч/б фильтр

                    #     text_atr.write(char)
                    # text_atr.write("\n")

            new_filename = 'ASCII_' + filename
            new_folder_path = "tests/ascii_photos2"
            os.makedirs(new_folder_path, exist_ok=True)
            new_path = os.path.join(new_folder_path, new_filename)
            ASCII_Art.save(new_path)  # сохраняем файл в указанный путь
