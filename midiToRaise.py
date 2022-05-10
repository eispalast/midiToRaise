from time import sleep
from configuration import configuration
import pygame.midi as midi
import threading
import serial
import serial.tools.list_ports

dygma = None
config = None

def rotate_layers(a):
    a["raise_action"]["layers"].append(a["raise_action"]["layers"].pop(0))


def translate():
    global config
    global dygma
    print("Started translating")
    while(True):
        # wait for midi input and send it to the raise
        if (config.midi_device != None):
            try:
                if midi.Input.poll(config.midi_device):
                    midiin=(midi.Input.read(config.midi_device,3))
                    for mid in midiin:
                        trig_event = mid[0][0] >> 4
                        trig_channel = mid[0][0] & 0xF
                        trig_key = mid[0][1]

                        for a in config.assignments:
                            if trig_event == a["midi"]["event"] and trig_channel == a["midi"]["channel"] and trig_key == a["midi"]["key"]:
                                send_string = f"layer.{a['raise_action']['action']} {a['raise_action']['layers'][0]}\n"
                                dygma.write(send_string.encode('utf-8'))
                                rotate_layers(a)
            except:
                continue
        else:
            print("MIDI device not configured. Go to options-> Select MIDI device.")
            sleep(5)
                    



def initialize():
    global dygma
    dygma = serial.Serial()
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if p.pid == 8705 and p.vid == 4617:
            dygma = serial.Serial(port=p.device)
            
            break
    if dygma.is_open:
        print("Success")
    else:
        print("Could not connect to Raise. Is it plugged in or another process accessing it?")
        print("Press any key to continue.")
        input()
    global config
    config = configuration()

    
if __name__ == "__main__":
    initialize()

    
    translate_thr = threading.Thread(target=translate)
    translate_thr.daemon = True
    translate_thr.start()
    config.mainMenu()
    # print(number)