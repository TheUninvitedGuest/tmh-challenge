#!/usr/bin/env python3
import pandas as pd
from pandas import plotting
import matplotlib.pyplot as plt

from hh_sim.hh_sim import HHSim
from pv_sim.pv_sim import PVSim


START_DATETIME = "2019-06-29 00:00:00"
END_DATETIME = "2019-06-29 23:59:59"
SAMPLING_ITVL = "60s"


class Problem:
    hhsim: HHSim
    pvsim: PVSim
    times: pd.DatetimeIndex

    def __init__(self):
        self.hhsim = HHSim()
        self.pvsim = PVSim()
        self.times = pd.date_range(START_DATETIME, END_DATETIME, freq=SAMPLING_ITVL)

    def run(self):
        df = pd.DataFrame(index=self.times)
        df['PV'] = self.pvsim.get_pac_kw(self.times)
        df['HH'] = self.hhsim.get_pac_kw(self.times)
        df['Sum'] = df['PV'] + df['HH']
        print(df)
        df.plot()
        plt.show()

if __name__ == '__main__':
    problem = Problem()
    problem.run()