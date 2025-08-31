import sounddevice as sd
import numpy as np
from pygame import *
from random import randint


fs = 16000
block = 256
mic_level = 0.0


def audio_cb(indata, frames, time, status):
    global mic_level
    if status:
        return
    rms = float(np.sqrt(np.mean(indata**2)))
    mic_level = 0.85 * mic_level * 0.15 * rms


