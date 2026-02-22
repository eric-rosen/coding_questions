"""
Given multiple concurrent control tasks with priorities and deadlines, design a scheduler that ensures high-priority tasks (e.g., balance recovery) always preempt lower-priority ones." — tests heaps, preemption logic, and maps directly to WBC task hierarchies.
"""
import time
from queue import PriorityQueue
import threading
from dataclasses import dataclass
from typing import Optional, Callable

@dataclass
class Task():
    target : Callable
    name : str
    stop_trigger : bool = False

    def _run_thread(self):
        while not self.stop_trigger:
            self.target()

    def start_thread(self):
        # Reset thread trigger
        self.stop_trigger = False
        # Make a thread for `target`
        self.thread = threading.Thread(target=self._run_thread, name=self.name)
        # Start the thread
        print(f" - Starting {self.thread.name}: [{time.time()}]")
        self.thread.start()
        print(f" - Started {self.thread.name}: [{time.time()}]")

    def stop_thread(self):
        # Send stop signal for _run_thread
        self.stop_trigger = True
        # Wait for self.thread to terminate
        print(f" X Stopping {self.thread.name}: [{time.time()}]")
        self.thread.join()
        print(f" X Stopped {self.thread.name}: [{time.time()}]")


## Functions representing control tasks that run forever
def task1():
    print(f"task 1: {time.time()}")
    time.sleep(0.25)

def task2():
    print(f"task 2: {time.time()}")
    time.sleep(0.25)

def task3():
    print(f"task 3: {time.time()}")
    time.sleep(0.25)

## Define initial task priorities and put them into priority queue which represents the scheduler. Lower priority number means higher priority (in accordance with python's heapq implementation)
# Each task is represented as a thread
scheduler = PriorityQueue()

def make_changes_to_scheduler():
    time.sleep(1)
    print(f"Adding task1 to scheduler!: [{time.time()}]")
    scheduler.put((3, Task(target=task1, name="task1")))
    print(f"Added task1 to scheduler!: [{time.time()}]")

    time.sleep(5)

    print(f"Adding task2 to scheduler!: [{time.time()}]")
    scheduler.put((2, Task(target=task2, name="task2")))
    print(f"Added task2 to scheduler!: [{time.time()}]")
    
    time.sleep(5)

    print(f"Adding task3 to scheduler!: [{time.time()}]")
    scheduler.put((1, Task(target=task3, name="task3")))
    print(f"Added task3 to scheduler!: [{time.time()}]")


def run_scheduler():
    # Set initial task and priority, which is nothing
    current_priority_task = [float('inf'), None]

    while True:
        # Naive approach:
        # - Get highest priority task from scheduler
        # - If it is higher priority than our current task:
        #   - Set stop signal, wait for thread to end, then add thread back to scheduler
        # - else:
        #   - Keep running current task

        # Get task from scheduler, this will wait till scheduler is not empty
        new_priority_task = scheduler.get()

        # If no current task, set this to new current task, and start it
        if current_priority_task[1] is None:
            current_priority_task = new_priority_task
            current_priority_task[1].start_thread()

        # if new task has higher priority, then stop current task, put it back in priority queue, and start new one
        elif new_priority_task[0] < current_priority_task[0]:
            # Stop current task
            current_priority_task[1].stop_thread()
            #  Re-add task to scheduler
            scheduler.put(current_priority_task)
            # Start new task
            current_priority_task = new_priority_task
            current_priority_task[1].start_thread()
        
        # if new task has equal or lower priority, just add back to queue
        else:
            scheduler.put(new_priority_task)

make_changes_to_scheduler_thread = threading.Thread(target=make_changes_to_scheduler)

make_changes_to_scheduler_thread.start()
run_scheduler()