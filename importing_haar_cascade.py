import cv2
import glob
import random
import numpy as np
import codecs, json

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Emotion list
fishface = cv2.face.FisherFaceRecognizer_create() #Initialize fisher face classifier

data = {}

def get_files(emotion): #Define function to get file list, randomly shuffle it and split 80/20
    files = glob.glob("E:/Emotion-Recognition-master/dataset//%s//*" %emotion)
    random.shuffle(files)
    training = files[:int(len(files))] #get first 80% of file list
    return training#, prediction

def make_sets():
    training_data = []
    training_labels = []    #prediction_data = []
    #prediction_labels = []
    prediction= [cv2.imread(file) for file in glob.glob('testing/*jpg')]


    for emotion in emotions:
        training = get_files(emotion)
        for item in training:
            image = cv2.imread(item) #open image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
            training_data.append(gray) #append image array to training data list
            training_labels.append(emotions.index(emotion))

    return training_data, training_labels, prediction#, prediction_labels

def trains():
    training_data, training_labels, prediction = make_sets()
    print ("training fisher face classifier")
    print ("size of training set is:", len(training_labels), "images")
    fishface.train(training_data, np.asarray(training_labels))
    print ("predicting classification set")  

def run_recognizer():
    cnt =0;
    prediction= [cv2.imread(file) for file in glob.glob('testing/*jpg')]
    predictions = []
    for image in prediction:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        out=cv2.resize(gray, (350, 350))
        pred, conf = fishface.predict(out)
        print("pred is :",emotions[pred])
        predictions.append(emotions[pred]);
        cv2.imwrite("static/images\\%s_%s.jpg" %(cnt, emotions[pred]), image)
        cnt=cnt+1;
        print(predictions)
    return predictions
             
#import an image
def crop_image(image):
    img=cv2.imread(image)
    
    #convert it into grayscale
    img1=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    
    #import haar classifier
    haar_face_cascade=cv2.CascadeClassifier('C:\opencv\sources\data\haarcascades\haarcascade_frontalface_alt.xml')
    
    faces = haar_face_cascade.detectMultiScale(img1, scaleFactor=1.1, minNeighbors=5)
     
    print('Faces found: ', len(faces))
    
    #loop in found faces
    for (x,y,w,h) in faces:
          cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
          
         
    
    fimg=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    i=0
    for (x,y,w,h) in faces:
     crop_img=fimg[y:y+h,x:x+w]
     cv2.imwrite("testing\\%s.jpg" %(i), crop_img)
     i=i+1
    
    predictions=run_recognizer()
    return predictions


