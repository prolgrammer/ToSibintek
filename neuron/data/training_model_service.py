
# Импорт необходимых библиотек
import pandas as pd
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from nltk.corpus import stopwords, wordnet
from transformers import BertTokenizer, BertModel
import torch
from collections import Counter
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import random
import nltk

# Загрузка данных
data = pd.read_csv("data/dataset_.csv", encoding='ISO-8859-1', sep=';')
data.rename(columns={'¹': '№'}, inplace=True)

# Предобработка текста
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

data['Topic_clean'] = data['Topic'].apply(preprocess_text)

# Разделение данных на обучающую и тестовую выборки
X = data['Topic_clean']
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Загрузка предобученной модели BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# Функция для генерации BERT-эмбеддингов
def bert_text_to_vector(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# Генерация эмбеддингов для обучающей и тестовой выборок
X_train_bert = np.array([bert_text_to_vector(text, tokenizer, model) for text in X_train])
X_test_bert = np.array([bert_text_to_vector(text, tokenizer, model) for text in X_test])

# Балансировка классов с помощью SMOTE на эмбеддингах BERT
le = LabelEncoder()
y_encoded = le.fit_transform(y_train)
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train_bert, y_encoded)

# Аугментация данных с помощью замены синонимов
def synonym_replacement(text):
    words = text.split()
    new_words = words.copy()
    for i, word in enumerate(words):
        synonyms = wordnet.synsets(word)
        if synonyms:
            synonym = random.choice(synonyms).lemmas()[0].name()
            new_words[i] = synonym
    return ' '.join(new_words)

# Применение аугментации
X_train_augmented = X_train.apply(synonym_replacement)
X_train_bert_augmented = np.array([bert_text_to_vector(text, tokenizer, model) for text in X_train_augmented])

# Объединение синтетических данных с основными и контроль за размерами
X_train_combined = np.vstack((X_train_res, X_train_bert_augmented))
y_train_combined = np.concatenate((y_train_res, y_train_res[:X_train_bert_augmented.shape[0]]))

# Проверка на соответствие размеров после аугментации
assert X_train_combined.shape[0] == y_train_combined.shape[0], "Размеры X_train и y_train не совпадают!"

# Обучение логистической регрессии на эмбеддингах BERT
classifier = LogisticRegression(max_iter=1000, random_state=42)
classifier.fit(X_train_combined, y_train_combined)

# Прогнозирование и отчет
y_pred = classifier.predict(X_test_bert)
y_pred_labels = le.inverse_transform(y_pred)
print("Отчет классификации:")
print(classification_report(y_test, y_pred_labels, zero_division=1))

# Функция для получения топ-N сервисов для нового текста
def get_top_predictions(text, model, classifier, top_n=3):
    text_vector = bert_text_to_vector(text, tokenizer, model)
    probas = classifier.predict_proba([text_vector])[0]
    top_indices = probas.argsort()[-top_n:][::-1]
    top_classes = le.inverse_transform(top_indices)
    return [(top_classes[i], probas[i]) for i in range(top_n)]
# Пример использования
text = "Forget my password"
top_services = get_top_predictions(text, model, classifier)
print("Топ предполагаемых сервисов для обращения:", top_services)