import pandas
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

column_names = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age', 'label']
feature_columns = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age']
df = pandas.read_csv("diabetes.csv")
df.columns = column_names

X = df[feature_columns]
y = df.label

X_train, X_test, y_train, y_test = train_test_split(X, y)

dec_tree = DecisionTreeClassifier()
dec_tree= dec_tree.fit(X_train, y_train)

y_pred = dec_tree.predict(X_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Precision:", metrics.precision_score(y_test, y_pred))
print("Recall:", metrics.recall_score(y_test, y_pred))
