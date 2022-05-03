**Diabetes prediction**

The objective of this assignment is to predict whether or not a female patient has diabetes, based on certain diagnostic measurements included in the dataset.

The datasets consists of several medical predictor variables and one target variable, Outcome. Predictor variables includes the number of pregnancies the patient has had, their BMI, insulin level, age, and so on.

Use the Scikit-learn Python library to build a decision tree (https://scikit-learn.org/stable/modules/tree.html), and train it using the dataset diabetes.csv. You should try to achieve as high accuracy as possible. Teachers obtained 74--75% accuracy and you can try to find better parameters. The accuracy depends on parameters of the classifier (https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier), the proportion of training and test data sizes etc. Make sure that your results are statistically significant so that your predicting system could be used in practice. Therefore, it is impractical to find the best random seed which only works for one selected test case.

Tasks: Your output should be a PDF file explaining the settings of your decision tree. A basic python code for a decision tree is already included. Edit this file and experiment with various settings. Find a combination of features and parameter settings that result in a good accuracy of your model. Discuss how the parameters influence the accuracy, i.e., which parameters affected the accuracy the most and which did not really change anything. Include a graph describing the dependency of accuracy and precision on the proportion of train and test set sizes. Finally, visualize the decision tree.

Upload both PDF and python source code to recodex. You will get 1 temporary point upon submission of two files (one syntactically correct PDF and one Python script) and proper points will be assigned later.
