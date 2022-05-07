import json
from random import choices
from numpy import integer
from simple_term_menu import TerminalMenu
from soupsieve import select
from sympy import im
from menu import Menu

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
            options = ["[0] Assign mapping","[1] Edit/Delete mapping", "[2] Quit"]
            print("Choose an option")
            main_menu = Menu(options=options,title="What do you want to do?")
            selection = main_menu.start()
            # menu = TerminalMenu(options,title="Choose an option")
            # menu_entry_index= menu.show()

            if selection == 0:
                self.assignNewMenu()
            elif selection == 1:
                self.editMenu()
            elif selection == 2:
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