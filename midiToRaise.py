from time import sleep

from configuration import configuration
import pygame.midi as midi
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
            if dygma.is_open:
                print("Success")
            else:
                print("Could not connect to Raise. Is another process accessing it?")
            # really ch1eck if the kb was found
            break
    global config
    config = configuration()

    # Initialize midi device
    midi.init()
    
    for i in range(midi.get_count()):
        device = midi.get_device_info(i)
        if config.midi_device_name in str(device[1]) and device[2] == 1:
            print("hooray")
            config.midi_device = midi.Input(i)
    if config.midi_device == None:
        print("MIDI device not found. Chose MIDI device in options menu")

if __name__ == "__main__":
    initialize()

    
    translate_thr = threading.Thread(target=translate)
    translate_thr.daemon = True
    translate_thr.start()
    config.mainMenu()
    # print(number)