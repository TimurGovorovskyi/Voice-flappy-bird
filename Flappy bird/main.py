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

pipes = generate_pipes(5)
font1 = font.Font(None, 100)
score = 0
lose = False
wait = 40

y_vel = 0.0
gravity = 0.6
THRESH = 0.001
IMPULSE = -0.8

with sd.InputStream(samplerate=fs, channels=1, blocksize=block, callback=audio_cb):
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()

        if mic_level > THRESH:
            y_vel = IMPULSE
        y_vel += gravity
        player.y += int(y_vel)

        window.fill((0, 0, 160))
        draw.rect(window, (255, 0, 0), player)

        for pipe in pipes[:]:
            if not lose:
                pipe.x -= 10
                draw.rect(window, (0, 255, 0), pipe)
                if pipe.x < -100:
                    pipes.remove(pipe)
                    score += 0.5
                if player.colliderect(pipe):
                    lose = True

        if len(pipes) < 0:
            pipes += generate_pipes(150)

        score_text = font1.render(str(score), True, (255, 255, 255))
        window.blit(score_text, (window_size[0]//2 - score_text.get_rect().w//2, 40))

        display.update()
        clock.tick(60)

        if player.bottom > window_size[1]:
            player.bottom = window_size[1]
            y_vel = 0.0
        if player.top < 0:
            player.top = 0
            if y_vel < 0:
                y_vel = 0

        if lose and wait > 1:
            for pipe in pipes[:]:
                pipe.x += 8
            wait -= 1
        else:
            lose = False
            wait = 40