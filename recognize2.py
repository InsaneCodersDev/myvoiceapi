import pyaudio
import wave
import os
import pickle
import time
from scipy.io.wavfile import read


from main_functions import *

def recognize(filename):
    # Voice Authentication
    ambiguity = 2
    threshold = 2

    modelpath = "./gmm_models2/"

    gmm_files = [os.path.join(modelpath,fname) for fname in 
                os.listdir(modelpath) if fname.endswith('.gmm')]

    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]

    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
                in gmm_files]
  
    if len(models) == 0:
        print("No Users in the Database!")
        return
        
    #read test file
    sr,audio = read(filename)
    
    # extract mfcc features
    vector = extract_features(audio,sr)
    log_likelihood = np.zeros(len(models)) 
    diff=np.zeros(len(models))
    #checking with each model one by one
    for i in range(len(models)):
        gmm = models[i]         
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
        print("Score for ",speakers[i]," is:",log_likelihood[i])

    pred = np.argmax(log_likelihood)
    identity = speakers[pred]
    print(log_likelihood[pred])
    count=0
    for i in range(len(models)):
        diff[i]=log_likelihood[pred]-log_likelihood[i]
        if diff[i]>threshold:
            count=count+1
    print(diff)
    print(count)
    # if voice not recognized than terminate the process
    if identity == 'unknown' or identity == 'unknown2' or identity == 'unknown3' or identity == 'unknown4' or identity == 'unknown5':
            print("Not Recognized! Try again...")
            return "Not identified"
    else:
        if count>=len(models)-ambiguity:
            print( "Recognized as - ", identity)
            return identity
        else:
            print( "Not recognised try again")
            return "Not identified"
        
if __name__ == '__main__':
    recognize()
