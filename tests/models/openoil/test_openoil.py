import pyproj
import numpy as np
from datetime import datetime, timedelta

from opendrift.models.openoil import OpenOil
from opendrift.readers import reader_ArtificialOceanEddy


def test_seed():
    """Test seeding"""
    o = OpenOil()
    fake_eddy = reader_ArtificialOceanEddy.Reader(2, 62)
    fake_eddy.start_time = datetime(2015, 1, 1)
    o.add_reader([fake_eddy])
    o.seed_elements(lon=4, lat=60, number=100, time=fake_eddy.start_time)
    assert len(o.elements) == 0
    assert len(o.elements_deactivated) == 0
    assert len(o.elements_scheduled) == 100


def test_oil_in_ice():
    """ Testing ice-in-oil transport with
    different values of sea ice concentration as defined by Nordam et al. 2019"""

    c = [0.2, 0.5, 0.8]
    lon = 24
    lat = 81

    # Distances calculated with fallback_values and Nordam's equation
    distances = {'0.2': 21.2914, '0.5': 15.1405, '0.8': 7.2}

    geod = pyproj.Geod(ellps='WGS84')

    for i in c:
        o = OpenOil(loglevel=50)
        o.set_config('environment:fallback:x_wind', 0)  # zonal wind
        o.set_config('environment:fallback:y_wind', 4)  # meridional wind

        o.set_config('environment:fallback:x_sea_water_velocity',
                     0)  # eastward current
        o.set_config('environment:fallback:y_sea_water_velocity',
                     .4)  # meridional current

        o.set_config('environment:fallback:sea_ice_x_velocity',
                     0)  # zonal ice velocity
        o.set_config('environment:fallback:sea_ice_y_velocity',
                     .2)  # meridional ice velocity

        o.set_config(
            'environment:fallback:sea_surface_wave_stokes_drift_y_velocity',
            0.1)  # meridional Stokes drif

        o.set_config('processes:dispersion', False)
        o.set_config('processes:evaporation', False)
        o.set_config('processes:emulsification', False)
        o.set_config('drift:stokes_drift', True)
        o.set_config('processes:update_oilfilm_thickness', False)
        o.set_config('drift:current_uncertainty', 0)
        o.set_config('drift:wind_uncertainty', 0)

        o.set_config('environment:fallback:sea_ice_area_fraction', i)

        o.seed_elements(lon,
                        lat,
                        radius=1,
                        number=10,
                        time=datetime.now(),
                        wind_drift_factor=0.03)

        o.run(duration=timedelta(hours=10))

        latf = o.history['lat'][0][-1]
        lonf = o.history['lon'][0][-1]

        _azimuth1, _azimuth2, dist = geod.inv(lon, lat, lonf, latf)

        np.testing.assert_almost_equal(distances[str(i)], dist / 1000, 2)

def test_default_oil_type():
    o = OpenOil(loglevel=50)
    print('Default oil_type', o.get_config('seed:oil_type'))

    assert o.get_config('seed:oil_type') == 'GENERIC BUNKER C'

def test_set_oil_type():
    o = OpenOil(loglevel=50)
    o.set_oiltype('AASGARD A 2003')
    assert o.oiltype.name == 'AASGARD A 2003'
    print(o.oiltype)

def test_set_oil_type_by_id():
    o = OpenOil(loglevel=50)
    o.set_oiltype_by_id('NO00108')
    assert o.oiltype.name == 'AASGARD A 2003'
    print(o.oiltype)



