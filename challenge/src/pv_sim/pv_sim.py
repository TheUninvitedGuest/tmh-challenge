#!/usr/bin/env python3
import pandas as pd
from pandas import DataFrame
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
import pvlib
from pvlib.pvsystem import PVSystem, pvwatts_ac
from pvlib.location import Location
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']


PV_SYS_CONFIG = {
    'location': 'TMH Munich',
    'latitude': 48.120872,
    'longitude': 11.602498,
    'timezone': 'Etc/GMT-1',
    'surface_tilt': 55,
    'surface_azimuth': 190,
}

class PVSim:
    system: PVSystem
    location: Location
    mc: ModelChain

    def __init__(self):
        self.system = PVSystem(module_parameters={'pdc0': 4e3, 'gamma_pdc': -0.004},
                          inverter_parameters={'pdc0': 4e3},
                          temperature_model_parameters=temperature_model_parameters,
                          surface_tilt=PV_SYS_CONFIG['surface_tilt'],
                          surface_azimuth=PV_SYS_CONFIG['surface_azimuth'])
        self.location = Location(latitude=PV_SYS_CONFIG['latitude'], longitude=PV_SYS_CONFIG['longitude'])
        self.mc = ModelChain(self.system, self.location, aoi_model='physical', spectral_model='no_loss')

    def get_pac_kw(self, times: pd.DatetimeIndex):
        weather = self.location.get_clearsky(times=times)
        self.mc.run_model(weather)
        return self.mc.ac / 1e3


if __name__ == '__main__':
    # times = pd.date_range("20190629 000000", "20190629 235959", freq="5s")
    times = pd.date_range("20190629 000000", "20190629 235959", freq="5s")
    pv_sim = PVSim()
    res_arr= pv_sim.get_pac_kw(times)
    res_df = DataFrame(res_arr, columns=['Pac[kW]'], index=times)
    print(res_df)
    res_df.plot()
    plt.show()