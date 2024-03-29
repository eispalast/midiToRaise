import json
import time
from tracemalloc import start
from menu import Menu
from pygame import midi as midi

MIDIEVENTS_I2S = {0x8:"Note Off", 0x9:"Note On", 0xC:"PC"}
MIDIEVENTS_S2I = {"Note Off":0x8, "Note On":0x9, "PC":0xC}

ACTION_I2S = {0:"activate",1:"deactivate",2:"moveTo"}
ACTION_S2I = {"activate":0,"deactivate":1,"moveTo":2}
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
        self.config_wait_for_midi_timeout = 2
    
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
            if self.midi_device_name == str(device[1])[2:-1] and device[2] == 1:
                self.midi_device = midi.Input(i)

    def readConfig(self):
        try:
            with open(self.path,"r") as configFile:
                self.config = json.load(configFile)
                self.assignments = self.config["assignments"]
                self.midiStr2int()
                self.midi_device_name = self.config["mididevice"]
        except:
            with open(self.path,"w") as configFile:
                self.config = {"mididevice":"","assignments":[]}
                self.assignments = self.config["assignments"]
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

    def selectMIDIinput(self):
        print("Press any midi key")
        starttime = time.time()
        midiinputs = []
        while time.time()-starttime < self.config_wait_for_midi_timeout:
            if midi.Input.poll(self.midi_device):
                ins = midi.Input.read(self.midi_device,3)
                for i in ins:
                    midiinputs.append(i[0])
        print(midiinputs)
        options = []
        translated_inputs = []
        id = 0
        for m in midiinputs:
            channel = m[0] & 0xF
            event = MIDIEVENTS_I2S[m[0]>>4]
            key = m[1]
            option_string = f"Ch. {channel} {event} on {key}" 
            
            for op in options:
                if option_string in op:
                    break
            else:
                options.append(f"[{id}] {option_string}")
                translated_inputs.append([channel,event,key])
                id += 1
        options.append("[c] cancel")
        menu = Menu(options,"Select a MIDI event")
        result = menu.start()
        if result == (len(options)-1):
            return None
        
        return translated_inputs[result]
    
    def selectLayerAction(self, midiinput = "this midi input"):
        action_options = ["[a] activate layer", "[d] deactivate layer", "[m] moveTo layer", "[c] cancel"]
        menu = Menu(action_options, f"Select an action for {midiinput}")
        action_result = menu.start()
        if action_result == (len(action_options)-1):
            return None

        layer_options = list([f"[{x}] Layer {x}" for x in range(10)])
        layer_results = []
        while True:
            menu = Menu(layer_options,"Chose a corresponding layer")
            layer_results.append(menu.start())
            if action_result != 2:
                break
            menu = Menu(["[y] yes", "[n] no"],"Do you want to add more layers to cycle through?")
            more_result = menu.start()
            if more_result == 1:
                break
        
        return [action_result,layer_results]
        
# return True when assignment was successful
    def assignNewMenu(self, midiinput = None, action = None, overwrite = False):
        if midiinput == None:
            midiinput = self.selectMIDIinput()
            if midiinput == None:
                return False
        if action == None:
            action = self.selectLayerAction(midiinput=midiinput)
            if action == None:
                return False
        
        self.assignments.append({"midi":{"channel":midiinput[0],"event":MIDIEVENTS_S2I[midiinput[1]],"key":midiinput[2]},"raise_action":{"action":ACTION_I2S[action[0]],"layers":action[1]}})

        if not overwrite:
            # in case it was a note on event and the action was activate, offer to automatically configure the deactivate function
            if midiinput[1] == 'Note On' and action[0] == 0:
                menu = Menu(["[y] yes", "[n] no"], "Do you want to automatically assign the corresponding deactivate layer action?")
                result = menu.start()
                if result == 0:
                    self.assignments.append({"midi":{"channel":midiinput[0],"event":8,"key":midiinput[2]},"raise_action":{"action":ACTION_I2S[1],"layers":action[1]}})
        
        self.writeConfig()
        return True
    
    def deleteBinding(self, id):
        self.assignments.pop(id)
        self.writeConfig()
    
    def editMenu(self):
        # first layer edit menu
        options = []
        
        for id, a in enumerate(self.assignments):
            midi = a["midi"]
            raise_action = a["raise_action"]
            options.append(f"[{id}] {(str(midi['channel'])) :3} {MIDIEVENTS_I2S[midi['event']]:8} {(str(midi['key'])):3} -> {raise_action['action']} {raise_action['layers']}")
        options.append("[b] back")
        
        menu = Menu(options,title="Choose an assignment to edit")
        assignment_id = menu.start()
        
        # in case "back" was pressed
        if assignment_id == (len(options)-1):
            return
        # second layer edit menu
        menu = Menu(options = ["[m] Change MIDI", "[a] Change action", "[d] Delete", "[b] Back"], title=options[assignment_id])
        result = menu.start()
        if result == 0:
            action = self.assignments[assignment_id]['raise_action']
            action = [ACTION_S2I[action['action']],action['layers']]
            if self.assignNewMenu(action=action,overwrite=True):
                self.deleteBinding(assignment_id)
        if result == 1:
            # brauche Darstellung [channel(int), "midiaction(Note On...",key(int)]
            midi = self.assignments[assignment_id]['midi']
            midi = [midi['channel'],MIDIEVENTS_I2S[midi['event']],midi['key']]
            if self.assignNewMenu(midiinput=midi,overwrite=True):
                self.deleteBinding(assignment_id)
        if result == 2:
            self.deleteBinding(assignment_id)
        if result == 3:
            self.editMenu()

    def optionsMenu(self):
        options = ["[s] Select MIDI device", "[b] back"]
        menu = Menu(options=options, title="Options")
        result = menu.start()
        if result == 0:
            self.selectMidiDeviceMenu()
        elif result == (len(options)-1):
            self.mainMenu()
    
    def selectMidiDeviceMenu(self):
        self.midi_device = None
        midi.quit()
        midi.init()
        options = []
        device_ids = []
        option_enum = 1
        device_list = []
        for i in range(midi.get_count()):
            device = midi.get_device_info(i)
            device_list.append(device)
            if device[2] == 1:
                options.append(f"[{option_enum}] {str(device[1])[2:-1]}")
                option_enum += 1
                device_ids.append(i)
        options.append("[b] back")
        menu = Menu(options,"Select MIDI device")
        midi_device_result = menu.start()
        if midi_device_result == (len(options)-1):
            self.optionsMenu
        else:
            self.midi_device = midi.Input(device_ids[midi_device_result])
            self.midi_device_name = options[midi_device_result][4:]