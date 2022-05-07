from turtle import color
from getkey import getkey, keys
import os
from colors import colors
from time import sleep



class Menu():
    options = []
    title = ""
    current_selection = 0
    shortcuts = []
    def __init__(self,options,title) -> None:
        self.options = options
        self.title = title
        self.parse_shortcuts()
    

    def parse_shortcuts(self):
        shortcuts_temp = []
        options_temp = []
        for o in self.options:
            o=o.lstrip()
            try:
                if o[0] == "[" and o[2] == "]":
                    shortcuts_temp.append(o[1])
                    options_temp.append((o[3:]).lstrip())
                else:
                    return
            except:
                return
        self.shortcuts = shortcuts_temp
        self.options = options_temp
    def start(self):
        while(True):
            os.system("clear")
            print(self.title)
            menu_string = ""
            for id,o in enumerate(self.options):
                if id == self.current_selection:
                    color = colors.fg_black+colors.bg_lightgrey
                else:
                    color = colors.reset
                
                sc_string = ""
                if len(self.shortcuts) > 0:
                    sc_string = f"{color}[{colors.fg_cyan}{self.shortcuts[id]}{color}] "
                
                menu_string += (f"  {color}{sc_string}{color}{o}{colors.reset}\n")
            print(menu_string)
            pressedkey = getkey()
            if pressedkey == keys.UP:
                self.current_selection = max(self.current_selection-1,0)
            elif pressedkey == keys.DOWN:
                self.current_selection = min(self.current_selection+1,len(self.options)-1)
            elif pressedkey == keys.ENTER:
                os.system("clear")
                return self.current_selection
            elif pressedkey in self.shortcuts:
                os.system("clear")
                return self.shortcuts.index(pressedkey)

            

 

# if __name__ == "__main__":
#     o = ["[2] zweite Option"," [e] erste","[v] vierte"]
#     men= menu(o,"wähle")
#     choice = men.start()
#     print(choice)