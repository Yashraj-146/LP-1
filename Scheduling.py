from collections import deque

class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining_burst = burst
        self.priority = priority
        self.completion = 0
        self.turnaround = 0
        self.waiting = 0

def fcfs(processes):
    processes.sort(key=lambda x: x.arrival)
    time = 0
    for p in processes:
        if time < p.arrival:
            time = p.arrival
        p.completion = time + p.burst
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.burst
        time = p.completion

def sjf_preemptive(processes):
    processes.sort(key=lambda x: (x.arrival, x.burst))
    time = 0
    ready_queue = []
    completed = 0
    while completed < len(processes):
        for p in processes:
            if p.arrival <= time and p.remaining_burst > 0 and p not in ready_queue:
                ready_queue.append(p)
        ready_queue.sort(key=lambda x: x.remaining_burst)
        if ready_queue:
            current = ready_queue.pop(0)
            time += 1
            current.remaining_burst -= 1
            if current.remaining_burst == 0:
                current.completion = time
                current.turnaround = current.completion - current.arrival
                current.waiting = current.turnaround - current.burst
                completed += 1
        else:
            time += 1

def priority_non_preemptive(processes):
    processes.sort(key=lambda x: (x.arrival, x.priority))
    time = 0
    for p in processes:
        if time < p.arrival:
            time = p.arrival
        p.completion = time + p.burst
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.burst
        time = p.completion

def round_robin(processes, quantum):
    queue = deque(processes)
    time = 0
    while queue:
        process = queue.popleft()
        if time < process.arrival:
            time = process.arrival
        if process.remaining_burst > quantum:
            time += quantum
            process.remaining_burst -= quantum
            queue.append(process)
        else:
            time += process.remaining_burst
            process.remaining_burst = 0
            process.completion = time
            process.turnaround = process.completion - process.arrival
            process.waiting = process.turnaround - process.burst

def print_results(processes, algorithm_name):
    print(f"\n{algorithm_name} Results")
    print("PID\tArrival\tBurst\tCompletion\tTurnaround\tWaiting")
    for p in processes:
        print(f"{p.pid}\t{p.arrival}\t{p.burst}\t{p.completion}\t\t{p.turnaround}\t\t{p.waiting}")

# Sample Processes
processes = [
    Process(pid=1, arrival=0, burst=8, priority=3),
    Process(pid=2, arrival=1, burst=4, priority=1),
    Process(pid=3, arrival=2, burst=9, priority=2),
    Process(pid=4, arrival=3, burst=5, priority=4)
]

# FCFS
fcfs_processes = [Process(p.pid, p.arrival, p.burst) for p in processes]
fcfs(fcfs_processes)
print_results(fcfs_processes, "FCFS")

# SJF (Preemptive)
sjf_processes = [Process(p.pid, p.arrival, p.burst) for p in processes]
sjf_preemptive(sjf_processes)
print_results(sjf_processes, "SJF (Preemptive)")

# Priority (Non-Preemptive)
priority_processes = [Process(p.pid, p.arrival, p.burst, p.priority) for p in processes]
priority_non_preemptive(priority_processes)
print_results(priority_processes, "Priority (Non-Preemptive)")

# Round Robin (Preemptive)
rr_processes = [Process(p.pid, p.arrival, p.burst) for p in processes]
quantum = 3
round_robin(rr_processes, quantum)
print_results(rr_processes, "Round Robin (Preemptive)")