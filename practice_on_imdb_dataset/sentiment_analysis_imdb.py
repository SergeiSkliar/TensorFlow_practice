# -*- coding: utf-8 -*-
"""sentiment_analysis_imdb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ugggKg3sU40bFXk-0yiaqDqia51kmlCj
"""

import tensorflow as tf
from tensorflow.keras import datasets, layers, models, preprocessing
import tensorflow_datasets as tfds

max_len = 200
n_words = 10000
dim_embeddings = 256
EPOCHS = 20
BATCH_SIZE = 500

def load_data():
  #load data
  (X_train, y_train), (X_test, y_test) = datasets.imdb.load_data(num_words = n_words)
  #pad sequences with max_len
  X_train = preprocessing.sequence.pad_sequences(X_train, maxlen = max_len)
  X_test = preprocessing.sequence.pad_sequences(X_test, maxlen = max_len)
  return (X_train, y_train), (X_test, y_test)

def build_model():
  model = models.Sequential()
  #Input: embedding layer
  #- an integer matrix of size (batch, input_length).
  #Output:
  #- dimension (input_length, dim_embedding).
  #The largest integer in the input should be no larger than n_words (vocabulary size).
  model.add(layers.Embedding(n_words, dim_embeddings, input_length = max_len))
  #Takes the maximum value of either feature vector from each of the n_words features.
  model.add(layers.GlobalMaxPooling1D())
  model.add(layers.Dense(128, activation = 'relu'))
  model.add(layers.Dropout(0.5))
  model.add(layers.Dense(1, activation = 'sigmoid'))

  return model

(X_train, y_train), (X_test, y_test) = load_data()
model = build_model()
model.summary()

model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

score = model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(X_test, y_test))

score = model.evaluate(X_test, y_test, batch_size=BATCH_SIZE)
print("\nTest score: ", score[0])
print("Test accuracy: ", score[1])