# Gesture Classifier Training Script - Code Explanation

This document explains the functionality of `train_classifier.py`, which trains a machine learning model to recognize hand gestures using the previously created dataset, with direct quotes from the code.

## Imports and Setup

The script begins by importing the necessary libraries:

```python
#import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
```

- `pickle` is used for loading the dataset and saving the trained model
- `RandomForestClassifier` from scikit-learn is the machine learning algorithm used
- `train_test_split` helps divide the data into training and testing sets
- `accuracy_score` is used to evaluate the model's performance
- `numpy` provides functions for numerical operations on arrays

## Loading the Dataset

The script loads the previously generated dataset:

```python
# Specify the full relative path to the data.pickle file
data_pickle_path = r"data.pickle"
data_dict = pickle.load(open(data_pickle_path, 'rb'))

# The dataset has samples with 84 datapoints (2 hands, 42 per hand)
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])
```

This code:
1. Specifies the path to the pickle file containing the dataset
2. Loads the dictionary from the pickle file
3. Converts the data and labels from the dictionary into NumPy arrays
4. Notes that each sample has 84 datapoints (21 landmarks × 2 coordinates × 2 hands)

## Splitting the Dataset

The script divides the dataset into training and testing sets:

```python
# Split the data into training and test sets.
x_train, x_test, y_train, y_test = train_test_split(
    data, labels, test_size=0.2, shuffle=True, stratify=labels
)
```

This section:
1. Uses `train_test_split` to divide the data
2. Allocates 80% of the data for training (`test_size=0.2` means 20% for testing)
3. Shuffles the data for randomization
4. Uses stratification to ensure proportional representation of each class in both sets

## Training the Model

The script creates and trains a Random Forest Classifier:

```python
# Define model algorithm as a Ran
