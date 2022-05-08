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
