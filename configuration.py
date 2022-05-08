import json
from menu import Menu

class configuration:
    path = None
    assignments = None
    midi_device_name = None
    midi_device = None
    def __init__(self,path="./midi2raise.json") -> None:
        self.path = path
        self.readConfig()

    def readConfig(self):
        with open(self.path,"r") as configFile:
            config = json.load(configFile)
            self.assignments = config["assignments"]
            self.midi_device_name = config["mididevice"]

    def writeConfig(self):
        # TODO: correctly save configuration
        with open(self.path,"w") as configFile:
            json.dump(self.assignments, configFile)
    
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