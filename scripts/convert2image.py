import numpy, scipy, matplotlib.pyplot as plt, librosa, sklearn
import urllib.request
import librosa.display
import os

def convert_to_image(birdSoundPath, birdName):
    x, fs = librosa.load(birdSoundPath,sr=None,mono=True)
    mfccs = librosa.feature.mfcc(x, sr=fs, n_fft=512, hop_length=256, n_mfcc=40)
    librosa.display.specshow(mfccs, sr=fs, x_axis='time')
    mfccs = sklearn.preprocessing.scale(mfccs, axis=1)  
    mfccs.mean(axis=1)
    mfccs.var(axis=1)
    librosa.display.specshow(mfccs, sr=fs*2, cmap='coolwarm')
    picName = birdName[:-4] + '.png'
    save_image(picName)

def save_image(picName):
    path = os.getcwd() + '/BirdMFCCS/TOP_10/ALL'
    if not os.path.exists(path):
        os.makedirs(path)
    fileName = path + picName
    plt.savefig(fileName)


def main():
    plt.rcParams['figure.figsize'] = (14,4)


    path = os.getcwd() + '/TOP_10/ALL'
    fileNames = os.listdir(path)
    for fileName in fileNames:
        birdSound = path + fileName
        convert_to_image(birdSound, fileName)
        print(fileName + ' MFCC has been generated') 

if __name__ == "__main__":
    main()
