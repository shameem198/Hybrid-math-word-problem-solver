from google.colab import drive
drive.mount('/content/gdrive/')

import warnings
warnings.filterwarnings("ignore")

import os
import pandas as pd
import numpy as np
import re
from numpy import array
from numpy import asarray
from numpy import zeros
from numpy import argmax
from keras.preprocessing.text import one_hot,Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import GRU,LSTM
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import RepeatVector, Bidirectional
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint
from keras.utils.vis_utils import plot_model
from keras.models import Model
from keras.models import load_model
from keras.optimizers import Adam
from keras import regularizers
from keras.callbacks import EarlyStopping





df_Train = pd.read_csv('/content/gdrive/My Drive/MathWPS/DATASETS/final_traindata.csv',engine='python', sep='\t')


questions = df_Train['Questions']
equations = df_Train['Equations']
Eqn_Template = df_Train['Equations_Template']




# fit a tokenizer
def create_tokenizer(lines):
    tokenizer = Tokenizer(filters='!"#$%&,:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=" ")
    tokenizer.fit_on_texts(lines)
    print(tokenizer.word_index)
    return tokenizer

# max sentence length
def max_length(lines):
    return max(len(line.split()) for line in lines)

#Question tokenizer train
Qstn_tokenizer = create_tokenizer(questions)
Qstn_vocab_size = len(Qstn_tokenizer.word_index) + 1
Qstn_length = max_length(questions)
print('Question Vocabulary Size: %d' % Qstn_vocab_size)
print('Question Max Length: %d' % (Qstn_length))

#Equation tokenizer
Eqn_tokenizer = create_tokenizer(Eqn_Template)
Eqn_vocab_size = len(Eqn_tokenizer.word_index) + 1
Eqn_length = max_length(Eqn_Template)
print('Equation Vocabulary Size: %d' % Eqn_vocab_size)
print('Equation Max Length: %d' % (Eqn_length))


# encode and pad sequences
def encode_sequences(tokenizer, length, lines):
    # integer encode sequences
    X = tokenizer.texts_to_sequences(lines)
    # pad sequences with 0 values
    X = pad_sequences(X, maxlen=length, padding='post')
    return X


# one hot encode target sequence
def encode_output(sequences, vocab_size):
    ylist = list()
    for sequence in sequences:
        encoded = to_categorical(sequence, num_classes=vocab_size)
        ylist.append(encoded)
    y = array(ylist)
    y = y.reshape(sequences.shape[0], sequences.shape[1], vocab_size)
    return y


# prepare training data
trainX = encode_sequences(Qstn_tokenizer, Qstn_length, questions)
trainY = encode_sequences(Eqn_tokenizer, Eqn_length, Eqn_Template)
trainY = encode_output(trainY, Eqn_vocab_size)



embeddings_index = {}
f = open(r'/content/gdrive/My Drive/MathWPS/Glove/glove.840B.300d.txt', encoding='utf8')
for line in f:
    values = line.split()
    word = ''.join(values[:-300])
    coefs = np.asarray(values[-300:], dtype='float32')
    embeddings_index[word] = coefs
f.close()
print('Loaded %s word vectors.' % len(embeddings_index))
# create a weight matrix for words in training docs
embedding_matrix = zeros((Qstn_vocab_size, 300))
for word, i in Qstn_tokenizer.word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector
        

# define RNN model
def define_model(src_vocab, tar_vocab, src_timesteps, tar_timesteps, n_units):
    model = Sequential()
    model.add(Embedding(src_vocab, n_units, weights=[embedding_matrix], input_length=src_timesteps, mask_zero=True))
    model.add(Bidirectional(LSTM(n_units, return_sequences=True)))  
    model.add(Dropout(0.5))
    model.add(Bidirectional(LSTM(n_units)))
    model.add(Dropout(0.5))
    model.add(RepeatVector(tar_timesteps))
    model.add(Bidirectional(LSTM(n_units, return_sequences=True)))
    model.add(Dropout(0.5))
    model.add(Bidirectional(LSTM(n_units, return_sequences=True)))
    model.add(Dropout(0.5))
    model.add(Dense(tar_vocab, activation='softmax'))
    return model

# define model
model = define_model(Qstn_vocab_size, Eqn_vocab_size, Qstn_length, Eqn_length, 300)
model.compile(optimizer=Adam(lr=0.0009), loss='categorical_crossentropy', metrics=['accuracy'])
# summarize defined model
print(model.summary())
plot_model(model, to_file='/content/gdrive/My Drive/MathWPS/SavedModels/modelseq2seq2.png', show_shapes=True)
# fit model
checkpoint_path = "/content/gdrive/My Drive/MathWPS/SavedModels/template_retrieval12.h5"
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = ModelCheckpoint(checkpoint_path, 
                              save_best_only=True,
                              monitor='loss',
                              verbose=1,
                              mode='min')

model.fit(trainX, trainY, epochs=350, batch_size=256, validation_split=0.005, verbose=1, callbacks = [cp_callback])

