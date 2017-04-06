#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import wave
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import *

CHUNK = 16384
MAX = 32768.0
DTYPE = np.int16

def main():
	# determine launch context
	
	if (sys.argv[1] == 'plot'): # usage = "python Main.py plot something.wav"
		plot()
	elif (sys.argv[1] == 'sin'): # usage = "python Main.py sin"
		sin_wave_ex()
	elif (sys.argv[1] == 'di'): # usage = "python Main.py di something.wav"
		destructive_interference_demo()
		
def destructive_interference_demo():
	wf = wave.open(sys.argv[2], 'rb')

	# begin audio stream
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=2,rate=wf.getframerate(),output=True)

	# read data from wav file
	data = wf.readframes(CHUNK)
	while len(data) > 0:
		# read from file, convert to usable form
		audio_data = np.fromstring(data, dtype=DTYPE)
			
		# split audio data into two channels & calculate anti-signal
		stereo_data = np.zeros([CHUNK,2])
		for i in range(int(len(audio_data)/2)):
			x = i*2
			stereo_data[i,0] = audio_data[x] #left speaker
			stereo_data[i,1] = -audio_data[x] #right speaker
		
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
	
def sin_wave_ex():

	# begin audio stream
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(2),channels=2,rate=11025,output=True)
	
	# write sine wave data
	i  = 0.0
	while True:
		stereo_data = np.zeros([CHUNK,2])
		for n in range(CHUNK):
			stereo_data[n,0] = math.sin(i/10.0)*30000 #left speaker
			stereo_data[n,1] = math.sin(i/10.0)*30000 #right speaker
			i+=1.0
	
		# write audio data to output
		out_data = np.array(stereo_data, dtype=DTYPE)
		string_audio_data = out_data.tostring()
		stream.write(string_audio_data, CHUNK)
	
	# cleanup
	stream.stop_stream()
	stream.close()
	p.terminate()

def plot():
	wf = wave.open(sys.argv[2], 'rb')

	# begin audio stream
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=2,rate=wf.getframerate(),output=True)
		
	energy_before = 0
	energy_after = 0
	lastFFT = None
	#TODO use averages 
	#TODO plot energy over time
	
	# read data from wav file
	plot_data = []
	plot_inv = []
	plot_sum = []
	data = wf.readframes(CHUNK)
	while len(data) > 0:
	
		# read from file, convert to usable form
		audio_data = np.fromstring(data, dtype=DTYPE) / MAX
		
		if lastFFT==None:
			synth = np.fft.ifft(np.fft.fft(audio_data))
		else:
			synth = np.fft.ifft(lastFFT)
		
		for i in range(int(len(audio_data)/2)):
			a = audio_data[i] # actual 
			b = -synth[i] * 1.0
			plot_data.append(a)	
			plot_inv.append(-synth[i])
			plot_sum.append(a+b)
			if (lastFFT==None):
				eatpoo = True
			else:
				energy_before += abs(a)
				energy_after += abs(a+b)
		
		# fetch new audio data
		lastFFT = np.fft.fft(audio_data)
		data = wf.readframes(CHUNK)
		
	print('energy ratio:'+str(energy_after/energy_before))
		
	# cleanup
	stream.stop_stream()
	stream.close()
	p.terminate()	
		
	# plot result
	plt.figure(figsize=(15,4))
	plt.plot(plot_data, 'r', plot_sum, 'b', plot_inv, 'y')#, plot_inv, 'y'
	plt.show()
	
if __name__ == "__main__":
    main()

