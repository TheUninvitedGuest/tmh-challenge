#!/usr/bin/env python3

import multiprocessing

from hh_sim.hh_sim import HHSim
from pv_sim.pv_sim import PVSim

# Simulation time range and sampling intervals
START_DATETIME = "2019.06.29 00:00:00"
END_DATETIME = "2019.06.29 23:59:59"
SAMPLING_ITVL = "600s"


class Problem:
    """ Here we start up our simulation workers. Both the household simulator (HH) and PV simulator (PV) are running in
        seperated processes to demonstrate real-world applicability within a distributed environment."""

    hhsim: HHSim
    pvsim: PVSim
    jobs: []

    def __init__(self):
        self.hhsim = HHSim(START_DATETIME, END_DATETIME, freq=SAMPLING_ITVL)
        self.pvsim = PVSim()
        self.jobs = []

    def run(self):
        self.jobs.append(multiprocessing.Process(target=self.pvsim.run))
        self.jobs.append(multiprocessing.Process(target=self.hhsim.run))
        for job in self.jobs:
            job.start()


if __name__ == '__main__':
    problem = Problem()
    problem.run()
