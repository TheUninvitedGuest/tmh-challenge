#!/usr/bin/env python3

import pandas as pd
from pandas import DataFrame
import os
import matplotlib.pyplot as plt
from pvlib.pvsystem import PVSystem
from pvlib.location import Location
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
from broker.broker import Subscriber
from logger.logger import Logger


_PARENT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_RESULTS_DIR_PATH = _PARENT_DIR_PATH + '/../results/'
_LOG_FILENAME = 'thm_challenge.csv'
_LOG_FILEPATH = _RESULTS_DIR_PATH + _LOG_FILENAME

_TEMP_MODEL_PARAMS = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

# Parameters of the simulated PV panel
_PV_SYS_CONFIG = {
    'location': 'TMH Munich',
    'latitude': 48.120872,
    'longitude': 11.602498,
    'timezone': 'Etc/GMT-1',
    'surface_tilt': 55,
    'surface_azimuth': 190,
    'pdc0': 4e3,
    'gamma_pdc': -0.004,
}


class PVSim:
    """ This PV Simulator calculates the output of a PV panel based on its parameters such as location, orientation,
        and rated power using the pvlib module.
        The output corresponds to the PV production in kilowatts, producers are assumed to have positive values."""
    system: PVSystem
    location: Location
    mc: ModelChain
    subscriber: Subscriber
    logger: Logger

    def __init__(self):
        self.system = PVSystem(module_parameters={'pdc0': _PV_SYS_CONFIG['pdc0'],
                                                  'gamma_pdc': _PV_SYS_CONFIG['gamma_pdc']},
                               inverter_parameters={'pdc0': _PV_SYS_CONFIG['pdc0']},
                               temperature_model_parameters=_TEMP_MODEL_PARAMS,
                               surface_tilt=_PV_SYS_CONFIG['surface_tilt'],
                               surface_azimuth=_PV_SYS_CONFIG['surface_azimuth'])
        self.location = Location(latitude=_PV_SYS_CONFIG['latitude'], longitude=_PV_SYS_CONFIG['longitude'])
        self.mc = ModelChain(self.system, self.location, aoi_model='physical', spectral_model='no_loss')

        self.logger = Logger(_LOG_FILEPATH)

        self.subscriber = Subscriber(callback_ctrl=self._on_new_meter_ctrl, callback_data=self._on_new_meter_data)

    def run(self):
        self.logger.writerow(('Datetime', 'Pac_HH[kW]', 'Pac_PV[kW]', 'Pac_sum[kW]'))
        self.subscriber.run()

    def get_pac_kw(self, times: pd.DatetimeIndex):
        weather = self.location.get_clearsky(times=times)
        self.mc.run_model(weather)
        return self.mc.ac / 1e3

    def _on_new_meter_data(self, timestamp, meter_pac_kw):
        times = pd.date_range(start=timestamp, end=timestamp, tz=_PV_SYS_CONFIG['timezone'])
        pv_pac_kw = self.get_pac_kw(times).values[0]
        sum_pac_kw = meter_pac_kw + pv_pac_kw
        data = (timestamp, meter_pac_kw, pv_pac_kw, sum_pac_kw)
        # print(data)
        self.logger.writerow(data)

    def _on_new_meter_ctrl(self, msg):
        # print(msg)
        if msg == "done":
            self._cleanup()

    def _cleanup(self):
        self.subscriber.close()
        self.logger.close()
        self._plot_results_to_file()

    def _plot_results_to_file(self):
        df = pd.read_csv(_LOG_FILEPATH, index_col=0)

        df.plot()
        plt.xlabel('Zeit')
        plt.ylabel('Leistung in kW')
        plt.setp(plt.xticks()[1], rotation=30, ha='right')
        plt.grid()
        plt.subplots_adjust(left=0.2, bottom=0.25)
        plt.savefig(f'{_RESULTS_DIR_PATH}/plot.png', dpi=150)


if __name__ == '__main__':
    times = pd.date_range("20190629 000000", "20190629 235959", freq="5s")
    pv_sim = PVSim()
    res_arr = pv_sim.get_pac_kw(times)
    res_df = DataFrame(res_arr, columns=['Pac[kW]'], index=times)
    print(res_df)
    res_df.plot()
    plt.show()
