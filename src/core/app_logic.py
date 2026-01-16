import sys
from pathlib import Path
import io
import base64
import os
import asyncio
from typing import Optional
import flet as ft
from PIL import Image

sys.path.append(str(Path(__file__).parent.parent))
from core.converter import photo_converter


class AppLogic:
    def __init__(self, page):
        self.page = page
        self.current_image: Optional[Image.Image] = None
        self.final_image: Optional[Image.Image] = None
        self.original_name = ""

        self.open_button = None
        self.change_button = None
        self.save_button = None
        self.save_text_button = None
        self.copy_text_button = None
        self.image_view = None
        self.loading_text = None
        self.progress_bar = None
        self.scale_slider = None
        self.alfabet_dropdown = None
        self.font_dropdown = None
        self.sheet = None

        self.scale = None
        self.chars = None
        self.name_font = None
        self.filling = None

    def set_ui_elements(self, **elements):
        """Установить ссылки на UI-элементы"""
        for name, element in elements.items():
            setattr(self, name, element)

    def set_settings(self, **elements):
        """Установить ссылки на элементы настроек будущего фото"""
        for name, element in elements.items():
            setattr(self, name, element)

    async def show_snackbar(self, message: str):
        """Показать уведомление"""
        self.page.show_dialog(
            ft.SnackBar(
                ft.Text(message),
                action=ft.SnackBarAction(
                    label="Скрыть",
                    text_color=ft.Colors.BLACK,
                    bgcolor=ft.Colors.GREEN,
                ),
            )
        )

    async def handle_pick_file(self, e=None):
        """Выбираем и загружаем выбранный файл в программу"""
        original_file = await ft.FilePicker().pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg", "bmp", "webp"]
        )

        if original_file:
            file_path = original_file[0].path
            self.original_name = os.path.splitext(os.path.basename(file_path))[0]
            self.current_image = Image.open(file_path)
            self.image_view.src = file_path
            self.change_button.disabled = False
        else:
            await self.show_snackbar(f"Изображение не выбрано")

    async def handle_save_png(self, e=None):
        """Скачиваем преобразованное фото в Загрузки"""
        downloads_path = str(Path.home() / "Downloads") if os.path.exists(str(Path.home() / "Downloads")) \
            else "/storage/emulated/0/Download"
        new_file_name = f"AsciiArt_{self.original_name}.png"
        new_file_path = os.path.join(downloads_path, new_file_name)

        counter = 1
        while os.path.exists(new_file_path):
            new_file_name = f"AsciiArt_{self.original_name}_{counter}.png"
            new_file_path = os.path.join(downloads_path, new_file_name)
            counter += 1

        try:
            self.final_image.save(new_file_path)
            await self.show_snackbar(f"Изображение успешно сохранено в '{new_file_path}'")
        except Exception as e:
            await self.show_snackbar(f"Ошибка при сохранении: {e}")

    async def update_image_view(self, img_obj: Image.Image):
        """Рисуем преобразованное изображение на экране"""
        buffer = io.BytesIO()
        img_obj.save(buffer, format="PNG")
        base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
        self.image_view.src = base64_img

    @staticmethod
    def ascii_converter(image: Image.Image, scale: float, chars: str, name_font: str, filling: str) -> Image.Image:
        """Выполняет преобразование фото в ASCII рисунок"""
        result = photo_converter(
            image=image,
            scale=scale,
            chars=chars,
            name_font=name_font,
            filling=filling,
        )

        return result

    async def handle_ascii_converter(self, e=None):
        """Обработка преобразования изображения"""
        self.progress_bar.visible = True
        self.loading_text.visible = True
        self.page.update()

        try:
            self.final_image = await asyncio.to_thread(
                self.ascii_converter, self.current_image, self.scale, self.chars, self.name_font, self.filling
            )
            await self.update_image_view(self.final_image)
            self.save_button.disabled = False
            self.save_text_button.disabled = False
            self.copy_text_button.disabled = False
        except Exception as ex:
            await self.show_snackbar(f"Ошибка при преобразовании: {ex}")
        finally:
            self.progress_bar.visible = False
            self.loading_text.visible = False
            self.page.update()
