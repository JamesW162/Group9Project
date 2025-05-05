#import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Specify the full relative path to the data.pickle file
data_pickle_path = r"data.pickle"
data_dict = pickle.load(open(data_pickle_path, 'rb'))

# The dataset has samples with 84 datapoints (2 hands, 42 per hand)
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

# Split the data into training and test sets.
x_train, x_test, y_train, y_test = train_test_split(
    data, labels, test_size=0.2, shuffle=True, stratify=labels
)

# Define model algorithm as a Random Forest Classifier. 
model = RandomForestClassifier()
model.fit(x_train, y_train)

# Test result against the initial dataset. Outputs success rate as a percentage.
y_predict = model.predict(x_test)
score = accuracy_score(y_predict, y_test)
print('{}% of samples were classified correctly'.format(score*100))

# Save the trained model.
with open('model.p', 'wb') as f:  
    pickle.dump({'model': model}, f)