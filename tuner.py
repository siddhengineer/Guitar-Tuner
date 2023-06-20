# This is the code for a Guitar Tuner python program
'''
firstly importing the libraries
'''
import sounddevice as sd
import numpy as np
import scipy.fftpack
import os


sample_freq = 44100  # (Hz)audio samples captured per second
window_size = 44100  # number of samples that are considered in each analysis
window_step = 21050  # shift between consecutive windows
window_length = window_size/sample_freq  # calculate window length in second
sample_length = 1/sample_freq  # time duration between two consecutive samples
window_samples = [0]*window_size

'''

code to find the closest note for a given input,
using the mathematical formula 

'''
concert_pitch = 440  # constant value
all_notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


def find_closest_note(pitch):
    i = int(np.round(np.log2(pitch/concert_pitch)*12))
    closest_note = all_notes[i % 12]+str(4+((i+9)//12))
    closest_pitch = concert_pitch*2**(i/12)
    return closest_note, closest_pitch


'''
now defining  the callback function of sounddevice library
'''


def callback(indata, frames, time, status):
    global window_samples
    if status:
        print(status)
    if any(indata):
        # append new samples
        window_samples = np.concatenate((window_samples, indata[:, 0]))
        # remove old samples
        window_samples = window_samples[len(indata[:, 0]):]
        # finding Fast Fourier Transform values
        fft_values = abs(scipy.fftpack.fft(window_samples)
                         [:len(window_samples)//2])
        '''
        calculates the frequency resolution of the FFT analysis
         (range up to 62 Hz)
        '''
        for i in range(int(62/(sample_freq/window_size))):
            fft_values[i] = 0

        max_index = np.argmax(fft_values)
        max_freq = max_index*(sample_freq/window_size)

        closestNote, closestPitch = find_closest_note(max_freq)

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Closest note: {closestNote} {max_freq:.1f}/{closestPitch:.1f}")
    else:
        print('no input')


'''
taking microphone input

'''
try:
    with sd.InputStream(channels=1, callback=callback,
                        blocksize=window_step,
                        samplerate=sample_freq):
        while True:
            pass
except Exception as e:
    print(str(e))
