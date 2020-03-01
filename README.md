# PV Simulator Challenge

Author: Alexander Prostejovsky


## Preamble
Please read ahead to learn why the programme executes rather slowly!
(Spoiler alert: It's the external module for simulating the PV power yield.)

## General Information
This programme solves the task at hand using the following elements:
- A household data simulator based on a random number generator for uniformly distributed
continuous values;
- A PV simulator using the `pvlib` module, which takes various parameters (such as location,
orientation, and nominal power of the PV array) as inputs and calculates the power yield
at a given time and date for this location.
- A dedicated broker using `pika`, Python's native RabbitMQ client, which is used by the 
 household and PV simulators to exchange data in a publish/subscribe messaging scheme. 

Each simulator runs in a dedicated process to highlight the abstraction between the
simulated entities (household/meter, PV).
The PV simulator assumes a 4 kWpeak panel located at TMH's Munich site.

As specified by the challenge description, the PV simulator is also responsible for
receiving and processing the meter readings from the household simulator, and writing the
results to the disk.

By default, the whole day of 29 June 2019 is simulated in 60s intervals. 
Both the date range and the simulation intervals can be customised if desired.


## Requirements
The script was developed on Kubuntu 19.10 using Python 3.7.5.
Presumably the script works on Python >= 3.6, but this could not be tested.

The following packages will be automatically installed on running the accompanying Bash script:
- matplotlib==3.1.3
- pvlib==0.7.1
- pika==1.1.0
- numpy==1.18.1
- pandas==1.0.1
- tables==3.6.1

A RabbitMQ server must be present on localhost and reachable via its default port `5672`
for message queues.

## How to Run
Simply execute `./run.sh` in the project root.
The script checks the system's Python version, creates a virtual environment,
installs required packages, and runs the challenge programme.

The numerical results along with a graphical plot are stored 
in `project_root/challenge/results/`.