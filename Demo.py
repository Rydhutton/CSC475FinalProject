import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
import pyaudio
import sys
import wave


def combine(wave1, wave2):

    combinedData = []

    if(wave1.size != wave2.size):
        print "error"
        exit()

    for i in range(wave1.size):
        combinedData.append(wave1[i] + wave2[i])

    return combinedData


def demo(twosine, elimsine):

    rate, data = read(twosine)
    print "sample rate: ", rate, "Hz"
    #print data

    plt.plot(data, 'b', label="720/240Hz Mixture")
    plt.ylim([-2.5, 2.5])
    plt.xlim([0, 440])

    antirate, antidata = read(elimsine)
    for i in range(antidata.size):
        antidata[i] *= -1.0
    write("AntiSine.wav", 44100, antidata)

    plt.plot(antidata, 'r', label='240Hz wave w/ inverted phase')
    plt.legend()
    plt.show()



    combo = combine(data, antidata)
    plt.plot(data, 'b', linestyle='dotted')
    plt.plot(antidata, 'r', linestyle='dotted')
    plt.plot(combo, 'k')
    plt.title("Resulting single 720Hz Sine Wave")
    plt.ylim([-2.5, 2.5])
    plt.xlim([0, 440])
    plt.show()

    combo = np.array(combo)
    write("720Sine.wav", 44100, combo)


def playWav(wavfile):

    chunk = 1024
    wf = wave.open(wavfile, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=
                    p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.close()
    p.terminate()


def main():

    demo("Sine.wav", "240Sine.wav")

if __name__ == "__main__":
    main()
