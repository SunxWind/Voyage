import datetime


daly_forcast = {'app_max_temp': 20.8, 'app_min_temp': 13, 'clouds': 23, 'clouds_hi': 9, 'clouds_low': 45,
                'clouds_mid': 32, 'datetime': datetime.datetime(2025, 1, 22, 0, 0),
                'dewpt': 11.9, 'high_temp': 21.3, 'low_temp': 12.4, 'max_temp': 21.3, 'min_temp': 13, 'moon_phase': 0.36,
                'moon_phase_lunation': 0.78, 'moonrise_ts': 1737501932, 'moonset_ts': 1737540171, 'ozone': 312,
                'pop': 10, 'precip': 0.3474121, 'pres': 1016, 'rh': 74, 'slp': 1020, 'snow': 0, 'snow_depth': 0,
                'sunrise_ts': 1737521676, 'sunset_ts': 1737559784, 'temp': 16.9,
                'timestamp_local': datetime.datetime(2025, 1, 22, 0, 0),
                'timestamp_utc': datetime.datetime(2025, 1, 22, 0, 0),
                'uv': 2, 'vis': 24, 'weather': {'description': 'Scattered clouds', 'code': 802, 'icon': 'c02d'},
                'wind_dir': 277, 'wind_gust_spd': 5.3, 'wind_spd': 2}

forcast_mock = []

for day in range(16):
    forcast_mock.append(daly_forcast)
