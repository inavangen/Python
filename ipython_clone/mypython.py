#!/usr/bin/env python
# encoding: utf-8
""" A basic python interface that imitates the ipython clone 
implementing feedline.py. """

import sys
import os
import re
from getchar import getchar
from feedline import *

counter = 0
length = 0
hist_list = []
out_list = []

def save_file(strin):
    """Saves history as a file.

    Args:
	   strin (string): string containing filename.
    Raises:   
	   IOError: if filename is not provided in strin.
	   IndexError: if strin doesn't start with %save

    Example usage:
    >>> save_file("%save name.txt")
    File saved.
    """

    global hist_list 

    pattern = r"\%save\s(?P<save>.*)"
    filename = re.findall(pattern, strin)
    savefile = open(filename[0], "w")
    savefile.write(str(hist_list))
    savefile.close()
    sys.stdout.write("\nFile saved.")
    return

def is_magic(strin):
    """Checks for magic commands. If there is a magic command, 
    the function operates it.

    Magic commands:
        - !: as a suffix will pass the command to the os.
        - object?: will display the docstring of object.
        - %save filename: will save history as filename.
    Args:
        strin (string): input string
    Returns:
        True: if strin contains magic command
        False: if strin does not contain magic command.

    Example usages:
    >>> is_magic("!ls")
    >>> is_magic("object?")
    >>> is_magic("%save file.txt")
    """

    if strin == "":	
        return False
    elif "!" in strin[0]:
        print ""
        os.system(strin[1:])
        return True
    elif "?" in strin[len(strin)-1]: 
        help(strin[:len(strin)-1])
        return True        
    elif strin.startswith("%save") :
        save_file(strin)
        return True
    else:
        return False    

# TODO clean up
def prompt():
    """ Asks for user input using getchar(). If enter is pressed 
    the function calls the feedline()-function with the user input. 
    If arrow up/down are used the function retrieves history information. 
    The program terminates if ctrl+d is pressed in an empty-line.

    """
    global counter
    global length

    typing = True
    line = ""
    cn = length-1

    # TODO handling ctrl+d and arrow keys could possible be
    # moved to their own functions for better readability.
    while typing:
        char = getchar()
        sys.stdout.write(char)

        # Handles CTRL+D to exit.
        if char in "\x04":
            if not line == "":
                sys.stdout.write("\nKeyboardInterupt")
                line = ""
                sys.stdout.write(feedline(line))
                typing = False              
            else: 
                print"\nKthankxbye!"
                exit(0)
        
        # Handles arrows keys and command history
        # Iterates over a history list (hist_list) with a counter (cn)
        if char in "\x1b":
            key = sys.stdin.read(2)
            sys.stdout.write("\r" + " "*(len(line)+20) + "\r" + "in [%d]: "%counter)
            # Checks if arrow up or arrow down is pressed
            if key == "[A" and len(hist_list)>0:
                line = hist_list[cn]
                sys.stdout.write(line)		
                cn -= 1
                if cn == -1: cn = length-1                
            elif key == "[B" and len(hist_list)>0:
                cn += 1
                if cn == length: cn = 0                
                line = hist_list[cn]
                sys.stdout.write(line)                    
            continue

        # Stop cycle if newline
        if char in "\r\n":

            hist_list.append(line) # save input in list
            length += 1          
            # Check for magic commands
            if is_magic(line) == True:
                output = feedline("")
                sys.stdout.write(output) #To print new promt
                out_list.append(output)
            else:
                output = feedline(line)
                sys.stdout.write(output)    
                out_list.append(output)              
            output = ""
            counter += 1
            return

        # Else, simply add char to line.
        else:   
           line += char
		  
if __name__ == "__main__":
    print "Welcome to mypython!"
    sys.stdout.write("\nin [%d]: "%counter)
    while True:
        prompt()
        

