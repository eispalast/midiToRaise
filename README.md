midiToRaise
===========
An easy way to switch layers on you Dygma Raise using MIDI.
You can activate and deactivate layers or cycle through multiple layers.

_The program is not yet finished, see disclaimer below._

Requirements
------------
Following python packages are necessary:

    pyserial
    pygame
    getkey

On some systems the official getkey package doesn't work. In the [requirements](requirements) file you can find a fork that should work. 
You can install all requirements at once using pip, e.g. like this:

    python3 -m pip install -r requirements

Start
-----
Run with python:

    python3 midiToRaise.py

When you start the program for the first time, there is no MIDI input device set yet. The menu will show a corresponding message. Use the arrow keys to navigate to `options` or press `o` while in the main menu.
Go to `select MIDI device` or press `s`, and select the device you want to use.

You should now be back in the main menu where you can go to `Assign mapping` (shortcut `a`). You then have 2 seconds to press a MIDI button (Note On/Off or Program Change). After 2 seconds the menu shows the received MIDI events. (_Disclaimer: This process is still a bit buggy. If the event wasn't properly received, just try again after pressing cancel_).

Select the MIDI event you want to assign. In the next menu you can select which action is connected to the MIDI event. A good practice is to assign an `activate layer` on a MIDI Note On event and the corresponding `deactivate layer` on the Note Off event for the same note (in fact, when you assign a active layer to a Note On event, the program asks you if it should automatically assign the corresponding `deactivate` action. I suggest you do so). 

If you instead choose to assign the MIDI event to a `moveTo` action, you can select multiple layers to cycle through when you press the MIDI note multiple times. You can however select only one layer so that the same MIDI event always takes you to one specific layer. 

All assignments and the MIDI device's name are stored in the file [midi2raise.json](midi2raise.json). You can edit them there manually or backup this file or use it on multiple machines.


Disclaimer
----------
The program is not in its final state, but the main functionality is there. The `Edit/Delete mapping` menu is not working yet. If you want to delete or edit a mapping, you have to do it manually in the [midi2raise.json](midi2raise.json) file.

Troubleshooting
---------------
Midi cannot be started on Linux with a message like this: 

    ALSA lib conf.c:3558:(snd_config_hooks_call) Cannot open shared library libasound_module_conf_pulse.so (/usr/lib/alsa-lib/libasound_module_conf_pulse.so: libasound_module_conf_pulse.so: cannot open shared object file: No such file or directory)
    ALSA lib seq.c:935:(snd_seq_open_noupdate) Unknown SEQ default

copy the files the correct directory.
You might have to create that directory first.

    mkdir /usr/lib/alsa-lib

    cp /usr/lib/x86_64-linux-gnu/alsa-lib/libasound_module_conf_pulse.so
    /usr/lib/alsa-lib/libasound_module_conf_pulse.so
