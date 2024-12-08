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

Description: Script that presents system process memory

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


def percent_to_graph(percent: float, length: int=20) -> str:
    '''turns a percent 0.0 - 1.0 into a bar graph'''

    # Keep our values between desired range
    percent = max(0.0, min(1.0, percent))
    
    # Scaling foruma
    hash_num = round(percent * length)

    # Format output
    hash_bar = "#" * hash_num + " " * (length - hash_num)

    return hash_bar

def get_sys_mem() -> int:
    '''return total system memory (used or available) in kB'''
    #open file and auto close when finished
    with open("/proc/meminfo", "r") as file:
        meminfo = file.readlines()
    
    # get the first line, which is the memory total line
    memory_total = int(meminfo[0].split()[1])

    return memory_total

def get_avail_mem() -> int:
    '''return total memory that is available'''
     #open file and auto close when finished
    with open("/proc/meminfo", "r") as file:
        meminfo = file.readlines()

    # get the third line, which is the memory available line
    memory_free = int(meminfo[2].split()[1])

    return memory_free

def pids_of_prog(app_name: str) -> list:
    """Given an app name, return all PIDs associated with the app using pidof."""
    # Read all pidof, store in output
    # Convert our strings to int
    # Catch all errors exception
    # ** Modified from int -> str for check script req
    try:
        output = os.popen(f"pidof {app_name}").read().strip()
        if output:
            return list(map(str, output.split()))
        else:
            return []
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

def rss_mem_of_pid(proc_id: str) -> int:
    '''given a process id, return the resident memory used, zero if not found'''
    ## Read /proc/[PID]/status to find VmRSS
    ## Reading from status as smaps causes permissions error
    try:
        with open(f"/proc/{proc_id}/status", "r") as file:
            for line in file:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1])
    except FileNotFoundError:
        print("PID file cannot be found...")
        return 0
    return 0


def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    ## Everytime kibibyte is successfully divied by 1024
    ## Increment memory size suffix value
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

    # Unspecified PID
    if not args.program:
        # Set our variables
        total_memory = get_sys_mem()
        available_memory = get_avail_mem()
        used_memory = total_memory - available_memory

        # Calculate % memory used
        percent_memory_used = used_memory / total_memory

        # Set output for '-H' flag
        if args.human_readable:
            total_memory_str = bytes_to_human_r(total_memory)
            used_memory_str = bytes_to_human_r(used_memory)
            output = f"Memory [{percent_to_graph(percent_memory_used, args.length)} | \
                {int(percent_memory_used * 100)}%] {used_memory_str}/{total_memory_str}"
               
        else:
            output = f"Memory [{percent_to_graph(percent_memory_used, args.length)} | \
                {int(percent_memory_used * 100)}%] {used_memory}/{total_memory}"
        
        print(output)

    # Specified PID
    else:
        pids = pids_of_prog(args.program)

        if not pids:
            print(f"{args.program} not found.")
            sys.exit(1)
        
        # Set our variables
        total_memory_used = 0
        total_memory = get_sys_mem()
        for pid in pids:
            rss_memory = rss_mem_of_pid(pid)
            total_memory_used += rss_memory

            # Calculate % memory used
            percent_memory_used = rss_memory / total_memory

            # Set our formatting for '-H' flag
            if args.human_readable:
                rss_memory_str = bytes_to_human_r(rss_memory)
                total_memory_str = bytes_to_human_r(total_memory)
                print(f"{pid:<15} [{percent_to_graph(percent_memory_used, args.length)} | \
                     {int(percent_memory_used * 100)}%] {rss_memory_str}/{total_memory_str}")
            else:
                print(f"{pid:<15} [{percent_to_graph(percent_memory_used, args.length)} | \
                     {int(percent_memory_used * 100)}%] {rss_memory}/{total_memory}")
        
        # Calculate our total memory usage
        percent_total_memory_used = total_memory_used / total_memory

        # Set format for '-H' flag
        if args.human_readable:
            total_memory_used_str = bytes_to_human_r(total_memory_used)
            total_memory_str = bytes_to_human_r(total_memory)
            print(f"{args.program:<15} [{percent_to_graph(percent_total_memory_used, args.length)} | \
                 {int(percent_total_memory_used * 100)}%] {total_memory_used_str}/{total_memory_str}")
        else:
            print(f"{args.program:<15} [{percent_to_graph(percent_total_memory_used, args.length)} | \
                 {int(percent_total_memory_used * 100)}%] {total_memory_used}/{total_memory}")
