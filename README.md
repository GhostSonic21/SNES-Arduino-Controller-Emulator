SNES-Arduino-Controller-Emulator
=======================

Emulates a SNES Controller with an Arduino board, controlled via a python script.

Basically: Use an Arduino board as a SNES Controller on a real SNES console.

You can play the game with your keyboard (with some input lag) or try to playback a TAS if you know how to get a lagless input file.

TAS Playback script requires pySerial

Keyboard control script requires pySerial and Python for Windows Extensions, and only works for Windows at the moment.

pySeral: http://pyserial.sourceforge.net/

Windows Extensions: http://sourceforge.net/projects/pywin32/

Keyboard Bindings: WASD for directions, N for SNES Y, M for SNES B, K for SNES A, J for SNES X, Q for SNES L, R for SNES R, ENTER for SNES Start, BACKSPACE for SNES Select.

If you want to try the TAS Playback function, you need an input file with no header, no lag frames included, in a 0000RLXA rlduSsYB format (the four zeros represent buttons non-existant but still technically polled for on a real controller, and have only been demonstrated in special TAS'.) 

A lua script for the LSNES emulator that does this automatically can be found here: http://tasvideos.org/forum/viewtopic.php?p=327260#327260

I've supplied a pre-converted file for a TAS of Super Mario All-Stars: Super Mario Bros. The Lost Levels here: https://drive.google.com/file/d/0B9K--hBWxlxidzM2S294Mlh0T0E/edit?usp=sharing This should work with a regular All-Stars cartridge.

The original run was done by KFCMARIO of TASVideos, and his original publication can be seen here: http://tasvideos.org/2296M.html
