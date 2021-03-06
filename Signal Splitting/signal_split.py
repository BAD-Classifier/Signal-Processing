import librosa.display
import os
import librosa
import sklearn
import matplotlib.pyplot as plt

# Change the genus for the bird you want to convert
genus = 'Andropadus'

#Andropadus Importunus - Sombre Greenbul
#Anthus Crenatus - African Rock Pipit
#Camaroptera Brachyura - Green-backed Camaroptera
#Cercotrichas Leucophrys - White-browed Scrub Robin
#Chlorophoneus Olivaceus - Olive Bushshrike
#Cossypha Caffra - Cape Robin-Chat
#Laniarius Ferrugineus - Southern Boubou
#Prinia Maculosa - Karoo Prinia
#Sylvia Subcaerulea - Chestnut-vented Warbler
#Telophorus Zeylonus - Bokmakierie

def convert_to_image(birdSoundPath, birdName):
    x, fs = librosa.load(birdSoundPath, sr=None, mono=True)

    win_length = 4 * fs
    sound_length = len(x)
    div = sound_length//win_length
    start = 0
    end = win_length
    clips = []

    for i in range(0,div):
        clips.append(x[start:end])
        start += win_length
        end += win_length
    
    if len(x[start:]) > win_length/2:
        clips.append(x[start:])
    u_id = 1
    path = os.getcwd() + '/4_seconds/sounds/'
    if not os.path.exists(path):
        os.makedirs(path)

    for clip in clips:
        librosa.output.write_wav(path+(birdName[:-4]) + '-'+str(u_id) + '.wav' , clip, fs)
        mfccs = librosa.feature.mfcc(clip, sr=fs, n_fft=1024, hop_length=512, n_mfcc=13, fmin=20, fmax=12000)
        mfccs = sklearn.preprocessing.scale(mfccs, axis=1)  
        librosa.display.specshow(mfccs, sr=fs*2, cmap='coolwarm')
        picName = birdName[:-4] + '-' + str(u_id) + '.png'
        save_image(picName)
        u_id = u_id + 1

def save_image(picName):
    path = os.getcwd() + '/4_seconds/MFCCs/'
    if not os.path.exists(path):
        os.makedirs(path)
    fileName = path + picName
    plt.savefig(fileName, bbox_inches='tight', pad_inches=0)


def main():

    plt.rcParams['figure.figsize'] = (14,4)
    batch_size = 15
    batch_num = 1


    path = os.getcwd() + '/ALL/' + genus
    fileNames = os.listdir(path)
    all_genus_id = []
    path = os.getcwd() + '/4_seconds/MFCCs/' 
    if not os.path.exists(path):
        os.makedirs(path)
    incompleteFiles = os.listdir(path)
    completedFiles = []
    remainingSoundPaths = []

    for fileName in incompleteFiles:
        fileName = fileName[:-4]
        fileName = fileName.split('-')
        if fileName[0] == genus:
            completedFiles.append(fileName[0]+fileName[-2])

    for fileName in fileNames:
        temp = fileName[:-4]
        temp = temp.split('-')
        genus_id = temp[0] + temp[-1]
        
        if (genus_id in completedFiles):
            print("Already converted")
        else:
            remainingSoundPaths.append(fileName)

    path = os.getcwd() + '/ALL/' + genus

		# Does conversions in batches of 15, running the script for more audio files starts to slow down the conversion process
    for fileName in remainingSoundPaths:
        if batch_num < 16:
            birdSound = path + '/' + fileName
            print(str(batch_num) + '/' + str(batch_size) + ' ' + fileName + ' conversion has started')
            convert_to_image(birdSound, fileName)
            print(str(batch_num) + '/' + str(batch_size) + ' ' + fileName + ' MFCC has been generated')
            batch_num = batch_num + 1
        else:
            break

if __name__ == "__main__":
    main()
