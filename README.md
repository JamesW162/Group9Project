# SIGN LANGUAGE TRANSLATOR
At the current moment this is a ALS translator unfortunately it did not allow me to upload
the data set- git hub panicked because apparently "_100 files is too much_" so its up to you
to create the data for this model 

This project uses Mediapipe for hand detection and ML model to classify the gestures. 
The system then uses real -time video input from a camera to detect hand landmarks and predict
what letter the hand gesture relates to. 

## Installation 
to get started, clone this repository and install the dependancies 

`
git clone https://github.com/yourusername/hand-gesture-recognition.git

cd hand-gesture-recognition

pip install -r requirements.txt
`

## The order to run the programs in 
- initially start by running the `collect_imags.py`
    - at the moment it only creates a classe for 3 set of data AKA 3 Letters
    - `number_of_classes = 3`
    - you have to run the q 3 times
- from there run the `create_dataset.py`
    - this creates the `data.pickle` file that is needed to train the LLM model
- then run the `train_classifier.py`
    - this file creates the LLM model and trains it on the data set we have just created
    - within it it creates the `model.p` which is needed to run the classifier
- finally run the `inference_classifier.py`
    - at the moment it only has 3 letters which it relates to each class as seen bellow, if you add
      classes you need to edit this dictionary
    - `labels_dict = {0: 'A', 1: 'B', 2: 'L'}`
 
## Important to note
- the model **_panics_** if there is more than 1 hand and shuts down really messily
- I have yet to train it on the full alphabet so no clue if that works
- we need to figure out how to string the words into sentences
- This is ASL **not** BSL

## the video tutorial that was followed if further help is needed 

<iframe width="560" height="315" src="https://www.youtube.com/embed/MJCSjXepaAM" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


## Next Week 
can we connect this to the pi ASAP :)
