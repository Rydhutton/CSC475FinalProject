#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pyaudio
import numpy

def main():

	# initalize PyAudio
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=1,
                rate=11025,
                input=True,
                output=False,
                frames_per_buffer=(1024*2)

print("* recording")
	
	"""if (len(sys.argv) <= 1):
		print("\nTo use, type 'py Main.py <command>'.\nCommands include -mine or -train or -test")
	elif (sys.argv[1] == "-mine"):
		Scraper.StartCollectingData()
	elif (sys.argv[1] == "-train"):
		SVM.TrainOnData()
	else:
		print("unknown mode")"""
	
if __name__ == "__main__":
    main()