
import matplotlib.pyplot as plt
import PyDragonfly
from PyDragonfly import copy_to_msg
import numpy as np
from scipy import signal
import time



from PyDragonfly import copy_from_msg
import sound_buffer as sbuff


if __name__ == "__main__":


    config = {}
    execfile("bbmi.conf", config)

    MID_VIZ = config["MID_VIZ"]
    BUFFER_SIZE = config["BUFFER_SIZE"]

    mod = PyDragonfly.Dragonfly_Module(MID_VIZ, 0)
    mod.ConnectToMMM("localhost:7111")
    mod.Subscribe(sbuff.MT_SOUND_BUFFER_50HZ)

    viz_buffer = np.zeros(44100, dtype=np.int16)

    fs = 44100
    plt.ion()
    f, t, Sxx = signal.spectrogram(viz_buffer, fs)
    plt.pcolormesh(t, f, Sxx)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show(block=False)

    

    off_set = 0
    audio_chunk = 1

    while True:
        msg = PyDragonfly.CMessage()
        mod.ReadMessage(msg)    # blocking read

        if msg.GetHeader().msg_type == sbuff.MT_SOUND_BUFFER_50HZ:

            sound_msg = sbuff.MDF_SOUND_BUFFER_50HZ()
            print "Sound buffer Received"
            copy_from_msg(sound_msg, msg)

            for i in range(0, BUFFER_SIZE):
                viz_buffer[off_set * BUFFER_SIZE + i] = sound_msg.buffer[i]

            plt.clf()
            # plotting
            f, t, Sxx = signal.spectrogram(viz_buffer, fs)
            plt.draw_all()
            plt.pause(0.001)
            off_set = 0
            audio_chunk += 1

        off_set += 1

    mod.DisconnectFromMMM()
