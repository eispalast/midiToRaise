import json
from random import choices
from simple_term_menu import TerminalMenu

class configuration:
    path = None
    assignments = None
    def __init__(self,path="./midi2raise.json") -> None:
        self.path = path
        self.readConfig()

    def readConfig(self):
        with open(self.path,"r") as configFile:
            self.assignments = json.load(configFile)

    def writeConfig(self):
        with open(self.path,"w") as configFile:
            json.dump(self.assignments, configFile)
    
    def mainMenu(self):
        while(True):
            options = ["[a] Assign mapping","[e] Edit/Delete mapping", "[q] Quit"]
            menu = TerminalMenu(options,title="Choose an option")
            menu_entry_index= menu.show()

            if menu_entry_index == 0:
                self.assignNewMenu()
            elif menu_entry_index == 1:
                self.editMenu()
            elif menu_entry_index == 2:
                break

    def assignNewMenu(self):
        print("Press any midi key")
    
    def editMenu(self):
        # first layer edit menu
        options = []
        
        for id, a in enumerate(self.assignments["configuration"]):
            midi = a["midi"]
            raise_action = a["raise_action"]
            options.append(f"[{id}] {(str(midi['channel'])) :3} {midi['event']:8} {(str(midi['key'])):3} -> {raise_action['action']} {raise_action['layers']}")
        options.append("[b] back")
        
        menu = TerminalMenu(options,title="Choose an assignment to edit")
        result = menu.show()
        
        # in case "back" was pressed
        if result == (len(options)-1):
            return

        # second layer edit menu
        menu = TerminalMenu(menu_entries= ["[m] Change MIDI", "[a] Change action", "[d] Delete", "[b] Back"], title=options[result])
        result = menu.show()
        if result == 3:
            self.editMenu()