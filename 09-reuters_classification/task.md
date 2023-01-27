## Setting

In this exercise, we are building a neural network that can categorize short business news messages called newswires. The dataset is a set of newswires published by Reuters in 1986. There are 46 categories (topics) into which each newswire can be placed. Some topics are more often represented than others but each is represented at least 10 times. The newswire itself is encoded as a list of integers, each integer representing a specific word. The correct categories are represented simply as an integer in the range [1, 46]. The dataset provides in total 8982 training examples and 2246 test examples.

## Provided code

You are provided with a simple script that modifies the input data, creates and trains a neural network, and shows the data collected during training.

The input data is transformed in such a way that only the 10000 most often used words are present. The input for the network is a vector of length 10000 with 1s in places of words that are used in the newswire. This transformation throws away the knowledge of the order of the words in the newswire and focuses only on whether or not the word is present. The output is a vector of length 46 with 1 in the place of the correct category.

The provided network has an input of 10000, 2 hidden dense layers each with 64 neurons, and one dense output layer of size 46. The activation function for the hidden layers is relu (rectified linear unit), and the activation function for the output layer is softmax across 46 outputs (returns 46 probabilities summing up to 1). The optimizer used is rmsprop (Root Mean Squared Propagation) and the loss function is categorical_crossentropy. Furthermore, the model will monitor accuracy (specified in "metrics") which will be stored in the training history.

For the training of the network, we used 1000 samples as a validation set, the rest is used as a training set. The training is performed over 20 epochs (epoch = iteration over all samples in the training data) in batches of 512 samples.

We print graphs of the loss function (difference between the expected outcome and the produced outcome) and the accuracy (fraction of predictions the model got right) for both the training set and the validation set based on the number of epochs performed. Note that the loss is always decreasing for the training set, but for the validation set, it is not the case. Similarly, the accuracy always increases for the training set but not for the validation set. 

## Your task

During the preparation of the data and creation of the network, we made many decisions. Your task is to try to change the setting of the network and write a report on the things you tried. In every part where you modify the network discuss if the performance of the network improved or not.

1. So far, we only used the training set. Implement a function that takes the trained network and categorizes the testing set. Recall the meaning of the output of the network. Are the results on the testing set more comparable to the training set or the validation set? [2 points]
2. Change the number of neurons in the hidden layers. You may try to both increase and decrease the number. What happens if you use significantly fewer neurons than the output size? [2 points]
3. Change the number of hidden layers. You may try to both increase and decrease the number. [2 points]
4. We showed that the accuracy and loss behave differently for the training and validation sets. Why is that? What does it tell you about the number of epochs? Try to use a different number of epochs. [2 points]
5. Combining the previous parts, describe a model of a network that performed the best. [2 points] 

### Presentation of your results

Important part of the report is to represent your results in a meaningful way. The suggested way is to use the function from task 1. and report the accuracy of the network on testing data as a function of the parameter you changed (number of layers, number of neurons, etc.). You can plot this function as a graph or show the numbers in a table. Remember to discuss the trend and try to provide a reasoning for what you observed.

## Resources

For the dataset and the neural network, we used Keras which runs on top of TensorFlow. You will need to install both TensorFlow version '2.8.0' and Keras version '2.8.0'. You can read up on all of the features provided by Keras on the [webpage](https://keras.io/) of the project.

For the graphs, we used matplotlib.
