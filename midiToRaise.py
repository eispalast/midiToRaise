from time import sleep

from ordered_set import T
from configuration import configuration
#import pygame.midi
import threading
import serial
import serial.tools.list_ports

dygma = None
config = None


def translate():
    global config
    print("Started translating")
    while(True):
        # wait for midi input and send it to the raise
        pass



def initialize():
    global dygma
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if p.description == "Raise":
            dygma = serial.Serial(port=p.device)
            if dygma != None:
                print("Success")
            # really check if the kb was found
            break
    global config
    config = configuration()

if __name__ == "__main__":
    initialize()

    
    translate_thr = threading.Thread(target=translate)
    translate_thr.daemon = True
    translate_thr.start()
    config.mainMenu()
    # print(number)