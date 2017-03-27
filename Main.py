#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pyaudio
import numpy

def main():

	# initalize PyAudio
	WIDTH = 2
	p = pyaudio.PyAudio()
	audio_stream = p.open(format=p.get_format_from_width(WIDTH),channels=1,rate=11025,input=True,output=False,frames_per_buffer=(1024*2))
	print("*recording")
	
	# clean up
	audio_stream.stop_stream()
	audio_stream.close()
	p.terminate()
	
if __name__ == "__main__":
    main()