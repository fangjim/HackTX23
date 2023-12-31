# -*- coding: utf-8 -*-
"""HackTX2023.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fCtmxGsM9eG6P9u0vAavweDX23jFW9cZ

#Imports
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import binary_crossentropy, categorical_crossentropy
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.utils import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import random
import torch
import torch.nn as nn

"""# Dataset Preprocessing"""

data = pd.read_csv("/content/HackTx Classification Data - Sheet1.csv")
df = data[["item", "exercise", "clothes", "electronics"]]
df.head(10)

data = data[:-1]
data = data[:-1]
data.tail(10)

class DataPreprocessing:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def str_cols(data):
        str_cols = []
        for col in data.columns:
            if isinstance(data[col][0], str):
                str_cols.append(col)
        return str_cols

    @staticmethod
    def lower_case(string):
        return string.lower()

    @staticmethod
    def letters_only(word):
        letters = set('abcdefghijklmnopqrstuvwxyz ')
        word = ''.join(char for char in word if char in letters)
        return word

    @staticmethod
    def space_offset(string):
        offset = 0
        for i in range(len(string)):
            if string[i] == ' ':
                offset += 1
            else:
                return offset
        return offset


    @staticmethod
    def remove_mult_spaces(s):
        spaces = False
        i = 0
        while i < len(s):
            if s[i] == ' ' and spaces:
                offset = DataPreprocessing.space_offset(s[i:])
                s = s[:i] + s[i+1+offset:]
            elif s[i] == ' ' and not spaces:
                spaces = True
            else:
                spaces = False
            i += 1
        return s


    def text_preprocess(self, col):
        for i, itemName in enumerate(self.data[col]):
            itemName = self.lower_case(itemName)
            itemName = self.letters_only(itemName)
            itemName = self.remove_mult_spaces(itemName)
            self.data.loc[i, col] = itemName
        return None

data_preprocessing = DataPreprocessing(data)
data_preprocessing.text_preprocess("item")

data

"""# Analysis"""

def popCount(col):
    popularity_dict = {}
    word_arr = []
    for item in col:
      words = item.split(' ')
      for word in words:
        if word not in popularity_dict:
          popularity_dict[word] = 1
          word_arr.append(word)
        else:
          popularity_dict[word] += 1
    return popularity_dict, word_arr


def popWords(word_dict, word_arr):
    wordPopArr = []
    for word in word_arr:
      wordPopArr.append([word, word_dict[word]])
    return wordPopArr



def sortPopWords(popWordArr):
    for i in range(len(popWordArr)):
      for j in range(i+1, len(popWordArr)):
        if popWordArr[i][-1] < popWordArr[j][-1]:
          popWordArr[i], popWordArr[j] = popWordArr[j], popWordArr[i]
    return popWordArr



def returnPopWords(data):
  word_dict, word_Arr = popCount(data["item"])
  popWordArr = popWords(word_dict, word_Arr)
  sortedPopWordArr = sortPopWords(popWordArr)
  return sortedPopWordArr

cols = data.columns
data_dicts = []

for i in range(1, len(cols)):
    filtered_data = data[data[cols[i]] == 1]
    data_dicts.append(returnPopWords(filtered_data))

print(data_dicts[5])

exercise_dict = {
    "exercise": True,
    "bands": True,
    "resistance": True,
    "workout": True,
    "fitness": True,
    "equipment": True,
    "gym": True,
    "bike": True,
    "yoga": True,
    "training": True,
    "mat": True,
    "adjustable": True,
    "exerciser": True,
    "physical": True,
    "pilates": True,
    "elliptical": True,
    "lbs": True,
    "stretching": True,
    "weight": True,
    "strength": True,
}

clothes_dict = {
    "mens": True,
    "womens": True,
    "sleeve": True,
    "long": True,
    "workout": True,
    "shirts": True,
    "tops": True,
    "pants": True,
    "causal": True,
    "fleece": True,
    "ribbed": True,
    "shirt": True,
    "yoga": True,
    "sweatshirt": True,
    "pullover": True,
    "women": True,
    "slim": True,
    "piece": True,
    "jacket": True,
    "button": True,
    "clothes": True,
    "fit": True,
    "zip": True,
    "shorts": True,
    "seamless": True,
    "jogger": True,
    "hoodie": True
}

electronics_dict = {
    "charger": True,
    "wireless": True,
    "iphone": True,
    "fast": True,
    "bluetooth": True,
    "apple": True,
    "display": True,
    "electronic": True,
    "headphones": True,
    "smart": True,
    "usb": True,
    "led": True,
    "battery": True,
    "electric": True,
    "airpods": True,
    "laser": True,
    "tv": True,
    "sound": True,
    "hd": True,
    "earphones": True,
    "tablet": True,
    "echo": True,
    "amazon": True
}

entertainment_dict = {
    "game": True,
    "tv": True,
    "stand": True,
    "games": True,
    "book": True,
    "board": True,
    "family": True,
    "entertainment": True,
    "center": True,
    "station": True,
    "control": True,
    "controller": True,
    "guide": True,
    "hardcover": True,
    "room": True,
    "cards": True,
    "playstation": True,
    "paperback": True,
    "adults": True,
    "disney": True,
    "kids": True,
    "media": True
}

diet_dict = {
    "protein": True,
    "pills": True,
    "fat": True,
    "loss": True,
    "diet": True,
    "weight": True,
    "supplement": True,
    "suppressant": True,
    "burner": True,
    "free": True,
    "pack": True,
    "keto": True,
    "powder": True,
    "appetite": True,
    "vegan": True,
    "energy": True,
    "drink": True,
    "blocker": True,
    "booster": True,
    "cider": True,
    "vinegar": True,
    "gluten": True,
    "caffeine": True
}

personalCare_dict = {
    "skin": True,
    "for": True,
    "eye": True,
    "face": True,
    "care": True,
    "mask": True,
    "under": True,
    "serum": True,
    "teeth": True,
    "collagen": True,
    "whitening": True,
    "patches": True,
    "skincare": True,
    "bikini": True,
    "body": True,
    "hair": True,
    "toothpaste": True,
    "acid": True,
    "set": True,
    "area": True,
    "dry": True,
    "razor": True,
    "facial": True,
    "exfoliator": True,
    "kit": True,
    "wrinkles": True,
    "scrub": True,
    "comb": True,
    "lines": True,
    "soft": True,
    "circles": True

}

title_arr = []

for item in data["item"]:
    input_arr = []
    words = item.split(" ")
    for word in words:
        if (word in exercise_dict) or (word in clothes_dict) or (word in electronics_dict) or (word in entertainment_dict) or (word in diet_dict) or (word in personalCare_dict):
            input_arr.append(word)
    title_arr.append(input_arr)

print(title_arr)

data["item"] = title_arr

import random
for _ in range(10):
  num = random.randint(0, 300)
  print(data.iloc[num]["item"])

"""#Data Split"""

exercise_dict = {
    "exercise": True,
    "bands": True,
    "resistance": True,
    "workout": True,
    "fitness": True,
    "equipment": True,
    "gym": True,
    "bike": True,
    "yoga": True,
    "training": True,
    "mat": True,
    "adjustable": True,
    "exerciser": True,
    "physical": True,
    "pilates": True,
    "elliptical": True,
    "lbs": True,
    "stretching": True,
    "weight": True,
    "strength": True,
}

clothes_dict = {
    "mens": True,
    "womens": True,
    "sleeve": True,
    "long": True,
    "workout": True,
    "shirts": True,
    "tops": True,
    "pants": True,
    "causal": True,
    "fleece": True,
    "ribbed": True,
    "shirt": True,
    "yoga": True,
    "sweatshirt": True,
    "pullover": True,
    "women": True,
    "slim": True,
    "piece": True,
    "jacket": True,
    "button": True,
    "clothes": True,
    "fit": True,
    "zip": True,
    "shorts": True,
    "seamless": True,
    "jogger": True,
    "hoodie": True
}

electronics_dict = {
    "charger": True,
    "wireless": True,
    "iphone": True,
    "fast": True,
    "bluetooth": True,
    "apple": True,
    "display": True,
    "electronic": True,
    "headphones": True,
    "smart": True,
    "usb": True,
    "led": True,
    "battery": True,
    "electric": True,
    "airpods": True,
    "laser": True,
    "tv": True,
    "sound": True,
    "hd": True,
    "earphones": True,
    "tablet": True,
    "echo": True,
    "amazon": True
}

entertainment_dict = {
    "game": True,
    "tv": True,
    "stand": True,
    "games": True,
    "book": True,
    "board": True,
    "family": True,
    "entertainment": True,
    "center": True,
    "station": True,
    "control": True,
    "controller": True,
    "guide": True,
    "hardcover": True,
    "room": True,
    "cards": True,
    "playstation": True,
    "paperback": True,
    "adults": True,
    "disney": True,
    "kids": True,
    "media": True
}

diet_dict = {
    "protein": True,
    "pills": True,
    "fat": True,
    "loss": True,
    "diet": True,
    "weight": True,
    "supplement": True,
    "suppressant": True,
    "burner": True,
    "free": True,
    "pack": True,
    "keto": True,
    "powder": True,
    "appetite": True,
    "vegan": True,
    "energy": True,
    "drink": True,
    "blocker": True,
    "booster": True,
    "cider": True,
    "vinegar": True,
    "gluten": True,
    "caffeine": True
}

personalCare_dict = {
    "skin": True,
    "for": True,
    "eye": True,
    "face": True,
    "care": True,
    "mask": True,
    "under": True,
    "serum": True,
    "teeth": True,
    "collagen": True,
    "whitening": True,
    "patches": True,
    "skincare": True,
    "bikini": True,
    "body": True,
    "hair": True,
    "toothpaste": True,
    "acid": True,
    "set": True,
    "area": True,
    "dry": True,
    "razor": True,
    "facial": True,
    "exfoliator": True,
    "kit": True,
    "wrinkles": True,
    "scrub": True,
    "comb": True,
    "lines": True,
    "soft": True,
    "circles": True

}


def assign(col):
  classifications = []
  for itemName in col:

    # Initialize col and counts
    exercise_count = 0
    clothes_count = 0
    electronics_count = 0
    entertainment_count = 0
    diet_count = 0
    personalCare_count = 0

    # iteratively increment counts
    for word in itemName:
      if word in exercise_dict:
        exercise_count += 1
      elif word in clothes_dict:
        clothes_count += 1
      elif word in electronics_dict:
        electronics_count
      elif word in entertainment_dict:
        entertainment_count += 1
      elif word in diet_dict:
        diet_count += 1
      else:
        personalCare_count += 1

    #

    lst = [[exercise_count, "exercise"], [clothes_count, "clothes"], [electronics_count, "electronics"], [entertainment_count, "entertainment"], [diet_count, "diet"], [personalCare_count, "personalCount"]]
    max, max_cat = 0, []
    for i in range(len(lst)):
      if lst[i][0] >= max:
        max = lst[i][0]
        max_cat.append(lst[i][-1])
    if max != 0:
      num = random.randint(0, (len(max_cat)-1))
      classification = max_cat[num]
      classifications.append(classification)
    else:
      classification = lst[random.randint(0, 5)][-1]
      classifications.append(classification)
  return classifications

assign(data["item"])

def data_split(data):
    data = data.sample(frac=1)
    features = data["item"].tolist()
    labels = []

    for i in range(len(data)):
        if data["exercise"][i] == 1.0:
            labels.append("exercise")
        elif data["clothes"][i] == 1.0:
            labels.append("clothes")
        elif data["electronics"][i] == 1.0:
            labels.append("electronics")
        elif data["personalCare"][i] == 1.0:
            labels.append("personalCare")
        elif data["entertainment"][i] == 1.0:
            labels.append("entertainment")
        else:
            labels.append("diet")

    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.4, random_state=42
    )

    return train_features, train_labels, test_features, test_labels

trainData, trainLabels, testData, testLabels = data_split(data)

def maxSeqLen(arr):
  max_len = 0
  for arr in title_arr:
    if len(arr) > max_len:
      max_len = len(arr)
  return max_len

def vocabSize(arr):
  occurArr = []
  for seq in arr:
    for word in seq:
      if word not in occurArr:
        occurArr.append(word)
  return len(occurArr)

max_seq_len = maxSeqLen(title_arr)
vocab_size = vocabSize(title_arr)
tokenizer = Tokenizer(num_words=vocab_size, oov_token='<OOV>')
label_encoder = LabelEncoder()

all_labels = trainLabels + testLabels
label_encoder.fit(all_labels)

train_labels_encoded = label_encoder.transform(trainLabels)
test_labels_encoded = label_encoder.transform(testLabels)

def model(data, labels):
    tokenizer.fit_on_texts(data)
    trainSeq = tokenizer.texts_to_sequences(data)
    trainPadded = pad_sequences(trainSeq, maxlen=max_seq_len, padding='post', truncating='post')
    train_data_padded = trainPadded

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=64, input_length=max_seq_len),
        tf.keras.layers.LSTM(units=64, return_sequences=False),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(6, activation='softmax')
    ])

    optimizer = tf.keras.optimizers.Adam(lr=0.0001)

    model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=['accuracy'])

    model.fit(train_data_padded, labels, epochs=300, validation_split=0.2, batch_size=32)

    return model

train_model = model(trainData, train_labels_encoded)

"""# Run on Test Data"""

test_sequences = tokenizer.texts_to_sequences(testData)
test_data_padded = pad_sequences(test_sequences, maxlen=max_seq_len, padding='post', truncating='post')


loss, accuracy = train_model.evaluate(test_data_padded, test_labels_encoded)

print("Model Accuracy:", accuracy)

"""# Regression Model"""

data.columns

"""### Data"""

customer_dict = {
    "exercise": [],
    "clothes": [],
    "diet": [],
    "entertainment": [],
    "electronics": [],
    "personalCare": [],
    "price": [],
    "score": [],
    }

for a in range(1, 6):
    for b in range(1, 6):
        for c in range(1, 6):
            for d in range(1, 6):
                for e in range(1, 6):
                    for f in range(1, 6):
                        for g in np.arange(4, 301, 0.5):
                            for h in range(3):
                                customer_dict["exercise"].append(a)
                                customer_dict["clothes"].append(b)
                                customer_dict["diet"].append(c)
                                customer_dict["entertainment"].append(d)
                                customer_dict["electronics"].append(e)
                                customer_dict["personalCare"].append(f)
                                customer_dict["price"].append(g)
                                customer_dict["score"].append(np.random.normal(5, 2))

customer_df = pd.DataFrame(customer_dict)

df = customer_df.sample(1000)

print(df.iloc[:-1].shape[1])

# Assuming df is your DataFrame with 999 samples and 8 features
X = df.iloc[:, :7].values
y = df.iloc[:, -1].values

X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32).reshape(-1, 1)  # Reshape y to have dimensions (999, 1)


n_samples, n_features = X.shape
input_size = n_features
output_size = 1  # Assuming you want to predict one value for each sample

# Rest of your code remains the same



# 2) Model, loss, and optimizer
model = nn.Linear(input_size, output_size)
learning_rate = 0.00001
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# 3) Training loop
num_epochs = 100
for epoch in range(num_epochs):
    # Forward pass and loss calculation
    y_pred = model(X)
    #print(y_pred)
    loss = criterion(y_pred, y)

    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch: {epoch + 1}, Loss: {loss.item():.4f}')

"""# Run on Test Data"""

input_data = [1, 5, 1, 4, 1, 3, 10.5]
input_data = torch.tensor(input_data, dtype=torch.float32)

# Put the model in evaluation mode
model.eval()

# Make predictions
with torch.no_grad():
    predictions = model(input_data)
    predictions += 5

print(predictions)