#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import wave
import sys
import matplotlib.pyplot as plt
import numpy as np

CHUNK = 1024
DTYPE = np.int16
wf = wave.open(sys.argv[1], 'rb')

# begin audio stream
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=2,rate=wf.getframerate(),output=True)

# read data
data = wf.readframes(CHUNK)

while len(data) > 0:
	# read from file, convert to usable form
	audio_data = np.fromstring(data, dtype=DTYPE)
		
	stereo_data = np.zeros([CHUNK,2])
	for i in range(CHUNK):
		x = i*2
		stereo_data[i,0] = 0#audio_data[x]
		stereo_data[i,1] = audio_data[x+1]
	
	# write audio data to output
	out_data = np.array(stereo_data, dtype=DTYPE)
	string_audio_data = out_data.tostring()
	stream.write(string_audio_data, CHUNK)
	
	# fetch new audio data
	data = wf.readframes(CHUNK)

# cleanup
stream.stop_stream()
stream.close()
p.terminate()