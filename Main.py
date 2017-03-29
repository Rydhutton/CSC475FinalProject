#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import wave
import sys
import matplotlib.pyplot as plt
import numpy as np

CHUNK = 1024
MAX_INT = 32768.0
wf = wave.open(sys.argv[1], 'rb')

# begin audio stream
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=2,rate=wf.getframerate(),output=True)

# read data
to_plot = []
n = 15
data = wf.readframes(CHUNK)

while (n>0):
	data = wf.readframes(CHUNK)
	audio_data = (np.fromstring(data, dtype=np.int16)) / MAX_INT
	for i in range(len(audio_data)):
		to_plot.append(audio_data[i])
	n -= 1

# play stream (3)
#while len(data) > 0:
#    stream.write(data)
#	data = wf.readframes(CHUNK)

	
plt.plot(to_plot)
plt.show()
	
# Clean up
stream.stop_stream()
stream.close()
p.terminate()