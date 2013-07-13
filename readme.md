# Serial to Xively Bridge #

This simple program runs on a PC to allow Arduinos or other embedded devices to read and write Xively feed data. e.g.

Embedded device -> Serial -> PC running serial-xively-bridge -> Network -> Xively

## Dependancies ##
These python libraries need to be installed:

* pyserial
* xively-python

## Setup ##

Create a file called 'api.txt' in this directory. Past your Xively device API key in the file on the first line and save.

## Usage ##

When the program is first run you can select from a list of serial ports or the console as in the input device.

    Select serial port to open:
    0: /dev/tty.Bluetooth-PDA-Sync
    1: /dev/tty.Bluetooth-Modem
    2: /dev/tty.usbserial-A1017KVR
    3: Console input
    
Select a port and then the program will start waiting for input

### Writing data ###

The command to write to a feed is

    write:FEEDID,DATASTREAMID:DATASTREAMVALUE,DATASTREAMID:DATASTREAMVALUE, ...
    
e.g.

    write:135647615,Temperature:25,Pressure:1014,Humidity:76
    
Not all the datastreams are required to be in the command. Commands are followed by EOL character.

### Reading data ###

The command to read the latest value of a feed is

    read:FEEDID
    
which will return 

    DATASTREAMID:DATASTREAMVALUE,DATASTREAMID:DATASTREAMVALUE, ...
    
e.g. 

    read:135647615
    
returns

    Temperature:25,Pressure:1014,Humidity:76
