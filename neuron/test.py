import pandas as pd
import re
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from nltk.corpus import stopwords, wordnet
from transformers import BertTokenizer, BertModel
import torch
import torch.nn as nn
import torch.optim as optim
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
import nltk
from deep_translator import GoogleTranslator  # новая библиотека для перевода

# Загрузка данных
data = pd.read_csv("data/data_training/dataset_.csv", encoding='ISO-8859-1', sep=';')
data.rename(columns={'¹': '№'}, inplace=True)

# Фильтрация редких классов (оставляем только те, где примеров >= 5)
label_counts = data['label'].value_counts()
data = data[data['label'].isin(label_counts[label_counts >= 5].index)]

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
    if not text:
        return np.zeros(model.config.hidden_size)
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

# Функции для аугментации текста
def synonym_replacement(text):
    words = text.split()
    new_words = words.copy()
    for i, word in enumerate(words):
        synonyms = wordnet.synsets(word)
        if synonyms:
            synonym = random.choice(synonyms).lemmas()[0].name()
            new_words[i] = synonym
    return ' '.join(new_words)

def shuffle_words(text):
    words = text.split()
    random.shuffle(words)
    return ' '.join(words)

def random_deletion(text, p=0.3):
    words = text.split()
    if len(words) == 1:
        return text
    new_words = [word for word in words if random.uniform(0, 1) > p]
    return ' '.join(new_words) if new_words else words[0]

# Функция для перевода текста на другой язык и обратно
translator = GoogleTranslator(source='en', target='fr')

def translate_back_and_forth(text, lang='fr'):
    try:
        translated = translator.translate(text)
        back_translated = GoogleTranslator(source=lang, target='en').translate(translated)
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        back_translated = text  # Если перевод не удался, используем исходный текст
    return back_translated

# Применение аугментации к обучающим данным
X_train_augmented = pd.concat([
    X_train.apply(synonym_replacement),
    X_train.apply(shuffle_words),
    X_train.apply(random_deletion),
    X_train.apply(translate_back_and_forth)
], axis=0)

# Преобразование аугментированных данных в BERT-эмбеддинги
X_train_augmented_bert = np.array([bert_text_to_vector(text, tokenizer, model) for text in X_train_augmented])
# Объединение синтетических данных с основными и аугментированными
X_train_combined = np.vstack((X_train_res, X_train_augmented_bert))
y_train_combined = np.concatenate((y_train_res, y_train_res[:X_train_augmented_bert.shape[0]]))

# Определение нейронной сети
class SimpleNN(nn.Module):
    def __init__(self, input_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 256)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, output_size)
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return x

# Настройки нейронной сети
input_size = X_train_combined.shape[1]
output_size = len(np.unique(y_train_combined))
model_nn = SimpleNN(input_size, output_size)

# Оптимизатор и функция потерь
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model_nn.parameters(), lr=0.001)

# Обучение модели
epochs = 10  # Уменьшите количество эпох для быстрой проверки
batch_size = 32
X_train_tensor = torch.tensor(X_train_combined, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train_combined, dtype=torch.long)

for epoch in range(epochs):
    model_nn.train()
    permutation = torch.randperm(X_train_tensor.size()[0])
    epoch_loss = 0
    for i in range(0, X_train_tensor.size()[0], batch_size):
        indices = permutation[i:i + batch_size]
        batch_x, batch_y = X_train_tensor[indices], y_train_tensor[indices]
        optimizer.zero_grad()
        outputs = model_nn(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    print(f'Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss / (i+1):.4f}')

# Оценка модели
model_nn.eval()
X_test_tensor = torch.tensor(X_test_bert, dtype=torch.float32)
with torch.no_grad():
    outputs = model_nn(X_test_tensor)
    _, y_pred = torch.max(outputs, 1)

# Обратное преобразование меток
y_pred_labels = le.inverse_transform(y_pred.numpy())
print("Отчет классификации:")
print(classification_report(y_test, y_pred_labels, zero_division=1))
print("Точность:", accuracy_score(y_test, y_pred_labels))