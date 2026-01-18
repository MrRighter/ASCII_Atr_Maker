import sys
from pathlib import Path
import flet as ft

sys.path.append(str(Path(__file__).parent.parent))
from core.app_logic import AppLogic


def main(page: ft.Page):
    page.title = "ASCII Art Maker"
    page.theme_mode = ft.ThemeMode.DARK
    page.spacing = 10
    page.padding = 10

    # создаём логику и UI для приложения
    app = AppLogic(page)

    current_settings = {}

    current_file = Path(__file__).resolve()
    fonts_dir = current_file.parent.parent / "assets" / "fonts"
    icon_dir = str(current_file.parent.parent / "assets" / "icon.png")

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

    # создаем стилизованные кнопки с иконками и градиентами
    button_style = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=12),
        padding=ft.Padding(16, 12, 16, 12),
        side=ft.BorderSide(1, ft.Colors.BLUE_GREY_200),
        bgcolor={
            ft.ControlState.DEFAULT: ft.Colors.BLUE_GREY_50,
            ft.ControlState.HOVERED: ft.Colors.BLUE_100,
        },
        color={
            ft.ControlState.DEFAULT: ft.Colors.BLUE_GREY_800,
            ft.ControlState.HOVERED: ft.Colors.BLUE_900,
        }
    )

    # создаем элементы UI
    open_button = ft.OutlinedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.ADD_PHOTO_ALTERNATE, size=20),
            ft.Text("Выбрать фото", size=14, weight=ft.FontWeight.W_500),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        style=button_style,
        on_click=app.handle_pick_file,
        height=50,
        col={"xs": 12, "sm": 6, "md": 4, "lg": 2.4, "xl": 2.4},
    )

    change_button = ft.OutlinedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.REFRESH, size=20),
            ft.Text("Преобразовать", size=14, weight=ft.FontWeight.W_500),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        style=button_style,
        disabled=True,
        on_click=app.handle_ascii_converter,
        height=50,
        col={"xs": 12, "sm": 6, "md": 4, "lg": 2.4, "xl": 2.4},
    )

    async def save_png_handler():
        """Вызывает функцию сохранения файла с параметром 'png'"""
        await app.handle_save_file("png")

    save_button = ft.OutlinedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.DOWNLOAD, size=20),
            ft.Text("PNG файл", size=14, weight=ft.FontWeight.W_500),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        style=button_style,
        disabled=True,
        on_click=save_png_handler,
        height=50,
        col={"xs": 12, "sm": 6, "md": 4, "lg": 2.4, "xl": 2.4},
    )

    async def save_txt_handler():
        """Вызывает функцию сохранения файла с параметром 'txt'"""
        await app.handle_save_file("txt")

    save_text_button = ft.OutlinedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.DESCRIPTION, size=20),
            ft.Text("TXT файл", size=14, weight=ft.FontWeight.W_500),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        style=button_style,
        disabled=True,
        on_click=save_txt_handler,
        height=50,
        col={"xs": 12, "sm": 6, "md": 4, "lg": 2.4, "xl": 2.4},
    )

    copy_text_button = ft.OutlinedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.COPY, size=20),
            ft.Text("Копировать", size=14, weight=ft.FontWeight.W_500),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        style=button_style,
        disabled=True,
        on_click=app.handle_copy_text,
        height=50,
        col={"xs": 12, "sm": 6, "md": 4, "lg": 2.4, "xl": 2.4},
    )

    # контейнер для изображения с эффектом свечения
    image_container = ft.Container(
        content=ft.Image(
            src=icon_dir,
            fit=ft.BoxFit.CONTAIN,
            border_radius=ft.BorderRadius.all(16),
        ),
        border_radius=ft.BorderRadius.all(20),
        padding=ft.Padding(4, 4, 4, 4),
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.5, ft.Colors.BLUE_200),
            offset=ft.Offset(0, 4),
        ),
        col={"xs": 12, "sm": 8, "md": 7, "lg": 5, "xl": 4},
        animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
    )

    loading_text = ft.Text(
        value="Загрузка...",
        visible=False,
        size=18,
        weight=ft.FontWeight.W_600,
        color=ft.Colors.BLUE_800,
    )

    progress_bar = ft.ProgressBar(
        visible=False,
        color=ft.Colors.GREEN,
        bgcolor=ft.Colors.BLUE_GREY_100,
        height=6,
        border_radius=3,
        col={"xs": 12, "sm": 9, "md": 8, "lg": 7, "xl": 6},
    )

    # боковая кнопка настроек
    page.floating_action_button = ft.FloatingActionButton(
        tooltip="Настройки изображения",
        bgcolor=ft.Colors.BLUE,
        content=ft.Container(
            padding=ft.Padding.all(4),
            border_radius=ft.BorderRadius.all(16),
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=[ft.Colors.BLUE_600, ft.Colors.PURPLE_600],
            ),
            content=ft.Icon(ft.Icons.SETTINGS, color=ft.Colors.WHITE, size=24),
        ),
        on_click=lambda e: page.show_dialog(sheet),
        shape=ft.RoundedRectangleBorder(radius=16),
    )

    def slider_changed(e: ft.Event[ft.Slider]):
        """Высвечивает сообщение о выбранном значении слайдера"""
        scale_value = round(e.control.value, 2)
        message_scale.value = f"Масштаб: {scale_value}\nP.S.: чем больше изображение, тем меньше масштаб желательно ставить"
        # обновляем настройки
        current_settings['scale'] = scale_value
        app.set_settings(**current_settings)
        page.update()

    scale_slider = ft.Slider(
        min=0.1,
        max=0.4,
        divisions=15,
        value=0.1,
        on_change=slider_changed,
        active_color=ft.Colors.BLUE,
        inactive_color=ft.Colors.BLUE_GREY_200,
    )

    def alfabet_dropdown_changed(e: ft.Event[ft.DropdownM2]):
        """Высвечивает и возвращает данные по выбранному алфавиту"""
        alfabet = e.control.value
        message_alfabet.value = alphabet_dict[alfabet][0]
        # обновляем настройки
        current_settings['chars'] = alphabet_dict[alfabet][1]
        app.set_settings(**current_settings)
        page.update()

    alfabet_dropdown = ft.DropdownM2(
        value="Простой",
        label="Алфавит символов",
        hint_text="Выберите символы для заполнения",
        on_change=alfabet_dropdown_changed,
        border_color=ft.Colors.BLUE_GREY,
        border_radius=12,
        filled=True,
        options=[
            ft.dropdownm2.Option("Детализированный"),
            ft.dropdownm2.Option("Простой"),
            ft.dropdownm2.Option("Блочный"),
        ],
    )

    def font_dropdown_changed(e: ft.Event[ft.DropdownM2]):
        """Высвечивает и возвращает данные по выбранному шрифту"""
        font = e.control.value
        message_font.value = font_dict[font][0]
        # обновляем настройки
        current_settings['name_font'] = font_dict[font][1]
        app.set_settings(**current_settings)
        page.update()

    font_dropdown = ft.DropdownM2(
        value="RobotoMono",
        label="Шрифт текста",
        hint_text="Выберите шрифт для заполнения",
        on_change=font_dropdown_changed,
        border_color=ft.Colors.BLUE_GREY,
        border_radius=12,
        filled=True,
        options=[
            ft.dropdownm2.Option("RobotoMono"),
            ft.dropdownm2.Option("GothicA1"),
            ft.dropdownm2.Option("MPLUS1p"),
            ft.dropdownm2.Option("NotoSansJP"),
        ],
    )

    def filling_dropdown_changed(e: ft.Event[ft.DropdownM2]):
        """Высвечивает и возвращает данные по выбранной цветовой палитре"""
        filling = e.control.value
        message_filling.value = filling_dict[filling][0]
        # обновляем настройки
        current_settings['filling'] = filling_dict[filling][1]
        app.set_settings(**current_settings)
        page.update()

    filling_dropdown = ft.DropdownM2(
        value="Разноцветное фото",
        label="Цветовое решение",
        hint_text="Выберите фильтр для заполнения",
        on_change=filling_dropdown_changed,
        border_color=ft.Colors.BLUE_GREY,
        border_radius=12,
        filled=True,
        options=[
            ft.dropdownm2.Option("Разноцветное фото"),
            ft.dropdownm2.Option("Фото в ч/б (1)"),
            ft.dropdownm2.Option("Фото в ч/б (2)"),
        ],
    )

    # создаем 'карточки' для каждой настройки
    scale_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ZOOM_IN, size=20, color=ft.Colors.BLUE),
                    ft.Text("Масштаб изображения", size=16, weight=ft.FontWeight.W_600),
                ], spacing=8),
                scale_slider,
                ft.Container(
                    message_scale := ft.Text("Масштаб: 0.1", size=14, color=ft.Colors.BLUE_GREY),
                    padding=ft.Padding(0, 4, 0, 0),
                ),
            ], spacing=8),
            padding=ft.Padding(16, 12, 16, 12),
        ),
        elevation=10,
        margin=ft.Margin(0, 0, 0, 10),
    )

    alphabet_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ABC, size=20, color=ft.Colors.GREEN),
                    ft.Text("Настройки символов", size=16, weight=ft.FontWeight.W_600),
                ], spacing=8),
                alfabet_dropdown,
                ft.Container(
                    message_alfabet := ft.Text(alphabet_dict["Простой"][0], size=13, color=ft.Colors.BLUE_GREY),
                    padding=ft.Padding(0, 4, 0, 0),
                ),
            ], spacing=8),
            padding=ft.Padding(16, 12, 16, 12),
        ),
        elevation=10,
        margin=ft.Margin(0, 0, 0, 10),
    )

    font_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.FONT_DOWNLOAD, size=20, color=ft.Colors.PURPLE),
                    ft.Text("Настройки шрифта", size=16, weight=ft.FontWeight.W_600),
                ], spacing=8),
                font_dropdown,
                ft.Container(
                    message_font := ft.Text(font_dict["RobotoMono"][0], size=13, color=ft.Colors.BLUE_GREY),
                    padding=ft.Padding(0, 4, 0, 0),
                ),
            ], spacing=8),
            padding=ft.Padding(16, 12, 16, 12),
        ),
        elevation=10,
        margin=ft.Margin(0, 0, 0, 10),
    )

    color_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PALETTE, size=20, color=ft.Colors.ORANGE),
                    ft.Text("Цветовые настройки", size=16, weight=ft.FontWeight.W_600),
                ], spacing=8),
                filling_dropdown,
                ft.Container(
                    message_filling := ft.Text(filling_dict["Разноцветное фото"][0], size=13, color=ft.Colors.BLUE_GREY),
                    padding=ft.Padding(0, 4, 0, 0),
                ),
            ], spacing=8),
            padding=ft.Padding(16, 12, 16, 12),
        ),
        elevation=10,
        margin=ft.Margin(0, 0, 0, 10),
    )

    # дополнительное окно с настройками по нажатию боковой кнопки
    sheet = ft.BottomSheet(
        fullscreen=True,
        show_drag_handle=True,
        content=ft.Container(
            padding=ft.Padding(20, 20, 20, 40),
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.TUNE, size=28, color=ft.Colors.BLUE),
                            ft.Text("Настройки ASCII Art", size=24, weight=ft.FontWeight.W_700),
                        ], spacing=12),
                        padding=ft.Padding(0, 0, 0, 20),
                    ),
                    scale_card,
                    alphabet_card,
                    font_card,
                    color_card,
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=4,
            ),
        ),
    )

    # инициализируем все UI элементы
    app.set_ui_elements(
        image_view=image_container.content,
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

    # добавляем элементы на страницу
    page.add(
        ft.Container(
            content=ft.ListView(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "ASCII Art Maker",
                            size=32,
                            weight=ft.FontWeight.W_800,
                            color=ft.Colors.BLUE_900
                        ),
                        alignment=ft.Alignment.CENTER,
                        padding=ft.Padding(0, 0, 0, 20),
                    ),
                    ft.ResponsiveRow(
                        spacing=12,
                        run_spacing=12,
                        controls=[
                            open_button,
                            change_button,
                            save_button,
                            save_text_button,
                            copy_text_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(height=30),
                    ft.ResponsiveRow(
                        spacing=20,
                        run_spacing=20,
                        controls=[image_container],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(height=20),
                    ft.ResponsiveRow(
                        spacing=12,
                        run_spacing=12,
                        controls=[
                            loading_text,
                            progress_bar,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=10,
                padding=20,
            ),
            expand=True,
        )
    )
