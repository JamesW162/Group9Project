https://users.cs.cf.ac.uk/DaviesWR1/

# SIGN LANGUAGE TRANSLATOR
![image](https://github.com/JamesW162/Group9Project/blob/main/logo.png)

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
to get started, clone this repository, set up a virtual environment and install the dependancies 

### instilation on a laptop/pc
```
git clone https://github.com/JamesW162/Group9Project
cd Group9Project
```
open VS code in the Group9Project and now on run the commands in the terminals
```
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
cd project
cd server
npm install
npm install firebase
npm install express body-parser cors
```
you then need to add  `bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json` from firebase

Steps to Download Your Firebase Admin SDK JSON File
- Go to Firebase Console: Visit Firebase Console and log in.
- Select Your Project: Click on the project associated with bsltranslator-93f00.
- Open Project Settings:
- Click on the ⚙️ gear icon in the left sidebar.
- Choose Project settings.
- Navigate to Service Accounts:
- In the Project settings, select the Service accounts tab.
- Scroll down and find Firebase Admin SDK.
- Generate a New Private Key:
- Click Generate new private key.
- This will download a JSON file (firebase-adminsdk-xxxxx.json).

Important Notes
- Handle with care! This file contains sensitive credentials. Do not expose it publicly.
- Use in your backend: Place it in a secure location where only authorized applications can access it.
- **MAKE SURE** to save it as `bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json`
- **MAKE SURE** IT IS SAVED IN `Group9Project/project/server`

to then make sure everything is installed run

```
python fix.py
```

if there are any missing dependancies type `y` to fix them open cv sometimes plays around so sometimes you need to run `pip install opencv-python`

then to start running the server run
```
node server.js
```

### instilation on the pi
The `only` files you need from the repository are 




**NOTE PLEASE PUT THE `index.html` AND `logo.png` INTO A FOLDER CALLED `templates` my computer wouldnt let me upload the file for a wierd reason.**

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

How the code currently connects to the raspberry pi is found in the file `live_stream_pi_code.py` that can be found in the `raspberryPi` folder is through Firebase, a Google backends-as-a-service platform. Data is sent to the firelbase Realtime database and firestore with this configuration.

```
FRAME_RATE = 3  # Lower frames per second to avoid database overload
DO NOT GO OVER 5 frame rate we do not have the storage and any frame rate
higher has no notable difference.

RESOLUTION = (320, 240)  # Lower resolution for better performance with database

QUALITY = 20  # JPEG compression quality (lower = smaller file size)

MAX_STREAM_TIME = 300  # Maximum streaming time in seconds (5 minutes)

STREAM_ID = datetime.now().strftime("%Y%m%d_%H%M%S")  # Unique ID for this stream
```


the data is then stored within the realtime database
![image](https://github.com/user-attachments/assets/f8e41ac4-51ef-4f1f-825d-01f8e867b1da)

After that data gets fetched from the FireBase inside the `LiveStreamFromPi.html` it fetches the `streamId, connectBtn, refreshBtn, videoFrame, noStreamMessage, streamStatus, resolution, frameRate, startTime, frameCount, lastUpdate` and uses that data to dynamically load the live stream. This script also includes error handeling methods to improve user experience.

It is important to note the frame rate is awfully slow and we have restricted it to 5 mins of streaming as we are on the free version of firebase and we dont want to start costing ourselves money 

### The cloud process 
This diagram shows how the camera data flows from the Raspberry Pi to the Firebase. From there the data is sent to a PC/Laptop where the data is locally processed and the model translation  the BSL to text. From there the data has 2 routes:

Processed data sent to the Universities Cloud Webserver which serves as the backend for a website and mobile interface
2.   The processed data is returned to Things board which is used for output on the raspberry pi’s speaker.
![image](https://github.com/user-attachments/assets/803f0839-40de-431e-8479-3a3a09b21124)


### Learning Process That Failed
After further research the Raspberry Pi runs on version 3.7 and the Mediapipe library is not compatible with this this version. :)

SO... with this "fun" development we tried 2 options:
1. Factory reset the raspberry pi and see it we can update the whole pi
   https://www.geeksforgeeks.org/how-to-upgrade-raspberry-pi-os/
   we tried to update the version of python on the pi for several hours and even the lab techs came to the conclusion we can't with this version of pi we would need to update the whole pi so if one of the pis wants to try this extreme measure.

   
3. Do the proessing on the cloud and send it back.
As seen below the Raspberry Pi will collect the image data and feed it to ThingsBoard. This will then trigger an event and run a python script on something like "AWS Cloud based Lambda" - we have yet to figure out what service we will use. This will trigger the computer vision program. Finally we will then feed the data to both a front end website and back to the Raspbery Pi to output to audio. 
![image](https://github.com/user-attachments/assets/07492b59-955f-418c-858c-ce19d5b94ed3)

what the working webpage looks like now
![image](https://github.com/user-attachments/assets/9ce45291-fea6-4419-8a29-9f95c9cedc46)

server layoout that i could not implement cause my git is screwed

![image](https://github.com/user-attachments/assets/54ef874d-4d4b-492b-90f5-ad7d237ea908)

`npm install

npm install firebase

npm install express body-parser cors

node server.js` 

also need to add the bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json from firebase
Steps to Download Your Firebase Admin SDK JSON File
- Go to Firebase Console: Visit Firebase Console and log in.
- Select Your Project: Click on the project associated with bsltranslator-93f00.
- Open Project Settings:
- Click on the ⚙️ gear icon in the left sidebar.
- Choose Project settings.
- Navigate to Service Accounts:
- In the Project settings, select the Service accounts tab.
- Scroll down and find Firebase Admin SDK.
- Generate a New Private Key:
- Click Generate new private key.
- This will download a JSON file (firebase-adminsdk-xxxxx.json).
Important Notes
- Handle with care! This file contains sensitive credentials. Do not expose it publicly.
- Use in your backend: Place it in a secure location where only authorized applications can access it.
make sure to save it as `bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json`


![image](https://github.com/user-attachments/assets/c707cc54-8388-4c49-bbe7-bee3025bc692)

## Output 
The auto correct exitst :)
yay!

## Next Week 
- Improve the AI model
- get it connected faster
