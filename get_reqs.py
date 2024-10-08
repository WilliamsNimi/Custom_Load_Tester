import os
import concurrent.futures
import sys
import time
import datetime
import requests
from tabulate import tabulate
import numpy as np

start_time = datetime.datetime.now()
success = 0
failure = 0
reqs_comp_time = []
try:
    url = sys.argv[2]
except Exception as e:
    with open("Error_Logs/LoadTesterErrorLog.txt", 'a') as f:
        f.write(f"{datetime.datetime.now()}: {e}")
try:          
    load = sys.argv[1]
    load = int(load)
except Exception as e:
    with open("Error_Logs/LoadTesterErrorLog.txt", 'a') as f:
        f.write(f"{time.time()}: {e}")
    print("Usage: Python3 get_reqs.py *Load int value* *URL*")

def req(count):
    global success, failure, reqs_sent
    try:
        start = datetime.datetime.now()
        res = requests.get(url)
        if res:
            success = success + 1
        elif res.status_code >= 400:
            failure = failure + 1
        end = datetime.datetime.now()
        reqs_comp_time.append((end - start).total_seconds())
    except Exception as e:
        failure = failure + 1
        #Log Exception to a file
def threading():
    with concurrent.futures.ThreadPoolExecutor(max_workers = 1000) as executor:
        executor.map(req, range(load))

def display_table(success, failure):
    table = [['Success', 'Failure'], [success, failure]]
    return tabulate(table, headers='firstrow', tablefmt='fancy_grid')
        
if __name__ == "__main__":
    try:
        threading()
    except NameError:
        print("Please provide a valid load value. See Usage above")
    end_time = datetime.datetime.now()
    diff = end_time - start_time
    seconds = diff.total_seconds()
    print(f"Total Time Taken: {diff}")
    try:
        print(f"seconds/request: {sum(reqs_comp_time)/len(reqs_comp_time)}")
        print(f"requests/second: {success/seconds}")
    except Exception as e:
        print(f"seconds/request: 0")
        with open("Error_Logs/LoadTesterErrorLog.txt", 'a') as f:
            f.write(f"{datetime.datetime.now()}: {e}")
    print(display_table(success, failure))
    print(f"Minimum Request completion time: {min(reqs_comp_time)}")
    print(f"Maximum Request completion time: {max(reqs_comp_time)}")
    print(f"95th percentile completion time: {np.percentile(np.array(reqs_comp_time), 95)}")
