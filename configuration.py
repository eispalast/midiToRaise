import json
from unittest import result

from boto import config
from menu import Menu
from pygame import midi as midi

MIDIEVENTS_I2S = {0x8:"Note Off", 0x9:"Note On", 0xC:"PC"}
MIDIEVENTS_S2I = {"Note Off":0x8, "Note On":0x9, "PC":0xC}

class configuration:
    path = None
    assignments = None
    _midi_device_name = None
    midi_device = None
    config = None
    def __init__(self,path="./midi2raise.json") -> None:
        self.path = path
        self.readConfig()
        self.initMidi()
    
    @property
    def midi_device_name(self):
        return self._midi_device_name
    
    @midi_device_name.setter
    def midi_device_name(self,new_val):
        self._midi_device_name = new_val
        self.config["mididevice"] = new_val
        self.writeConfig()

    def initMidi(self):
        midi.init()
    
        for i in range(midi.get_count()):
            device = midi.get_device_info(i)
            if self.midi_device_name in str(device[1]) and device[2] == 1:
                self.midi_device = midi.Input(i)

    def readConfig(self):
        with open(self.path,"r") as configFile:
            self.config = json.load(configFile)
            self.assignments = self.config["assignments"]
            self.midiStr2int()
            self.midi_device_name = self.config["mididevice"]

    def midiStr2int(self):
        for a in self.assignments:
            a["midi"]["event"] = MIDIEVENTS_S2I[a["midi"]["event"]]

    def midiInt2Str(self):
        for a in self.assignments:
            a["midi"]["event"] = MIDIEVENTS_I2S[a["midi"]["event"]]
                    
    def writeConfig(self):
        self.midiInt2Str()
        with open(self.path,"w") as configFile:
            json.dump(self.config, configFile, indent=2)
        self.midiStr2int()
    
    def mainMenu(self):
        while(True):
            options = ["[a] Assign mapping","[e] Edit/Delete mapping", "[o] Options","[q] Quit"]
            print("Choose an option")
            
            no_midi_warning = ""
            if (self.midi_device == None):
                no_midi_warning = "MIDI device not found. Chose MIDI device in options menu"
            
            main_menu = Menu(options=options,title=f"{no_midi_warning} What do you want to do?")
            selection = main_menu.start()
           
            if selection == 0:
                self.assignNewMenu()
            elif selection == 1:
                self.editMenu()
            elif selection == 2:
                self.optionsMenu()
            elif selection == 3:
                break
            
    def optionsMenu(self):
        pass

    def assignNewMenu(self):
        print("Press any midi key")
    
    def editMenu(self):
        # first layer edit menu
        options = []
        
        for id, a in enumerate(self.assignments):
            midi = a["midi"]
            raise_action = a["raise_action"]
            options.append(f"[{id}] {(str(midi['channel'])) :3} {midi['event']:8} {(str(midi['key'])):3} -> {raise_action['action']} {raise_action['layers']}")
        options.append("[b] back")
        
        menu = Menu(options,title="Choose an assignment to edit")
        result = menu.start()
        
        # in case "back" was pressed
        if result == (len(options)-1):
            return

        # second layer edit menu
        menu = Menu(options = ["[m] Change MIDI", "[a] Change action", "[d] Delete", "[b] Back"], title=options[result])
        result = menu.start()
        if result == 3:
            self.editMenu()

    def optionsMenu(self):
        options = ["[s] Select MIDI device", "[b] back"]
        menu = Menu(options=options, title="Options")
        result = menu.start()
        if result == 0:
            self.selectMidiMenu()
        elif result == (len(options)-1):
            self.mainMenu()
    
    def selectMidiMenu(self):
        options = []
        device_ids = []
        option_enum = 1
        for i in range(midi.get_count()):
            device = midi.get_device_info(i)
            if device[2] == 1:
                options.append(f"[{option_enum}] {str(device[1])[2:-1]}")
                option_enum += 1
                device_ids.append(i)
        options.append("[b] back")
        menu = Menu(options,"Select MIDI device")
        result = menu.start()
        if result == (len(options)-1):
            self.optionsMenu
        else:
            self.midi_device = midi.Input(device_ids[result])
            self.midi_device_name = options[result][4:]