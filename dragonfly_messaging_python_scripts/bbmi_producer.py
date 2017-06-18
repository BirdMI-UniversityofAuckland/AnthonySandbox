#!/usr/bin/python
import time

import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wavfile

import bbmi_sound
import Dragonfly_config as rc
import PyDragonfly
import sound_buffer as sbuff
from bbmi_messaging import copy_to_sound_msg
from PyDragonfly import copy_to_msg

if __name__ == "__main__":

    config = {}
    execfile("bbmi.conf", config)

    MID_PRODUCER = config["MID_PRODUCER"]
    BUFFER_SIZE = config["BUFFER_SIZE"]

    mod = PyDragonfly.Dragonfly_Module(MID_PRODUCER, 0)
    mod.ConnectToMMM("localhost:7111")
    mod.Subscribe(rc.MT_SAMPLE_GENERATED)
    mod.Subscribe(sbuff.MT_REQUEST_AUDIO_BUFFER)

    sample_rate, test_sound = wavfile.read('bird_song_mono.wav')
    print('Sample rate ',  sample_rate)

    out_sound = PyDragonfly.CMessage(sbuff.MT_SOUND_BUFFER_50HZ)
    sound_msg = sbuff.MDF_SOUND_BUFFER_50HZ()

    print "Producer running...\n"

    buffer_index = 0
    run = True
    while run:

        msg = PyDragonfly.CMessage()
        mod.ReadMessage(msg)

#        if not current_buffer:
#            copy_to_sound_msg(sound_msg, test_sound, buffer_index, BUFFER_SIZE)
#            buffer_index += 1
#
 #           current_buffer = True

        # if msg.GetHeader().msg_type == rc.MT_SAMPLE_GENERATED:

        #     print "Received sample generated message"
        #     if not current_buffer:
        #         copy_to_buffer(test_sound, sound_msg, buffer_index)
        #         current_buffer = True
        #         buffer_index += 1

        #     if (buffer_index + 1) % 20 == 0:
        #         time.sleep(3)

        if msg.GetHeader().msg_type == sbuff.MT_REQUEST_AUDIO_BUFFER:
            # elif msg.GetHeader().msg_type == sbuff.MT_REQUEST_AUDIO_BUFFER:

            print "Received request for audio buffer"
            copy_to_sound_msg(sound_msg, test_sound, buffer_index, BUFFER_SIZE)
            copy_to_msg(sound_msg, out_sound)
            mod.SendMessage(out_sound)
            buffer_index += 1

