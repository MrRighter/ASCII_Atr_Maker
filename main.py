from PIL import Image, ImageFont, ImageDraw
import os


folder_path = "photos"

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        file_path = os.path.join(folder_path, filename)
        with Image.open(file_path) as img:
            scale = 0.15

            width, height = img.size
            aspect_ratio = height / width
            new_height = int(width * aspect_ratio * 0.5 * scale)
            new_width = int(width * scale)
            img_resized = img.resize((new_width, new_height))

            pixels = img_resized.load()

            chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

            font = ImageFont.truetype("RobotoMono.ttf", 20)

            char_width = 12
            char_height = 24
            ascii_width = new_width * char_width
            ascii_height = new_height * char_height

            ASCII_Art = Image.new("RGB", (ascii_width, ascii_height), "black")
            draw = ImageDraw.Draw(ASCII_Art)

            # with open("ASCII_Art.txt", "w") as text_atr:
            for i in range(new_height):
                for j in range(new_width):
                    r, g, b = pixels[j, i]
                    average = int((r + g + b) / 3)
                    pixels[j, i] = (average, average, average)
                    char = chars[int((average / 255) * (len(chars) - 1))]

                    x = j * char_width
                    y = i * char_height
                    draw.text((x, y), char, font=font, fill=(r, g, b))

                    #     text_atr.write(char)
                    # text_atr.write("\n")

            new_filename = 'ASCII_' + filename
            new_folder_path = "ascii_photos"
            new_path = os.path.join(new_folder_path, new_filename)
            ASCII_Art.save(new_path)
