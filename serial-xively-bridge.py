import xively
import datetime
import sys
import time
import os
import re
from serial.tools import list_ports
import serial

BAUD_RATE = 57600

def main():
    with open('api.txt') as f:
        apiKey = f.readline().strip()
    api = xively.XivelyAPIClient(apiKey)
    
    print('Select serial port to open:')
    ports = list_serial_ports()
    
    numPorts = len(ports)
    for i in range(numPorts):
        print "{}: {}".format(i, ports[i])
    print "{}: Console input".format(numPorts)
    cmd = int(raw_input())
    
    usingConsole = False
    if cmd < numPorts:
        print "Opening {}".format(ports[cmd])
        comms = serial.Serial(ports[cmd], BAUD_RATE)
    else:
        comms = sys.stdin
        usingConsole = True
    
    #Loop to process commands
    while True:
        print('Waiting for command')
        msg = comms.readline()
        #print msg
        
        str = re.split('\n|,|\r| ',msg)
        now = datetime.datetime.utcnow()
        
        # Write to the feed
        cmd = re.split(':',str[0])
        if cmd[0] == 'write':
            try:
                feed = api.feeds.get(cmd[1])
            except Exception as e:
                print "Error getting feed information"
                print e
                continue
            
            dstreams = []
            try:
                for item in str[1:]:
                    if item != '':
                        cmd = re.split(':',item)
                        dstreams.append(xively.Datastream(id=cmd[0], current_value=cmd[1],at=now))
            except Exception as e:
                print "Error parsing command, {}".format(msg)
                print e
                continue
            
            try:
                feed.datastreams = dstreams
                feed.update()
            except Exception as e:
                print "Error writing to feed"
                print e
                continue
            
    
            for item in feed.datastreams:
                print "Wrote: {}  {}:{}".format(item.at,item.id,item.current_value)
        
        #Read from the feed
        elif cmd[0] == 'read':
            try:
                feed = api.feeds.get(cmd[1])
            except Exception as e:
                print "Error getting feed information"
                print e
                continue
                
            output = ["{}:{}".format(x.id,x.current_value) for x in feed.datastreams]
            
            if usingConsole:
                print ",".join(output)
            else:
                comms.write(",".join(output))
                comms.write("\r\n")
                print ",".join(output)
                
        elif cmd[0] == 'quit':
            break
            

def list_serial_ports():
    # Windows
    if os.name == 'nt':
        # Scan for available ports.
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append('COM'+str(i + 1))
                s.close()
            except serial.SerialException:
                pass
        return available
    else:
        # Mac / Linux
        return [port[0] for port in list_ports.comports()]


if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        main(*args)
    except KeyboardInterrupt:
        pass
