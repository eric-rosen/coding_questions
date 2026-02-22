"""
Given multiple concurrent control tasks with priorities and deadlines, design a scheduler that ensures high-priority tasks (e.g., balance recovery) always preempt lower-priority ones." — tests heaps, preemption logic, and maps directly to WBC task hierarchies.
"""
import time
from queue import PriorityQueue
import threading
from dataclasses import dataclass

# Global flag for determining if thread should stop
STOP_THREAD = False

## Functions representing control tasks that run forever
def task1():
    global STOP_THREAD
    while not STOP_THREAD:
        print(f"task 1: {time.time()}")
        time.sleep(1)

def task2():
    global STOP_THREAD
    while not STOP_THREAD:
        print(f"task 2: {time.time()}")
        time.sleep(1)

def task3():
    global STOP_THREAD
    while not STOP_THREAD:
        print(f"task 3: {time.time()}")
        time.sleep(1)

def start_thread(thread):
    global STOP_THREAD
    print(f"[ ] Starting {thread.name}: [{time.time()}]")
    STOP_THREAD = False
    thread.start()
    print(f"[X] {thread.name} started!: [{time.time()}]")

def stop_thread(thread):
    global STOP_THREAD
    # Will hang until the thread finishes due to STOP_THREAD signal
    print(f"[ ] Stopping {thread.name}: [{time.time()}]")
    STOP_THREAD = True
    thread.join()
    print(f"[X] Stopped {thread.name}: [{time.time()}]")

## Define initial task priorities and put them into priority queue which represents the scheduler. Lower priority number means higher priority (in accordance with python's heapq implementation)
# Each task is represented as a thread
scheduler = PriorityQueue()

def make_changes_to_scheduler():
    time.sleep(1)
    print(f"Adding task1 to scheduler!: [{time.time()}]")
    scheduler.put((3, threading.Thread(target=task1, name="task1")))
    print(f"Added task1 to scheduler!: [{time.time()}]")

    time.sleep(5)

    print("Adding task2 to scheduler!: [{time.time()}]")
    scheduler.put((2, threading.Thread(target=task2, name="task2")))
    print("Added task2 to scheduler!: [{time.time()}]")
    
    time.sleep(5)

    print("Adding task3 to scheduler!: [{time.time()}]")
    scheduler.put((1, threading.Thread(target=task3, name="task3")))
    print("Added task3 to scheduler!: [{time.time()}]")


def run_scheduler():
    global STOP_THREAD
    # Set initial task and priority, which is nothing
    current_priority_task = [0, None]

    while True:
        # Naive approach:
        # - Get highest priority task from scheduler
        # - If it is higher priority than our current task:
        #   - Set stop signal, wait for thread to end, then add thread back to scheduler
        # - else:
        #   - Keep running current task

        if scheduler.empty():
            # Nothing new to possibly schedule and nothing running, skip
            continue

        # Get task from scheduler
        new_priority_task = scheduler.get()

        # If no current task, set this to new current task, and start it
        if current_priority_task[1] is None:
            current_priority_task = new_priority_task
            start_thread(current_priority_task[1])

        # if new task has higher priority, then stop current task, put it back in priority queue, and start new one
        elif new_priority_task[0] < current_priority_task[0]:
            # Stop current task
            stop_thread(current_priority_task[1])
            #  Re-add task to scheduler
            scheduler.put(current_priority_task)
            # Start new task
            current_priority_task = new_priority_task
            start_thread(current_priority_task[1])
        
        # if new task has equal or lower priority, just add back to queue
        else:
            scheduler.put(new_priority_task)

make_changes_to_scheduler_thread = threading.Thread(target=make_changes_to_scheduler)

make_changes_to_scheduler_thread.start()
run_scheduler()