import time
from collections import deque
import heapq

class Process:
    def __init__(self, pid, burst_time, priority=1, arrival_time=0):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.arrival_time = arrival_time
        self.start_time = None
        self.completion_time = None

def round_robin(processes, quantum):
    print("\n--- Round-Robin Scheduling ---")
    queue = deque(sorted(processes, key=lambda x: x.arrival_time))
    current_time = 0

    while queue:
        process = queue.popleft()
        if process.start_time is None:
            process.start_time = current_time

        exec_time = min(process.remaining_time, quantum)
        print(f"Time {current_time}: Running Process {process.pid} for {exec_time} units")
        time.sleep(0.2)
        current_time += exec_time
        process.remaining_time -= exec_time

        if process.remaining_time > 0:
            queue.append(process)
        else:
            process.completion_time = current_time
            print(f"Process {process.pid} completed at time {current_time}")

    print("\nRound-Robin Metrics:")
    calculate_metrics(processes)

def priority_scheduling(processes):
    print("\n--- Priority-Based Scheduling ---")
    current_time = 0
    ready_queue = []
    processes = sorted(processes, key=lambda x: x.arrival_time)
    incoming = processes.copy()

    while incoming or ready_queue:
        while incoming and incoming[0].arrival_time <= current_time:
            p = incoming.pop(0)
            heapq.heappush(ready_queue, (p.priority, p.arrival_time, p))

        if not ready_queue:
            current_time += 1
            continue

        _, _, process = heapq.heappop(ready_queue)

        if process.start_time is None:
            process.start_time = current_time

        print(f"Time {current_time}: Running Process {process.pid} (Priority {process.priority})")
        time.sleep(0.2)

        next_arrival = incoming[0].arrival_time if incoming else float('inf')
        exec_time = min(process.remaining_time, next_arrival - current_time)

        if exec_time <= 0:
            exec_time = process.remaining_time

        process.remaining_time -= exec_time
        current_time += exec_time

        if process.remaining_time > 0:
            heapq.heappush(ready_queue, (process.priority, process.arrival_time, process))
        else:
            process.completion_time = current_time
            print(f"Process {process.pid} completed at time {current_time}")

    print("\nPriority-Based Metrics:")
    calculate_metrics(processes)

def calculate_metrics(processes):
    print("PID\tWT\tTAT\tRT")
    for p in processes:
        tat = p.completion_time - p.arrival_time
        wt = tat - p.burst_time
        rt = p.start_time - p.arrival_time
        print(f"{p.pid}\t{wt}\t{tat}\t{rt}")

if __name__ == "__main__":
    base_processes = [
        Process(1, 5, 2, 0),
        Process(2, 3, 1, 1),
        Process(3, 8, 3, 2),
        Process(4, 6, 2, 3),
    ]

    rr_processes = [Process(p.pid, p.burst_time, p.priority, p.arrival_time) for p in base_processes]
    round_robin(rr_processes, quantum=2)

    pb_processes = [Process(p.pid, p.burst_time, p.priority, p.arrival_time) for p in base_processes]
    priority_scheduling(pb_processes)
