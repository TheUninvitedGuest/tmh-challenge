#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from broker.broker import Publisher


class HHSim:
    """ Simple household simulator that generates random uniform numbers between -9 and 0 for a given time range.
        The output corresponds to the household consumption in kilowatts, loads are assumed to have negative values."""
    publisher: Publisher
    times: pd.DatetimeIndex

    def __init__(self, start_time, end_time, freq):
        np.random.seed(0)
        self.times = pd.date_range(start_time, end_time, freq=freq)
        self.publisher = Publisher()

    def run(self):
        self._send_meter_data()

    def _get_pac_kw(self):
        return -np.random.uniform(0.0, 9.0)

    def _send_meter_data(self):
        for timestamp in self.times:
            self.publisher.send_data(timestamp=timestamp, power=self._get_pac_kw())
        self.publisher.send_ctrl("done")
        self.publisher.close()


if __name__ == '__main__':
    hhsim = HHSim("20190629 000000", "20190629 000100", freq="5s")
    res_arr = [hhsim._get_pac_kw() for _ in hhsim.times]
    res_df = pd.DataFrame(res_arr, columns=['Pac[kW]'], index=hhsim.times)
    print(res_df)
    res_df.plot()
    plt.show()
