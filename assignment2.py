#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: Mitchell Gregoris
Semester: Fall 2024

The python code in this file is original work written by
Mitch Gregoris. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: <Enter your documentation here>

'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("-H", "--human-readable", action="store_true", help="Prints the sizes in human readable format")
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use is not.")
    args = parser.parse_args()
    return args
 
# create argparse function
# -H human readable
# -r running only

def get_system_memory():
    '''Get all current system memory'''
    #open file and auto close when finished
    with open("/proc/meminfo", "r") as file:
        meminfo = file.readlines()

    # get total and available memory
    memory_total = int(meminfo[0].split()[1])  # First line is MemTotal
    memory_free = int(meminfo[2].split()[1])  # Third line is MemAvailable

    # memory calculation
    memory_used = memory_total - memory_free

    return memory_used, memory_total

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"
    ...
# percent to graph function

def get_sys_mem() -> int:
    "return total system memory (used or available) in kB"
    #open file and auto close when finished
    with open("/proc/meminfo", "r") as file:
        meminfo = file.readlines()
    
    # get the first line, which is the memory total line
    memory_total = int(meminfo[0].split()[1])

    return memory_total

def get_avail_mem() -> int:
    "return total memory that is available"
     #open file and auto close when finished
    with open("/proc/meminfo", "r") as file:
        meminfo = file.readlines()

    # get the third line, which is the memory available line
    memory_free = int(meminfo[2].split()[1])  # Third line is MemAvailable

    return memory_free

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    ...

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    ...

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:
        ...
    else:
        ...
    # process args
    # if no parameter passed, 
    # open meminfo.
    # get used memory
    # get total memory
    # call percent to graph
    # print

    # if a parameter passed:
    # get pids from pidof
    # lookup each process id in /proc
    # read memory used
    # add to total used
    # percent to graph
    # take total our of total system memory? or total used memory? total used memory.
    # percent to graph.
