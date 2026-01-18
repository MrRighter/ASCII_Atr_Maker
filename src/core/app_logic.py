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

        self.current_image: Optional[Image] = None
        self.final_image: Optional[Image] = None
        self.original_name: str = ""
        self.final_text_file: str = ""

        self.open_button: Optional[ft.OutlinedButton] = None
        self.change_button: Optional[ft.OutlinedButton] = None
        self.save_button: Optional[ft.OutlinedButton] = None
        self.save_text_button: Optional[ft.OutlinedButton] = None
        self.copy_text_button: Optional[ft.OutlinedButton] = None
        self.image_view: Optional[ft.Image] = None
        self.loading_text: Optional[ft.Text] = None
        self.progress_bar: Optional[ft.ProgressBar] = None
        self.scale_slider: Optional[ft.Slider] = None
        self.alfabet_dropdown: Optional[ft.DropdownM2] = None
        self.font_dropdown: Optional[ft.DropdownM2] = None
        self.sheet: Optional[ft.BottomSheet] = None

        self.scale: float = 0
        self.chars: str = ""
        self.name_font: str = ""
        self.filling: str = ""

    def set_ui_elements(self, **elements):
        """Устанавливает ссылки на UI-элементы"""
        for name, element in elements.items():
            setattr(self, name, element)

    def set_settings(self, **elements):
        """Устанавливает ссылки на элементы настроек будущего фото"""
        for name, element in elements.items():
            setattr(self, name, element)

    async def show_snackbar(self, message: str):
        """Показывает уведомление с определённым текстом"""
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

    async def handle_pick_file(self):
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

    async def handle_save_file(self, save_type: str):
        """Скачивает файл (PNG или TXT) в Загрузки"""
        downloads_path = str(Path.home() / "Downloads") if os.path.exists(str(Path.home() / "Downloads")) \
            else "/storage/emulated/0/Download"

        if save_type == "png":
            prefix = "AsciiArt_"
            ext = ".png"
        else:
            prefix = "AsciiArt_Text_"
            ext = ".txt"

        new_file_name = f"{prefix}{self.original_name}{ext}"
        new_file_path = os.path.join(downloads_path, new_file_name)

        counter = 1
        while os.path.exists(new_file_path):
            new_file_name = f"{prefix}{self.original_name}_{counter}{ext}"
            new_file_path = os.path.join(downloads_path, new_file_name)
            counter += 1

        try:
            self.progress_bar.visible = True
            self.loading_text.visible = True
            self.page.update()

            if save_type == "png":
                await asyncio.to_thread(self.final_image.save, new_file_path)
            else:
                with open(new_file_path, "w+", encoding="utf-8") as f:
                    await asyncio.to_thread(f.write, self.final_text_file)
            await self.show_snackbar(f"Файл успешно сохранён в '{new_file_path}'")
        except Exception as e:
            await self.show_snackbar(f"Ошибка при сохранении: {e}")
        finally:
            self.progress_bar.visible = False
            self.loading_text.visible = False
            self.page.update()

    async def handle_copy_text(self):
        """Копируем текстовый файл в буфер обмена"""
        try:
            await ft.Clipboard().set(self.final_text_file)
            await self.show_snackbar(f"Файл успешно скопирован")
        except Exception as e:
            await self.show_snackbar(f"Ошибка при копировании: {e}")

    async def update_image_view(self, img_obj: Image.Image):
        """Рисует преобразованное изображение на экране"""
        buffer = io.BytesIO()
        img_obj.save(buffer, format="PNG")
        base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
        self.image_view.src = base64_img

    async def handle_ascii_converter(self):
        """Обработка преобразования изображения"""
        self.progress_bar.visible = True
        self.loading_text.visible = True
        self.page.update()

        try:
            self.final_image, self.final_text_file = await asyncio.to_thread(
                photo_converter,
                self.current_image,
                self.scale,
                self.chars,
                self.name_font,
                self.filling
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
