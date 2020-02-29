# EinsMan Challenge

Author: Alexander Prostejovsky


## General Information
This script replicates the plots from the challenge description using the
following assumptions:
- Avacon Netz interfaces with Tennet and 50Hertz, hence asset and
grid management data of these three network operators are considered.
- Of the different feed management causes only 'Netzengpass' and
'Vorgelagerter Netzbetreiber', as they can be directly attributed to
actual operational grid events. This is an arbitrary assumption for example's 
sake.
- Events without an asset key ("Anlagenschlüssel") are discarded because their
assotiated installed power ("Installierte Leistung") cannot be determined.
- The year 2018 is supported for evaluation in this script.

In addition, an additional plot is generated the shows a detailed view
of a selected date range.

By default, the month of August 2018 is considered, but the date range can be 
customised if desired.


## Requirements
Python >= 3.6 must be present on the host system.

The following packages will be automatically installed on running the script:
- pandas==0.25.1
- matplotlib==3.1.1
- dataclasses==0.6
- typing==3.7.4.1


## How to Run
### Quick start
Simply execute `./run.sh` in the project root.
It checks the system's Python version, creates a virtual environment,
installs required packages, and runs the challenge programme with default
parameters.


### Command Line Options
It is possible to pass command line parameters to the script for... 
- Customising the start/end date and time of both the total date range and 
the detailed view;
- Choosing whether data should be downloaded. This is useful if the script 
is run repeatedly with the same data.

Execute the script with the command line option `-h` for a detailed 
description of available parameters.
