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

init()
window_size = 1280, 720
window = display.set_mode(window_size)
clock = time.Clock()

player = Rect(150, window_size[1]//2 - 100, 100, 100)

def generate_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=440, distance=650):
    pipes = []
    start_x = window_size[0]
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = Rect(start_x, 0, pipe_width, height)
        bottom_pipe = Rect(start_x, height + gap, pipe_width, window_size[1] - (height + gap))
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distance
    return pipes