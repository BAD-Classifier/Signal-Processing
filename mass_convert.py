from pydub import AudioSegment
import glob

recording_list = glob.glob("*.mp3")
print(recording_list)

for record in recording_list:
	bird_recording = AudioSegment.from_mp3(record)
	print(bird_recording.frame_rate)
	converted_name = record[:-3] + "wav"
	bird_recording.export(converted_name, format="wav")



