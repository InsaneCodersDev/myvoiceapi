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
    CHANNELS = 1
    RATE = 8000
    CHUNK = 1024
    RECORD_SECONDS = 1.5

    source = "./voice_database/" + name
    dst = source + "/1.wav"	
    sound = AudioSegment.from_file(dst)
    sound = sound.set_frame_rate(8000)
    sound = sound.set_channels(1)
    sound = sound.set_sample_width(2)
    sound.export(dst, format="wav")

    dst = source + "/2.wav"	
    sound = AudioSegment.from_file(dst)
    sound = sound.set_frame_rate(8000)
    sound = sound.set_channels(1)
    sound = sound.set_sample_width(2)
    sound.export(dst, format="wav")

    dst = source + "/3.wav"	
    sound = AudioSegment.from_file(dst)
    sound = sound.set_frame_rate(8000)
    sound = sound.set_channels(1)
    sound = sound.set_sample_width(2)
    sound.export(dst, format="wav")

    dst = source + "/4.wav"     
    sound = AudioSegment.from_file(dst)
    sound = sound.set_frame_rate(8000)
    sound = sound.set_channels(1)
    sound = sound.set_sample_width(2)
    sound.export(dst, format="wav")

    dst = source + "/5.wav"     
    sound = AudioSegment.from_file(dst)
    sound = sound.set_frame_rate(8000)
    sound = sound.set_channels(1)
    sound = sound.set_sample_width(2)
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
            if count == 5:
                gmm = GaussianMixture(n_components = 12, max_iter = 2000, covariance_type='spherical',n_init = 50, random_state=39)
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
