import io
import base64
import os
import asyncio
import flet as ft
from PIL import Image, ImageFont, ImageDraw


def main(page: ft.Page):
    page.title = "ASCII Art Maker"
    page.window.width = 1300
    page.window.height = 800
    # выравниваем всё по центру
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    current_image: Image.Image  # задаём переменную для будущего изображения
    final_image: Image.Image
    original_name = ""

    async def handle_pick_file():
        """Выбираем и загружаем выбранный файл в программу"""
        nonlocal current_image, original_name

        original_file = await ft.FilePicker().pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg", "bmp", "webp"]
        )

        if original_file:
            file_path = original_file[0].path
            original_name = os.path.splitext(os.path.basename(file_path))[0]  # берём только название изначального файла из полного пути
            current_image = Image.open(file_path)  # открываем файл по конкретному путю
            image_view.src = file_path  # передаём в блок image_view путь к файлу, чтобы показать его
            image_view.visible = True
            change_button.disabled = False
            page.update()
        else:
            page.show_dialog(ft.SnackBar(ft.Text(f"Изображение не выбрано")))

    async def handle_save_file():
        """Скачиваем преобразованное фото в желаемое место"""
        nonlocal final_image, original_name

        new_file = await ft.FilePicker().save_file(
            allowed_extensions=["png", "jpg", "jpeg", "bmp", "webp"],
            file_name=f"AsciiArt_{original_name}.png",
        )

        try:
            final_image.save(new_file)
            page.show_dialog(ft.SnackBar(ft.Text(f"Изображение успешно сохранено в '{new_file}'")))
        except Exception as e:
            page.show_dialog(ft.SnackBar(ft.Text(f"Ошибка при сохранении: {e}")))

    async def update_image_view(img_obj: Image.Image):
        """Рисуем преобразованное изображение на экране напрямую из строки, закодированной в формате Base64"""
        buffer = io.BytesIO()
        img_obj.save(buffer, format="PNG")  # сохраняем в буфер в формате PNG
        base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
        image_view.src = base64_img  # заменяем путь на новый
        progress_bar.visible = False
        loading_text.visible = False
        page.update()

    def ascii_converter_task(image: Image.Image) -> Image.Image:
        """Выполняет преобразование в ASCII в отдельной задаче
        Необходимо для корректной работы всего приложения"""
        scale = 0.3
        width, height = image.size
        aspect_ratio = height / width
        new_width = int(width * scale)
        new_height = int(new_width * aspect_ratio * 0.5)
        img_resized = image.resize((new_width, new_height))

        pixels = img_resized.load()

        # chars = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '[::-1]
        chars = "#8XOHLTI)i=+;:,. "[::-1]

        font_size = int(scale * 150)
        font = ImageFont.truetype("RobotoMono.ttf", font_size)

        char_width = (font_size // 2) + 2
        char_height = char_width * 2
        ascii_width = new_width * char_width
        ascii_height = new_height * char_height

        ASCII_Art = Image.new("RGB", (ascii_width, ascii_height), "black")
        draw = ImageDraw.Draw(ASCII_Art)

        for i in range(new_height):
            for j in range(new_width):
                r, g, b = pixels[j, i]
                average = int((r + g + b) / 3)
                pixels[j, i] = (average, average, average)
                char = chars[int((average / 255) * (len(chars) - 1))]

                x = j * char_width
                y = i * char_height
                draw.text((x, y), char, font=font, fill=(r, g, b))
                # draw.text((x, y), char, font=font, fill=(average, average, average))
                # draw.text((x, y), char, font=font, fill=("#FFFFFF"))

        return ASCII_Art

    async def ascii_converter(e):
        nonlocal current_image, final_image

        if current_image:
            progress_bar.visible = True
            loading_text.visible = True
            page.update()

            try:
                final_image = await asyncio.to_thread(ascii_converter_task, current_image)  # асинхронно выполняем преобразование фото
                await update_image_view(final_image)  # заменяем фото
                save_button.disabled = False
                ascii_text_button.disabled = False
                page.update()
            except Exception as ex:
                page.show_dialog(ft.SnackBar(ft.Text(f"Ошибка при преобразовании: {ex}")))
                progress_bar.visible = False
                loading_text.visible = False
                page.update()

    open_button = ft.Button("Выбрать фото", icon=ft.Icons.ADD_PHOTO_ALTERNATE, on_click=handle_pick_file)
    change_button = ft.Button("Преобразовать фото", disabled=True, icon=ft.Icons.REFRESH, on_click=ascii_converter)
    save_button = ft.Button("Скачать как PNG", disabled=True, icon=ft.Icons.DOWNLOAD, on_click=handle_save_file)
    ascii_text_button = ft.Button("Скачать как текст", disabled=True, icon=ft.Icons.DESCRIPTION)

    image_view = ft.Image(visible=False, width=600, height=600, src="")

    loading_text = ft.Text(value="Загрузка...", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, visible=False)
    progress_bar = ft.ProgressBar(width=600, color=ft.Colors.AMBER, visible=False)

    page.add(
        ft.Row(
            controls=[open_button, change_button, save_button, ascii_text_button],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        image_view,
        loading_text,
        progress_bar
    )

if __name__ == "__main__":
    ft.run(main)
