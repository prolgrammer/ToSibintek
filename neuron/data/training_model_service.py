import pandas as pd
import re
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Подгружаем необходимые ресурсы для лемматизации
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# 1. Загрузка и обработка данных
data = pd.read_csv("data_training/dataset_.csv", encoding='ISO-8859-1', sep=';')
# data.rename(columns={'¹': '№'}, inplace=True)

# 2. Функция предобработки текста
def preprocess_text(text):
    text = text.lower()                              # Приведение текста к нижнему регистру
    text = re.sub(r'[^\w\s]', '', text)              # Удаление знаков препинания
    tokens = text.split()                            # Разделение на слова
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)                          # Сборка текста обратно

data['Topic_clean'] = data['Topic'].apply(preprocess_text)  # Применение предобработки

# 3. Определение признаков и меток
X = data['Topic_clean']
y = data['label']

# 4. Разделение данных на тренировочную и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Преобразование текста в TF-IDF векторы с учетом триграмм
vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=10000, min_df=2, max_df=0.95)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 6. Определение модели логистической регрессии с GridSearchCV
param_grid = {'C': [0.01, 0.1, 1, 10, 100]}
grid_search = GridSearchCV(LogisticRegression(class_weight='balanced', max_iter=500),
                           param_grid, cv=5, scoring='f1_weighted')
grid_search.fit(X_train_tfidf, y_train)

# 7. Лучшая модель
best_model = grid_search.best_estimator_

# 8. Оценка качества модели на тестовой выборке
y_pred = best_model.predict(X_test_tfidf)
y_prob = best_model.predict_proba(X_test_tfidf)  # Прогнозирование вероятностей для всех классов

# Вывод отчета о качестве модели
print("Отчет классификации по классам:")
print(classification_report(y_test, y_pred, zero_division=1))

# Пример для вероятностей классов: вывод наилучших вероятных сервисов в спорных случаях
def get_top_predictions(text, model, vectorizer, top_n=3):
    """Получает top_n наиболее вероятных сервисов для нового текста"""
    text_tfidf = vectorizer.transform([text])
    probas = model.predict_proba(text_tfidf)[0]
    classes = model.classes_
    top_indices = probas.argsort()[-top_n:][::-1]  # Находим топ-n вероятностей
    return [(classes[i], probas[i]) for i in top_indices]

# Пример использования функции для нового обращения
text = "Проблема с подключением к сети"
top_services = get_top_predictions(text, best_model, vectorizer)
print("Топ предполагаемых сервисов для обращения:", top_services)