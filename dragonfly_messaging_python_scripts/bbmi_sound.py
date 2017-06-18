import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from time import sleep


def generate_tone(freq, len, amp=20000, rate=44100):

    t = np.linspace(0, len, len * rate)

    data = np.sin(2 * np.pi * freq * t) * amp
    return data.astype(np.int16)


def generate_test_tones(harmonics=5):

    t = generate_tone(220, 4410) / harmonics

    for i in range(1, harmonics):
        h = generate_tone(440, 4410) / harmonics
        t = np.add(t, h)

    return t


if __name__ == "__main__":

    test_tone = generate_test_tones()

    print 'Playing test tone, you should hear an annoying  tone shortly'

    sd.play(test_tone)
    sleep(4)
