import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier


# !kaggle competitions download titanic
train_data = pd.read_csv("data/train.csv")
test_data = pd.read_csv("data/test.csv")


def add_age(cols):
    age, pclass = cols
    if pd.isnull(age):
        if pclass == 1:
            return train_data[train_data['Pclass'] == 1]['Age'].median()
        elif pclass == 2:
            return train_data[train_data['Pclass'] == 2]['Age'].median()
        elif pclass == 3:
            return train_data[train_data['Pclass'] == 3]['Age'].median()
    else:
        return age


def clean_data(df):
    # clean data
    df['Age'] = df[['Age', 'Pclass']].apply(add_age, axis=1)
    df.Sex = df.Sex.map({'female': 0, 'male': 1})
    df.Embarked = df.Embarked.map({'S': 0, 'C': 1, 'Q': 2, 'nan': 'NaN'})
    df.drop('Cabin', axis=1, inplace=True)
    df.dropna(inplace=True)
    df.drop(['Name', 'PassengerId', 'Ticket'], axis=1, inplace=True)


# Logistic Regression approach
# clean_data(train_data)
# x_data = train_data.drop('Survived', axis=1)
# y_data = train_data['Survived']
# x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(x_data, y_data, test_size=0.2,
#                                                                               random_state=0, stratify=y_data)
# model = LogisticRegression()
# model.fit(x_training_data, y_training_data)

# Random Forest approach
y = train_data["Survived"]
features = ["Pclass", "Sex", "SibSp", "Parch"]
X = pd.get_dummies(train_data[features])
x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(X, y, test_size=0.2,
                                                                              random_state=0, stratify=y)
model = RandomForestClassifier(n_estimators=300, max_depth=8, random_state=1)
model.fit(X, y)

predictions = model.predict(x_test_data)
print(classification_report(y_test_data, predictions))
print("Accuracy : ", accuracy_score(y_test_data, predictions))


# let's apply this to the test data and submit it
X_test = pd.get_dummies(test_data[features])
predictions = model.predict(X_test)
print(predictions)
# predictions.to_csv("submission_random_forest.csv")

output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
output.to_csv('submission_random_forest.csv', index=False)


# kaggle competitions submit -c titanic -f submission_random_forest.csv -m "random forest try"

# so Random Forest performed worse on our test dataset but better on Kaggle test_data, meaning
# our dataset did not correlate well, there should be a way to get a test set that correlates well (TODO)
