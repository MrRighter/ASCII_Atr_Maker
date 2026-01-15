from pathlib import Path
import flet as ft
from src.core.app_logic import AppLogic


def main(page: ft.Page):
    page.title = "ASCII Art Maker"
    page.spacing = 10
    page.padding = 10

    # создаём логику и UI для приложения
    app = AppLogic(page)

    current_settings = {}

    alphabet_dict = {
        "Детализированный": [
            "Лучше подойдёт с цветным фильтром, большими фотками и RobotoMono шрифтом",
            "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`\'. "[::-1],
        ],
        "Простой": [
            "Лучше подойдёт с ч/б фильтрами, маленькими фотками и RobotoMono шрифтом",
            "#8XOHLTI)i=+;:,. "[::-1],
        ],
        "Блочный": [
            "Подойдёт любое фото с любым фильтром и блочным шрифтом",
            "█▓▒░ "[::-1],
        ],
    }

    current_file = Path(__file__).resolve()
    fonts_dir = current_file.parent.parent / "assets" / "fonts"

    font_dict = {
        "RobotoMono": [
            "Шрифт для заполнения обычными символами клавиатуры",
            fonts_dir / "RobotoMono.ttf",
        ],
        "GothicA1": [
            "Первый из подвида блочных шрифтов",
            fonts_dir / "GothicA1.ttf",
        ],
        "MPLUS1p": [
            "Второй из подвида блочных шрифтов",
            fonts_dir / "MPLUS1p.ttf",
        ],
        "NotoSansJP": [
            "Третий из подвида блочных шрифтов",
            fonts_dir / "NotoSansJP.ttf",
        ],
    }

    filling_dict = {
        "Разноцветное фото": [
            "Картинка на выходе будет цветной, как в оригинале",
            "colored",
        ],
        "Фото в ч/б (1)": [
            "Картинка на выходе будет в ч/б с 'градацией серого'",
            "monochrome1",
        ],
        "Фото в ч/б (2)": [
            "Картинка на выходе будет в ч/б с монохромным цветом",
            "monochrome2",
        ],
    }

    # создаем элементы UI
    open_button = ft.OutlinedButton(
        "Выбрать фото",
        icon=ft.Icons.ADD_PHOTO_ALTERNATE,
        on_click=app.handle_pick_file,
        height=45,
        col={"xs": 12, "sm": 6, "md": 4, "lg": 2.4, "xl": 2.4},
    )

    change_button = ft.OutlinedButton(
        "Преобразовать фото",
        disabled=True,
        icon=ft.Icons.REFRESH,
        on_click=app.handle_ascii_converter,
        height=45,
        col={"xs": 12, "sm": 6, "md": 4, "lg": 2.4, "xl": 2.4},
    )

    save_button = ft.OutlinedButton(
        "Скачать как PNG",
        disabled=True,
        icon=ft.Icons.DOWNLOAD,
        on_click=app.handle_save_file,
        height=45,
        col={"xs": 12, "sm": 6, "md": 4, "lg": 2.4, "xl": 2.4},
    )

    save_text_button = ft.OutlinedButton(
        "Скачать как текст",
        disabled=True,
        icon=ft.Icons.DESCRIPTION,
        height=45,
        col={"xs": 12, "sm": 6, "md": 4, "lg": 2.4, "xl": 2.4},
    )

    copy_text_button = ft.OutlinedButton(
        "Скопировать как текст",
        disabled=True,
        icon=ft.Icons.COPY,
        height=45,
        col={"xs": 12, "sm": 6, "md": 4, "lg": 2.4, "xl": 2.4},
    )

    image_view = ft.Image(
        src="../assets/icon.png",
        col={"xs": 12, "sm": 8, "md": 7, "lg": 5, "xl": 4},
        border_radius=ft.BorderRadius.only(
            top_left=10,
            top_right=10,
            bottom_left=10,
            bottom_right=10,
        ),
    )

    loading_text = ft.Text(
        value="Загрузка...",
        visible=False,
        theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
    )

    progress_bar = ft.ProgressBar(
        visible=False,
        color=ft.Colors.GREEN,
        col={"xs": 12, "sm": 9, "md": 8, "lg": 7, "xl": 6},
    )

    # кнопка с настройками изображения поверх всего приложения
    page.floating_action_button = ft.FloatingActionButton(
        tooltip="Настройки будущего изображения",
        icon=ft.Icons.MENU,
        on_click=lambda e: page.show_dialog(sheet),
    )

    def slider_changed(e: ft.Event[ft.Slider]):
        """Высвечивает сообщение о выбранном значении слайдера"""
        scale_value = round(e.control.value, 2)
        message_scale.value = f"Выбранное значение: {scale_value}"
        # обновляем настройки
        current_settings['scale'] = scale_value
        app.set_settings(**current_settings)
        page.update()

    scale_slider = ft.Slider(
        min=0.02,
        max=0.5,
        divisions=24,
        value=0.1,
        on_change=slider_changed,
        active_color=ft.Colors.GREEN,
    )

    def alfabet_dropdown_changed(e: ft.Event[ft.DropdownM2]):
        """Высвечивает и возвращает данные по выбранному алфавиту"""
        alfabet = e.control.value
        message_alfabet.value = f"Выбранный алфавит: {alfabet}\n{alphabet_dict[alfabet][0]}"
        # обновляем настройки
        current_settings['chars'] = alphabet_dict[alfabet][1]
        app.set_settings(**current_settings)
        page.update()

    alfabet_dropdown = ft.DropdownM2(
        value="Простой",
        label="Алфавит",
        hint_text="Выберите символы для заполнения",
        on_change=alfabet_dropdown_changed,
        options=[
            ft.dropdownm2.Option("Детализированный"),
            ft.dropdownm2.Option("Простой"),
            ft.dropdownm2.Option("Блочный"),
        ],
    )

    def font_dropdown_changed(e: ft.Event[ft.DropdownM2]):
        """Высвечивает и возвращает данные по выбранному шрифту"""
        font = e.control.value
        message_font.value = f"Выбранный шрифт: {font}\n{font_dict[font][0]}"
        # обновляем настройки
        current_settings['name_font'] = font_dict[font][1]
        app.set_settings(**current_settings)
        page.update()

    font_dropdown = ft.DropdownM2(
        value="RobotoMono",
        label="Шрифт",
        hint_text="Выберите шрифт для заполнения",
        on_change=font_dropdown_changed,
        options=[
            ft.dropdownm2.Option("GothicA1"),
            ft.dropdownm2.Option("MPLUS1p"),
            ft.dropdownm2.Option("NotoSansJP"),
            ft.dropdownm2.Option("RobotoMono"),
        ],
    )

    def filling_dropdown_changed(e: ft.Event[ft.DropdownM2]):
        """Высвечивает и возвращает данные по выбранной цветовой палитре"""
        filling = e.control.value
        message_filling.value = f"Выбранное цветовое решение: {filling}\n{filling_dict[filling][0]}"
        # обновляем настройки
        current_settings['filling'] = filling_dict[filling][1]
        app.set_settings(**current_settings)
        page.update()

    filling_dropdown = ft.DropdownM2(
        value="Разноцветное фото",
        label="Цветовое решение",
        hint_text="Выберите фильтр для заполнения",
        on_change=filling_dropdown_changed,
        options=[
            ft.dropdownm2.Option("Разноцветное фото"),
            ft.dropdownm2.Option("Фото в ч/б (1)"),
            ft.dropdownm2.Option("Фото в ч/б (2)"),
        ],
    )

    # дополнительное окно с настройки для фото
    sheet = ft.BottomSheet(
        fullscreen=True,
        show_drag_handle=True,
        content=ft.Container(
            padding=ft.Padding.all(10),
            content=ft.Column(
                controls=[
                    scale_slider,
                    message_scale := ft.Text(),
                    alfabet_dropdown,
                    message_alfabet := ft.Text(),
                    font_dropdown,
                    message_font := ft.Text(),
                    filling_dropdown,
                    message_filling := ft.Text(),
                ],
            ),
        ),
    )

    # инициализируем все UI элементы
    app.set_ui_elements(
        image_view=image_view,
        change_button=change_button,
        save_button=save_button,
        save_text_button=save_text_button,
        copy_text_button=copy_text_button,
        loading_text=loading_text,
        progress_bar=progress_bar,
        scale_slider=scale_slider,
        alfabet_dropdown=alfabet_dropdown,
        font_dropdown=font_dropdown,
        sheet=sheet,
    )

    # устанавливаем значения по умолчанию
    current_settings = {
        "scale": scale_slider.value,
        "chars": alphabet_dict[alfabet_dropdown.value][1],
        "name_font": font_dict[font_dropdown.value][1],
        "filling": filling_dict[filling_dropdown.value][1],
    }

    # инициализируем настройки для будущего фото
    app.set_settings(**current_settings)

    # Добавляем элементы на страницу
    page.add(
        ft.ResponsiveRow(
            spacing=10,
            run_spacing=10,
            controls=[
                open_button,
                change_button,
                save_button,
                save_text_button,
                copy_text_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.ResponsiveRow(
            spacing=10,
            run_spacing=10,
            controls=[image_view,],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.ResponsiveRow(
            spacing=10,
            run_spacing=10,
            controls=[
                loading_text,
                progress_bar,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )
