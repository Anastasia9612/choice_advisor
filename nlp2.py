import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import random
import joblib
import os
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    Doc,
)
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def create_word_cloud(text):
    # Создание облака слов
    wordcloud = WordCloud(
        width=800,  # Ширина изображения
        height=400,  # Высота изображения
        background_color='white',  # Цвет фона
        colormap='viridis',  # Цветовая схема
        max_words=50  # Максимальное количество слов
    ).generate(text)

    # Отображение облака слов
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Убираем оси
    plt.show()

# Функция для чтения датасета из файла
def load_dataset(file_path):
    dataset = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            text, language = line.strip().split('.')  # Разделяем строку по табуляции
            dataset.append((text, language))
    return dataset


# Загрузка необходимых ресурсов для NLTK
nltk.download('stopwords')

# Инициализация Natasha для обработки русского текста
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)


# Предобработка текста с использованием Natasha
def preprocess_text(text):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    # Лемматизация
    for token in doc.tokens:
        token.lemmatize(morph_vocab)

    # Удаление стоп-слов
    stop_words = set(stopwords.words('russian'))  # Загружаем стоп-слова для русского языка

    filtered_tokens = [
        token.lemma for token in doc.tokens
        if token.lemma.isalnum() and token.lemma not in stop_words
    ]

    return " ".join(filtered_tokens)



# Проверяем, существуют ли файлы модели и векторизатора
if os.path.exists('trained_model.pkl') and os.path.exists('tfidf_vectorizer.pkl'):
    print("Модель и векторизатор уже обучены и загружены.")
    model = joblib.load('trained_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
else:
    print("Обучение модели...")

    # Загрузка датасета из файла
    dataset = load_dataset('dataset.txt')

    # Перемешивание данных
    random.shuffle(dataset)

    # Разделение данных на тексты и языки
    texts = [item[0] for item in dataset]
    languages = [item[1] for item in dataset]

    #create_word_cloud(texts[0])

    # Применение предобработки ко всем текстам
    preprocessed_texts = [preprocess_text(text) for text in texts]

    #create_word_cloud(preprocessed_texts[0])


    # Преобразование текста в TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(preprocessed_texts)

    # Разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, languages, test_size=0.2, random_state=42)

    # Обучение модели
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Оценка точности модели
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Точность модели: {accuracy * 100:.2f}%")


    # Сохранение модели и векторизатора
    joblib.dump(model, 'trained_model.pkl')  # Сохраняем модель
    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')  # Сохраняем векторизатор


# Функция для предсказания языка по тексту задачи
def predict_language(text):
    preprocessed_text = preprocess_text(text)
    text_vector = vectorizer.transform([preprocessed_text])
    prediction = model.predict(text_vector)
    return prediction[0]

'''
user_input = input("Введите текст задачи (или 'выход' для завершения): ")
# Определяем язык программирования
recommended_language = predict_language(user_input)
print(f"Рекомендуемый язык программирования: {recommended_language}\n")
'''