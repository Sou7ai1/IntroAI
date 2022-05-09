import keras
from keras.datasets import reuters
from keras import models
from keras import layers
from keras.utils.np_utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt

def create_testing_data():
    """
    Data = a newswire represented as a sequence of integers (representing words) 
    Labels = one of 46 categories the newswire talks about
    Consider only the 10000 most often used words, vectorization produces a vector of length 10000, index i = 1 if word i is in the newswire
    One hot labels is a vector of length 46 with 1 at the position of the correct category
    """
    (train_data, train_labels), (test_data, test_labels) = reuters.load_data(num_words=10000)

    train = vectorize_sequences(train_data)
    test = vectorize_sequences(test_data)
    one_hot_train_labels = to_categorical(train_labels)
    one_hot_test_labels = to_categorical(test_labels)

    # For fun, we can decode the input data to see what a newswire looks like
    #decode_input_data(train_data)

    return (train, one_hot_train_labels, test, one_hot_test_labels)

def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results

def decode_input_data(train_data):
    word_index = reuters.get_word_index()
    reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
    # Note that our indices were offset by 3
    # because 0, 1 and 2 are reserved indices for "padding", "start of sequence", and "unknown".
    decoded_newswire = ' '.join([reverse_word_index.get(i - 3, '?') for i in train_data[0]])
    print(decoded_newswire)



def create_and_train_network(input):
    """
    Create a network with the input of size 10000, two hidden layers, and one output layer of size 46
    The output of the network is a vector of probabilities the newswire falls into the specific category
    Set aside 1000 samples for validation, use the rest for training
    """
    (train,train_labels,_,_) = input

    # specify the shape of the network
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu', input_shape=(10000,)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(46, activation='softmax'))

    model.compile(optimizer='rmsprop',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    # split input data into training set and validation set
    val_data = train[:1000]
    train_data = train[1000:]

    val_labels = train_labels[:1000]
    train_labels = train_labels[1000:]

    # train the network
    history = model.fit(train_data,
                        train_labels,
                        epochs=20,
                        batch_size=512,
                        validation_data=(val_data, val_labels))
    
    return (history,model)



def print_graphs(history):
    """
    History contains data about the training process. It contains an entry for each metric used for both training and validation.
    Specifically, we plot loss = difference between the expected outcome and the produced outcome
    and accuracy = fraction of predictions the model got right
    """
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(loss) + 1)

    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()

    plt.clf()   # clear figure

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()



if __name__ == "__main__":
    # prepare data
    input = create_testing_data()

    # create and train the neural network
    (history,model) = create_and_train_network(input)

    # show the results
    print_graphs(history)
