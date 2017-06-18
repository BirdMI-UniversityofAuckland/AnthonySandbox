import os
import sys
import subprocess
import time
import numpy as np
import sounddevice as sd
from multiprocessing import Process


if __name__ == "__main__":

    print("Main")

    try:
        dragonfly_path = os.environ["DRAGONFLY"]

    except KeyError:
        print("Exiting, DRAGONFLY environment variable not set")
        sys.exit(1)

    python_files = ["bbmi_sample_generator.py",
                    "bbmi_producer.py", "bbmi_consumer.py", "bbmi_visualization"]
    # python_files = [
    # "bbmi_sample_generator.py", "bbmi_producer.py", "bbmi_consumer.py"]

    # Windows
    print('Attempting to launch MessageManager')

    try:
        subprocess.Popen(
            dragonfly_path + "/bin/MessageManager.exe", creationflags=subprocess.CREATE_NEW_CONSOLE)
    except:
        print('Failed to launch MessageManager')
        sys.exit(1)
    print('Succeeded')

    for file in python_files:
        print('Attempting to launch ', file)
        try:
            subprocess.Popen(
                ['python', file], creationflags=subprocess.CREATE_NEW_CONSOLE)
            print('Succeeded')
        except:
            print('Failed to launch', file)
            sys.exit(1)
