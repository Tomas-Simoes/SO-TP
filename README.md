# Scheduling-Simulator

A Python-based CPU scheduling simulator designed to model and analyze various scheduling algorithms. This tool is ideal for educational purposes, allowing users to visualize and compare the behavior of different scheduling strategies.

## Features

- **Multiple Scheduling Algorithms**: Simulate and compare FCFS, SJF, Round Robin, and Priority (and others) scheduling algorithms.
- **Process Visualization**: Graphical representation of process execution timelines.
- **Configurable Inputs**: Customize process parameters like arrival time, burst time, and priority.
- **Performance Metrics**: Calculate metrics such as average waiting time, turnaround time, and CPU utilization.

## Installation

### Prerequisites

- Python 3.8 or higher
- `pip` package manager

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Tomas-Simoes/Scheduling-Simulator.git
   cd Scheduling-Simulator
   ```
2. **Install Dependencies**

  ```bash
  pip install -r requirements.txt
  ```

## Usage

1. **Simulation Configurations**  
   There are several configurations you can edit to define your scheduling scenario. These are specified in the `config.json` file.

   **Available fields:**

   - `processes`: A list of process objects with:
     - `pid`: Process ID (unique identifier)
     - `arrival_time`: Time at which the process arrives
     - `burst_time`: Time required by the process to execute
     - `priority`: (Optional) Used for priority scheduling
   - `algorithm`: The scheduling algorithm to be used (`FCFS`, `SJF`, `RR`, `PRIORITY`)
   - `time_quantum`: (Optional) Required for Round Robin

   **Example `config.json`:**

   ```json
   {
     "processes": [
       {"pid": 1, "arrival_time": 0, "burst_time": 5, "priority": 2},
       {"pid": 2, "arrival_time": 2, "burst_time": 3, "priority": 1}
     ],
     "algorithm": "RR",
     "time_quantum": 4
   }
   ```
2. **Run the simulator**
  ```
  python src/main.py
  ```

## Project Structure  
```
├── src/ 
│   ├── main.py             # Entry point of the simulator
│   ├── scheduler.py        # Core logic for each algorithm
│   ├── process.py          # Process class and helpers
│   └── utils.py            # Metrics, input parsing, etc.
├── config.json             # User configuration file
```
## Acknowledgments

This project was carried out as part of the Operating Systems subject during my studies at Universidade da Beira Interior.
