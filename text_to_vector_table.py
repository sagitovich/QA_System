from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Word2Vec
from hashlib import sha256
import pandas as pd


def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data


def preprocess_text(txt):
    # Разбиваем текст на предложения
    sentences_ = sent_tokenize(txt)
    # Разбиваем каждое предложение на слова
    sentences_ = [word_tokenize(sentence) for sentence in sentences_]
    return sentences_


def hash_sentence(sentence):
    return sha256(' '.join(sentence).encode()).hexdigest()


def vectorize_sentences_and_store(sentences_):
    # Векторизация предложений и сохранение в словаре
    vectorized_sentences = {hash_sentence(sentence):
        pd.Series(sum(model.wv[word] for word in sentence if word in model.wv)) for sentence in sentences_}
    return vectorized_sentences


path = '/Users/a.sagitovich/programming/noneBFU/QA_System/input/sigarets.txt'
text = read_file(path)

# Предобработка текста
sentences = preprocess_text(text)

# Обучение модели Word2Vec
model = Word2Vec(sentences, min_count=1)

result = vectorize_sentences_and_store(sentences)

data_frame = pd.concat(result, axis=1).T
data_frame.columns = [f'vector_{i}' for i in range(data_frame.shape[1])]

data_frame.to_csv('vec_table.csv', index_label='hash')
