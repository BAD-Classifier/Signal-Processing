import numpy
import librosa
import glob
import os
import shutil

full_clips = glob.glob("Full_Clips/*.mp3")
print("Number of full clips: " + str(len(full_clips)))

for clip in full_clips:
    clip_name = clip[11:]
    print("Current clip: " + clip_name)
    signal, fs = librosa.load(clip)
    signal_abs = numpy.absolute(signal)

    search_name = "Cut_Clips/" + clip_name[:-4] + "*[0-9].*"
    cut_clips = glob.glob(search_name)
    print("Number of clip segments: " + str(len(cut_clips)))

    total_mean = numpy.mean(signal_abs)
    print("Signal Total mean: " + str(total_mean))
    condition = total_mean*0.25

    for record in cut_clips:
        signal_segment, sample_rate_segment = librosa.load(record)
        mean = numpy.mean(numpy.abs(signal_segment))
        if mean < condition:
            print(record)
            print("Segment mean: " + str(mean))
            shutil.move(record,"Rejected_noise/")    
                
rejected_clips = glob.glob("Rejected_noise/*.wav")
print(rejected_clips)
for item in rejected_clips:
    name = item[15:]
    new_name = "All_MFCCs/" + name[:-3] + "png"
    if os.path.isfile(new_name):
        shutil.move(new_name, "Rejected_MFCCS/")        
