import os
import time
from satellite import Satellite
from spacetrack import SpaceTrackApi
import storage


satellites = []
last_updated = []


def get_overhead_satellites_dicts(lat, lng, radius):
    """Returns the list of overhead satellite objects given the window"""
    overhead_satellites_dict = []
    for sat in satellites:
        try:
            sat_dict = sat.serialize_if_is_in_radius(lat, lng, radius)
        except Exception:
            continue
        if sat_dict:
            overhead_satellites_dict.append(sat_dict)
    return overhead_satellites_dict


def get_constellation(startswith):
    """Returns satellites of a certain constellation"""
    constellation = []
    for sat in satellites:
        if sat.name.startswith(startswith):
            serialized = sat.serialize()
            if serialized:
                constellation.append(serialized)
    return constellation


def get_tle(sat_id):
    """Return the TLE from sat_id"""
    for sat in satellites:
        if sat.name == sat_id:
            return sat.tle
    return None


def populate_satellites_array():
    """Populates the satellites array from TLEs"""
    total_tles = 0
    tles = storage.get_tles_from_cache()
    metadata = storage.get_metadata()
    last_updated.append(metadata.get('last_updated'))
    if len(last_updated) > 1:
        del last_updated[0] 
    if not tles:
        print('Fetching from spacetrack')
        cron_refresh_spacetrack_cache()
        tles = storage.get_tles_from_cache()
    for tle in tles:
        total_tles += 1
        s = Satellite(tle)
        if s.is_valid():
            satellites.append(s)
    print('Loaded {} of {} satellites'.format(len(satellites), total_tles))


def cron_refresh_spacetrack_cache():
    """Refreshes the cache from space-track daily"""
    s = SpaceTrackApi()
    updated_tles_str = s.get_all_tles()
    storage.save_tle_cache(updated_tles_str)
    last_updated[0] = int(time.time())
    metadata = {
        'last_updated': last_updated[0],
    }
    storage.save_metadata(metadata)


def announce_satellite(sat):
    """Announces the satellite"""
    if sat['isDebris']:
        return
    name = sat['name']
    altitude = int(float(sat['alt']) / 1000)
    distance = int(sat['observerDistance'])
    sentence = '{name} is overhead, {distance} kilometers from you at an altitude of {altitude} kilometers'.format(
        **locals()
    )
    cmd = 'say "{}"'.format(sentence)
    os.system(cmd)


def main():
    """Entrypoint for the application"""
    populate_satellites_array()
    latitude = float(os.environ['LATITUDE'])
    longitude = float(os.environ['LONGITUDE'])
    radius = int(os.environ['RADIUS'])
    timeout = 1
    previous_satellites = []
    while True:
        if (last_updated[0] + 86400) < int(time.time()):
            print('Expired data, updating from spacetrack')
            cron_refresh_spacetrack_cache()
            populate_satellites_array()
        print('Checking {}, {}'.format(latitude, longitude))
        currently_overhead = get_overhead_satellites_dicts(latitude, longitude, radius)
        for sat in currently_overhead:
            if not sat['name'] in previous_satellites:
                announce_satellite(sat)
        previous_satellites = [x['name'] for x in currently_overhead]
        time.sleep(timeout)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')
