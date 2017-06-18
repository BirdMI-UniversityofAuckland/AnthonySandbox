import os
import sys

if __name__ == "__main__":

    bci_path = os.environ['BCI_MODULES']
    sys.path.insert(0, bci_path + '\SampleGenerator')
    import SampleGenerator as sg
    sg.SampleGenerator('sample_gen.config', 'localhost:7111')
