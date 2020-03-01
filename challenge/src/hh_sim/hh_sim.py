#!/usr/bin/env python3
import random
import pandas as pd
import matplotlib.pyplot as plt

class HHSim:

    def __init__(self):
        random.seed(0)

    def get_pac_kw(self, times: pd.DatetimeIndex):
        return [-random.uniform(0.0, 9.0) for i in range(len(times))]

if __name__ == '__main__':
    times = pd.date_range("20190629 000000", "20190629 235959", freq="5s")
    hhsim = HHSim()
    res_arr = hhsim.get_pac_kw(times=times)
    res_df = pd.DataFrame(res_arr, columns=['Pac[kW]'], index=times)
    print(res_df)
    res_df.plot()
    plt.show()
