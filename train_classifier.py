import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import numpy as np

# Specify the full absolute path to the data.pickle file
data_pickle_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.pickle')
data_dict = pickle.load(open(data_pickle_path, 'rb'))

# check that pickle works uncomment bellow
#print(data_dict.keys())
#print(data_dict)

data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

#we need 2 sets: a set to train the data and a set to test performance of our algorithm
# the test set showl be smaller than the test set and get viewed at the end
# shuffeling the data is a common practice when training a classifier to help aviod biases
# we are going to keep the same proportion of labels in test and training a common practice
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = RandomForestClassifier()

model.fit(x_train, y_train)

y_predict = model.predict(x_test)

score = accuracy_score(y_predict, y_test)

print('{}% of samples were classified correctly'.format(score*100))

with open('model.p', 'wb') as f:  # pickle is a Python library used to save datasets
    pickle.dump({'model':model}, f)