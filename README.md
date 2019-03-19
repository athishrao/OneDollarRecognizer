<h1> One Dollar Recognizer </h1>

This is a simple python implementation of $1 recognizer. <br/>
The crux of this repo is the **OneDollar.py** file which implements the shape recognizer as defined in the Wobbrock et al. paper. It is a simple geometric and triginometry based algorithm that helps recognize single stroke gestures with impeccable accuracy even with a small traning dataset. <br/>
There are two files in this repo - **recognizeOffline.py** and **recognizeOnline.py**. The former has to do with simple verification of the working of the algorithm. You can view some testing functions that have been written to check the rigour of the algorithm. 
The latter is an attempt to give users the feel of trying out the software, in real time. 

Steps to run:
- [x] Clone this repo onto your local machine
- [x] Download and unzip the following folder http://depts.washington.edu/madlab/proj/dollar/xml.zip and place it in the same directory as the other files in this repo
- [x] Run app.py
- [x] Open https://0.0.0.0:80 and Voila!
