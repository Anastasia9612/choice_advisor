import flet as ft
from nlp2 import predict_language  # Импортируем функцию из основного файла
from tree import choose_top_3_languages, criteria, scores  # Импортируем функцию дерева решений и критерии

# Основная функция для запуска приложения
def main(page: ft.Page):
    # Настройки страницы
    page.title = "Определение языка программирования"
    page.theme_mode = ft.ThemeMode.LIGHT  # Светлая тема
    page.padding = 50
    page.bgcolor = ft.colors.GREY_100  # Фон страницы
    page.scroll = ft.ScrollMode.AUTO  # Включаем прокрутку

    # Заголовок
    title = ft.Text(
        "Определение языка программирования",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_800,
        text_align=ft.TextAlign.CENTER,  # Выравнивание по центру
    )

    # Поле для ввода текста
    text_input = ft.TextField(
        label="Введите текст задачи",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=600,
        border_color=ft.colors.BLUE_800,
        focused_border_color=ft.colors.BLUE_800,
        text_align=ft.TextAlign.CENTER,  # Выравнивание по центру
    )

    # Кнопка для предсказания
    def find_language(e):
        user_input = text_input.value  # Получаем текст из поля ввода
        if not user_input:
            page.snack_bar = ft.SnackBar(ft.Text("Пожалуйста, введите текст задачи."))
            page.snack_bar.open = True
            page.update()
            return

        # Предсказываем язык программирования
        recommended_language = predict_language(user_input)

        # Выводим результат
        result_text.value = f"Рекомендуемый язык программирования: {recommended_language}"
        result_text.color = ft.colors.GREEN_800
        page.update()

    # Кнопка "Найти"
    find_button = ft.ElevatedButton(
        text="Найти",
        on_click=find_language,
        width=200,
        bgcolor=ft.colors.BLUE_800,
        color=ft.colors.WHITE,
    )

    # Поле для вывода результата
    result_text = ft.Text(
        size=20,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,  # Выравнивание по центру
    )

    # Блок для уточнения задачи
    refinement_title = ft.Text(
        "Уточнение задачи",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_800,
        text_align=ft.TextAlign.CENTER,  # Выравнивание по центру
    )

    # Поля для ввода весов критериев
    weight_inputs = {}
    for criterion in criteria:
        weight_inputs[criterion] = ft.Dropdown(
            label=f"Вес для '{criterion}'",
            width=300,
            options=[ft.dropdown.Option(str(i / 10)) for i in range(1, 10)],
            value="0.1",  # Значение по умолчанию
            border_color=ft.colors.BLUE_800,
            # Убираем text_align, так как он не поддерживается для Dropdown
        )

    # Кнопка для расчета дерева решений
    def calculate_tree(e):
        # Получаем веса критериев
        weights = {}
        for criterion, dropdown in weight_inputs.items():
            weights[criterion] = float(dropdown.value)

        # Нормализация весов
        total_weight = sum(weights.values())
        if total_weight != 1:
            for criterion in weights:
                weights[criterion] /= total_weight

        # Рассчитываем топ-3 языка с помощью дерева решений
        top_3_languages = choose_top_3_languages(weights, scores)
        if top_3_languages:
            tree_result_text.value = "\n".join([f"{lang}: {score:.2f}" for lang, score in top_3_languages])
        else:
            tree_result_text.value = "Нет подходящих языков."

        page.update()

    # Кнопка "Рассчитать дерево решений"
    tree_button = ft.ElevatedButton(
        text="Рассчитать дерево решений",
        on_click=calculate_tree,
        width=300,
        bgcolor=ft.colors.BLUE_800,
        color=ft.colors.WHITE,
    )

    # Поле для вывода результата дерева решений
    tree_result_text = ft.Text(
        size=16,
        weight=ft.FontWeight.NORMAL,
        color=ft.colors.BLUE_800,
        text_align=ft.TextAlign.CENTER,  # Выравнивание по центру
    )

    # Контейнер для элементов
    container = ft.Container(
        content=ft.Column(
            [
                title,
                text_input,
                find_button,
                result_text,
                refinement_title,
                *[weight_inputs[criterion] for criterion in criteria],  # Добавляем поля для ввода весов
                tree_button,
                ft.Text("Результат дерева решений:", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                tree_result_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Выравнивание по центру
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Выравнивание по центру
            spacing=20,
            scroll=ft.ScrollMode.AUTO,  # Включаем прокрутку внутри контейнера
        ),
        padding=30,
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.colors.BLUE_900,
            offset=ft.Offset(0, 0),
        ),
        alignment=ft.alignment.center,  # Выравнивание по центру
    )

    # Добавляем контейнер на страницу
    page.add(container)


# Запуск веб-приложения
ft.app(target=main, view=ft.WEB_BROWSER, port=8000)