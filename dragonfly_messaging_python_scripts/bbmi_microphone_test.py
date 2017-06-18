
import argparse
import csv
import time

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as write_wav

import bbmi_sound as b_s

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Plays a series \
        of test tones and records the response (RMS) for microphone calibration")

    parser.add_argument('-fname', type=str,
                        help="File prefix name for saved wavs e.g FILE_NAME_FREQUNCY.wav and RMS data")

    parser.add_argument("-sf", help="Sampling frequncy", type=int)
    parser.add_argument("-strt", help="Start frequency", type=int)
    parser.add_argument("-ss", help="Frequency step size", type=int)
    parser.add_argument("-fin", help="Finish frequency", type=int)
    parser.add_argument(
        "-len", help="Length of tones played, in seconds", type=int)

    args = parser.parse_args()

    if not args.sf:
        SAMPLING_FREQ = 44100
    else:
        SAMPLING_FREQ = args.sf

    if not args.strt:
        start_freq = 400
    else:
        start_freq = args.strt

    if not args.ss:
        freq_step = 100
    else:
        freq_step = args.ss

    if not args.fin:
        finish_freq = 7200
    else:
        finish_freq = args.fin

    if not args.len:
        tone_length = 0.5
    else:
        tone_length = args.len

    current_freq = start_freq

    freq_rms = []

    print "Using Sampling frequency", SAMPLING_FREQ, "|| Starting frequency", start_freq,\
        "|| Frequency step", freq_step, "|| Finish frequency", finish_freq, "|| Tone length (s)", tone_length

    while current_freq <= finish_freq:

        Tone = b_s.generate_tone(current_freq, tone_length)

        print "Playing ", current_freq, "Hz..."

        rec = sd.playrec(data=tone, samplerate=SAMPLING_FREQ, channels=1)
        time.sleep(tone_length)

        write_wav(
            args.fname + "_" + str(current_freq) + ".wav", SAMPLING_FREQ, rec)

        rms = np.sqrt(np.mean(np.square(rec)))
        freq_rms.append([current_freq, rms])

        current_freq += freq_step

    with open(args.fname + "_RMS_data" + ".csv", "wb") as text_output:
        writer = csv.writer(text_output)
        writer.writerow(["Frequency (Hz)", "Reponse (RMS)"])
        for freq_response in freq_rms:
            writer.writerow(freq_response)

        # Calculate and write rms
