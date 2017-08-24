"""Commands used to control the RC car"""
import json
import socket

from common import server_up




keys = {0:"forward", 1:"forward_left", 2:"forward_right", 3:"reverse",
                4:"reverse_left", 5:"reverse_right", 6:"idle", 7:"right", 8:"left"}
#signal repeats list:
#Forward: 21
#Left: 126
#Right: 114
#LeftForward: 67
#RightForward: 56
#Reverse: 78
#LeftReverse: 92
#RightReverse: 102
#Return a dictionary with all the commands in it
def file_to_commands(configuration_file):
    configuration = json.loads(configuration_file.read())
    #raspberry pi has to send signal continously.
    #Instead of stopping the signal, send it with another frequency.
    #since my car is 26.995 Mhz, the dead freq will be 49
    dead_freq = 49
    sync_command = {
        'frequency': configuration['frequency'],
        'dead_frequency': dead_freq,
        'burst_us': configuration['synchronization_burst_us'],
        'spacing_us': configuration['synchronization_spacing_us'],
        'repeats': configuration['total_synchronizations'],
    }
    base_command = {
        'frequency': configuration['frequency'],
        'dead_frequency': dead_freq,
        'burst_us': configuration['signal_burst_us'],
        'spacing_us': configuration['signal_spacing_us'],
    }

    signal_command = {}
    #loop through the js object signal repeats list
    for key in ("forward", "forward_left", "forward_right", "left",
                "reverse","reverse_left", "reverse_right", "right"):
        #create a temporary dictionary to store the base command and the #repeats for different
        temp = base_command.copy()
        temp['repeats'] = configuration[key]
        signal_command[key] = temp

    #creating the direct command dictionary with the sync command
    direct_commands = {
        key: json.dumps([sync_command, signal_command[key]])
        for key in signal_command
    }
    #add the idle command
    temp = base_command.copy()
    temp['frequency'] = dead_freq
    temp['repeats'] = 4
    direct_commands['idle'] = json.dumps([temp])
    
    return direct_commands
    
def control(host, port, commands, com):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(commands[com], (host, port))
    except TypeError:
        sock.sendto(bytes(commands[com], 'utf-8'), (host,port))
        
def simpleControl(com):
    read_file = open("red-lamborghini.json")
    commands = file_to_commands(read_file)
    control('192.168.2.7', 12345, commands, keys[com])
    
def main():
    read_file = open("red-lamborghini.json")
    commands = file_to_commands(read_file)
    server = str(input("enter server:"))
    port = 12345
    keys = {0:"forward", 1:"forward_left", 2:"forward_right", 3:"reverse",
                4:"reverse_left", 5:"reverse_right", 6:"idle", 7:"right", 8:"left"}
    print(keys)
    while(True):
        com = int(input("enter command through number:"))
        control(server, port, commands, keys[com])
if __name__ == "__main__":
    main()

    









