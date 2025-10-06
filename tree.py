# Определяем универсальное множество языков программирования
languages = ["Python", "C++", "C#", "JavaScript", "Java", "MATLAB", "R", "PHP"]

# Определяем критерии
criteria = [
    "Производительность",
    "Кроссплатформенность",
    "Наличие библиотек",
    "Поддержка веб-технологий",
    "Простота",
    "Строгая типизация",
    "Асинхронность",
    "Работа с базами данных",
    "Графический интерфейс",
    "Математические вычисления",
    "Автоматическое тестирование"
]

# Оценки языков по критериям (от 1 до 9)
scores = {
    "Python": [3, 9, 9, 8, 9, 2, 8, 8, 7, 8, 9],
    "C++": [9, 7, 6, 2, 4, 9, 3, 4, 5, 8, 5],
    "C#": [8, 7, 8, 7, 7, 9, 6, 8, 8, 6, 8],
    "JavaScript": [5, 9, 8, 9, 8, 3, 9, 6, 7, 5, 7],
    "Java": [7, 8, 8, 7, 6, 9, 6, 7, 7, 6, 8],
    "MATLAB": [6, 5, 7, 3, 5, 4, 3, 4, 6, 9, 6],
    "R": [5, 6, 7, 4, 6, 6, 5, 5, 5, 9, 6],
    "PHP": [4, 7, 7, 9, 7, 3, 5, 8, 5, 4, 6]
}

# Функция для фильтрации языков по критерию
def filter_languages(languages, criterion, weight, scores):
    if weight > 0.45:  # Если вес критерия высокий, фильтруем
        # Оставляем только языки с оценкой >= 7 по этому критерию
        return [lang for lang in languages if scores[lang][criteria.index(criterion)] >= 7]
    return languages  # Иначе не фильтруем

# Функция для расчета полезности каждого языка
def calculate_utility(languages, weights, scores):
    utility = {}
    for lang in languages:
        total = 0
        for i, criterion in enumerate(criteria):
            total += scores[lang][i] * weights[criterion]
        utility[lang] = total
    return utility

# Функция для выбора трех лучших языков
def choose_top_3_languages(weights, scores):
    # Начинаем с полного списка языков
    filtered_languages = list(languages)
    
    # Фильтруем языки по каждому критерию (дерево решений)
    for criterion, weight in weights.items():
        filtered_languages = filter_languages(filtered_languages, criterion, weight, scores)
        if not filtered_languages:
            return []  # Если языков не осталось, возвращаем пустой список
    
    # Рассчитываем полезность для оставшихся языков
    utility = calculate_utility(filtered_languages, weights, scores)
    
    # Сортируем языки по полезности в порядке убывания
    sorted_languages = sorted(utility.items(), key=lambda x: x[1], reverse=True)
    
    # Возвращаем топ-3
    return sorted_languages[:3]
