#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import wave
import sys
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import *

#CHUNK = 4096
CHUNK = 8192
#CHUNK = 16384
#CHUNK = 32768
#CHUNK = 65536
MAX = 32768.0

def main():
	# determine launch context
	# "python Main.py something.wav" = calc most-recent-frame
	# optional -- add "plot" at end of command for visual plot
	# "python Main.py di something.wav" = 2-speaker destructive interference demo
	# "python Main.py sin" = test sine wave output
	if (sys.argv[1] == 'sin'): 
		debug_sine()
	elif (sys.argv[1] == 'di'): 
		destructive_interference_demo()
	else:
		calculate() 
		
def calculate():
	# begin audio stream
	wf = wave.open(sys.argv[1], 'rb')
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=2,rate=wf.getframerate(),output=True)
		
	# config
	linear_interpolate = True
	anti_signal_strength = 0.75
	n_averaging_set = 3
	delay = 1
	
	# vars
	plot_data = []
	plot_sum = []
	plot_inv = []
	delayed_data = []
	averaging_set = []
	energy_before = 0
	energy_after = 0	
	data = wf.readframes(CHUNK)
	T = delay #hacky fix
	
	#todo:negative feedback 
	
	# initialize
	for i in range(delay):
		delayed_data.append( np.zeros(CHUNK) )
			
	# read data from wav file
	while len(data) > 0:
	
		# read from file (stereo data), convert to usable form
		raw_data = np.zeros(CHUNK)
		wav_data = np.fromstring(data, dtype=np.int16) / MAX
		for i in range(int(len(wav_data)/2)):
			raw_data[i] = wav_data[i*2]
			
		# extract frequency data
		FFT_data = np.fft.fft(raw_data)
		delayed_data.append(FFT_data)
		
		# "recieve" delayed frequency data
		fresh_data = delayed_data.pop(0)
		averaging_set.append(fresh_data)
		if (len(averaging_set) > n_averaging_set):
			averaging_set.pop(0)
			
		# synthesize anti-signal (phase-shift by 180 degrees)
		AVG_FFT = np.zeros(CHUNK, dtype=complex)
		for i in range(len(averaging_set)):
			if (linear_interpolate):
				for j in range(CHUNK):
					AVG_FFT[j] += averaging_set[i][j] * ((i+1)/(len(averaging_set)+1))
			else:
				for j in range(CHUNK):
					AVG_FFT[j] += averaging_set[i][j]
		if (linear_interpolate):
			s = 0
			for i in range(len(averaging_set)):
				s += ((i+1)/(len(averaging_set)+1))
			for j in range(CHUNK):
				AVG_FFT[j] = AVG_FFT[j] / s
		else:
			for j in range(CHUNK):
				AVG_FFT[j] = AVG_FFT[j] / len(averaging_set)
		fin_freq = np.zeros(CHUNK, dtype=complex)
		for i in range(len(AVG_FFT)):
			angle = np.angle(AVG_FFT[i])
			mag = np.abs( AVG_FFT[i] )
			angle = angle + (math.pi) # phase shift waveforms
			fin_freq[i] = (math.cos(angle) + (1j*math.sin(angle)))*mag
		synth = np.fft.ifft(fin_freq)
		
		# calc results, fetch new audio data
		for i in range(CHUNK):
			a = raw_data[i]
			b = synth[i] * anti_signal_strength
			c = a+b
			plot_data.append(a)	
			plot_inv.append(b)
			plot_sum.append(c)
			if (T == 0): 
				if (a!=0): #hacky fix
					energy_before += abs(a)
					energy_after += abs(c)
		if (T > 0):
			T -= 1
		data = wf.readframes(CHUNK)
		
	print('energy ratio:'+str(energy_after/energy_before))
		
	# cleanup
	stream.stop_stream()
	stream.close()
	p.terminate()	
		
	# plot result
	zero = np.zeros(len(plot_data))
	if (len(sys.argv) > 2):
		if (sys.argv[2] == "plot"):
			plt.figure(figsize=(15,4))
			plt.plot(plot_data, 'b', plot_inv, 'r', zero, '#999999')
			#plt.plot(plot_sum, '#bbbbff', plot_data, 'b', zero, '#999999')
			plt.show()		
		
def destructive_interference_demo():
	wf = wave.open(sys.argv[2], 'rb')

	# begin audio stream
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=2,rate=wf.getframerate(),output=True)

	# read data from wav file
	data = wf.readframes(CHUNK)
	while len(data) > 0:
		# read from file, convert to usable form
		audio_data = np.fromstring(data, dtype=np.int16)
			
		# split audio data into two channels & calculate anti-signal
		stereo_data = np.zeros([CHUNK,2])
		for i in range(int(len(audio_data)/2)):
			x = i*2
			stereo_data[i,0] = audio_data[x] #left speaker
			stereo_data[i,1] = -audio_data[x] #right speaker
		
		# write audio data to output
		out_data = np.array(stereo_data, dtype=np.int16)
		string_audio_data = out_data.tostring()
		stream.write(string_audio_data, CHUNK)
		
		# fetch new audio data
		data = wf.readframes(CHUNK)

	# cleanup
	stream.stop_stream()
	stream.close()
	p.terminate()
	
def debug_sine():

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
		out_data = np.array(stereo_data, dtype=np.int16)
		string_audio_data = out_data.tostring()
		stream.write(string_audio_data, CHUNK)
	
	# cleanup
	stream.stop_stream()
	stream.close()
	p.terminate()
	
if __name__ == "__main__":
    main()

