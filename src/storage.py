import os
import json
import time

def get_cache_path():
    """Returns the path of the TLES cache file"""
    filename = 'spacetrack.3les'
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        filename)

def get_metadata_path():
    """Returns the path of the metadata storage service"""
    filename = 'metadata.json'
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        filename)

def save_tle_cache(tle_string):
    """Saves the tle cache to the filesystem"""
    print('Saving TLE cache')
    with open(get_cache_path(), 'w') as file:
        file.write(tle_string)

def get_tle_cache():
    """Loads the tle cache from the filesystem"""
    try:
        with open(get_cache_path(), 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None

def save_metadata(metadata):
    """Saves metadata to the filesystem"""
    print('Saving metadata')
    with open(get_metadata_path(), 'w') as file:
        file.write(json.dumps(metadata))

def get_metadata():
    """Loads metadata from the filesystem"""
    try:
        with open(get_metadata_path(), 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return {
            'last_updated': int(time.time())
        }

def get_tles_from_cache():
    """Returns list of TLEs from persistent cache"""
    cache_string = get_tle_cache()
    if not cache_string:
        return None
    tles = []
    tle = []
    for line in iter(cache_string.splitlines()):
        if len(tle) == 3:
            tles.append(tle)
            tle = []
        tle.append(line.strip())
    return tles
