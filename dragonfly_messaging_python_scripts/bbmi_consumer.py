#!/usr/bin/python
import numpy as np
import PyDragonfly
from PyDragonfly import copy_from_msg, copy_to_msg
import sound_buffer as sbuff
import sounddevice as sd
import Dragonfly_config as rc
import time
from bbmi_messaging import copy_to_sound_buffer


def request_audio():
    mod.SendMessage(request)
    msg = PyDragonfly.CMessage()
    mod.ReadMessage(msg)    # blocking read


    if msg.GetHeader().msg_type == sbuff.MT_SOUND_BUFFER_50HZ:

        
        copy_from_msg(sound_msg, msg)
        copy_to_sound_buffer(sound_msg, play_buffer, 0, BUFFER_SIZE)



def audio_callback (outdata, frames,
    time,CallbackFlags):

    request_audio()
    outdata[:] = play_buffer



if __name__ == "__main__":

    config = {}
    execfile("bbmi.conf", config)

    MID_CONSUMER = config["MID_CONSUMER"]
    BUFFER_SIZE = config["BUFFER_SIZE"]
    SAMPLE_RATE = config["SAMPLE_RATE"]

    mod = PyDragonfly.Dragonfly_Module(MID_CONSUMER, 0)
    mod.ConnectToMMM("localhost:7111")
    mod.Subscribe(sbuff.MT_SOUND_BUFFER_50HZ)


    play_buffer = np.zeros(shape = (BUFFER_SIZE, 1), dtype=np.int16)

    print "Consumer running...\n"

    sound_msg = sbuff.MDF_SOUND_BUFFER_50HZ()

    request = PyDragonfly.CMessage(sbuff.MT_REQUEST_AUDIO_BUFFER)
    request_message = sbuff.MDF_REQUEST_AUDIO_BUFFER()
    copy_to_msg(request_message, request)

    time.sleep(5)

    indata = np.ndarray(shape = (BUFFER_SIZE, 1))


    with sd.OutputStream(channels=1, callback=audio_callback, blocksize = BUFFER_SIZE, samplerate=SAMPLE_RATE):
        print("#" * 80)
        print("press Return to quit")
        print("#" * 80)
        input()


    mod.DisconnectFromMMM()
