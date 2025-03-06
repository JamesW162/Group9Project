# SIGN LANGUAGE TRANSLATOR
At the current moment this is a BSL translator unfortunately it did not allow me to upload
the data set- GitHub panicked because apparently "_100 files is too much_" so its up to you
to create the data for this model 

This project uses Mediapipe for hand detection and ML model to classify the gestures. 
The system then uses real-time video input from a camera to detect hand landmarks and predict
what letter the hand gesture relates to. 
It is currently built using version 3.11.9 of Python.
For example:

![image](https://github.com/user-attachments/assets/f8b1654a-554f-4194-9add-d3a08eb3a8c6)




## Installation 
to get started, clone this repository and install the dependancies 

`git clone https://github.com/yourusername/Group9Project.git`

`cd Group9Project`

`pip install -r requirements.txt`

## The order to run the programs in 
- Initially start by running the **`collect_images.py`**
    - At the moment it only creates a class for 3 set of data AKA 3 Letters
    - `number_of_classes = 3`
	@@ -35,48 +33,23 @@ to get started, clone this repository and install the dependancies
    - Within it it creates the `model.p` which is needed to run the classifier
    - Also IMPORTANT change the `data_dict` line 9 to the path on your computer
- Finally run the **`inference_classifier.py`**
    - At the moment it only has 3 letters which it relates to each class as seen below, if you add classes you need to edit this dictionary
    - `labels_dict = {0: 'A', 1: 'B', 2: 'L'}`

## Important to note
- We need to figure out how to string the words into sentences
- We need to start figuring out how to 


## the video tutorial that was followed if further help is needed 

[![Watch the tutorial on YouTube](https://img.youtube.com/vi/MJCSjXepaAM/0.jpg)](https://www.youtube.com/watch?v=MJCSjXepaAM)

## BSL Letter Chart
![image](https://imgs.search.brave.com/DKomfn_cPKzVi7KigGeY5d0Jdn0WK72m8gxgMzOFH6M/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9hY2Nl/c3Nic2wuY29tL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDIyLzEx/LzIuYWNjZXNzYnNs/LUZpbmdlcnNwZWxs/aW5nLXJpZ2h0LWhh/bmQtMS5qcGc)

## Raspbery pi connection 
After further research the Raspberry Pi runs on version 3.7 and the Mediapipe library is not compatible with this this version. :)

SO... with this "fun" development we have 2 options:

#### 1. Factory reset the raspberry pi and see it we can update the whole pi
   https://www.geeksforgeeks.org/how-to-upgrade-raspberry-pi-os/

   we tried to update the version of python on the pi for several hours and even the lab techs came to the conclusion we can't with this version of pi we would need to update the whole pi so if one of the pis wants to try this extreme measure. 

#### 2. Do the proessing on the cloud and send it back.
As seen below the Raspberry Pi will collect the image data and feed it to ThingsBoard. This will then trigger an event and run a python script on something like "AWS Cloud based Lambda" - we have yet to figure out what service we will use. This will trigger the computer vision program. Finally we will then feed the data to both a front end website and back to the Raspbery Pi to output to audio. 
![image](https://github.com/user-attachments/assets/07492b59-955f-418c-858c-ce19d5b94ed3)

HOWEVER... both these thes options come with new risks.

Option 1 we just straight up dont know if it will work and we've already wasted ~5 hours on trying to update the version of python so this is a last resort so try it if you want. Option 2 is long and convoluted (No it isn't) and we're going to have to figure out how to encrypt the images on the web to maintain the security. 


## Output 
The auto correct exitst :)
yay!

## Next Week 
- We need to get the program and the Pi integrated together.
- We need to start outputting the letters as text/words. 
- We need to collect more data.
- Someone needs to start building the front end.
