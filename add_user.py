import pyaudio
import wave
import os
import pickle
import time
from scipy.io.wavfile import read
from IPython.display import Audio, display, clear_output
from pydub import AudioSegment
import sys
from main_functions import *

def add_user():

    name = sys.argv[1]
    #Voice authentication
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 10

    source = "./voice_database/" + name
    dst = source + "/1.wav"	
    sound = AudioSegment.from_file(dst)
    sound = sound.set_frame_rate(8000)
    sound.export(dst, format="wav")

    dst = source + "/2.wav"	
    sound = AudioSegment.from_file(dst)
    sound = sound.set_frame_rate(8000)
    sound.export(dst, format="wav")

    dst = source + "/3.wav"	
    sound = AudioSegment.from_file(dst)
    sound = sound.set_frame_rate(8000)
    sound.export(dst, format="wav")

    try:
        dest =  "./gmm_models2/"
        count = 1

        for path in os.listdir(source):
            path = os.path.join(source, path)

            features = np.array([])

            # reading audio files of speaker
            (sr, audio) = read(path)

            # extract 40 dimensional MFCC & delta MFCC features
            vector   = extract_features(audio,sr)

            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))

            # when features of 3 files of speaker are concatenated, then do model training
            if count == 3:
                gmm = GaussianMixture(n_components = 17, max_iter = 2100, covariance_type='spherical',n_init = 50)
                gmm.fit(features)

                # saving the trained gaussian model
                pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
                print(name + ' added successfully')

                features = np.asarray(())
                count = 0
            count = count + 1

    except Exception as e:
        print('Username already exist, try another user name.')
        print(str(e))

if __name__ == '__main__':
    add_user()
