import ephem
import datetime
import math


class Satellite():
    """Generic satellite class"""

    def __init__(self, tle_list):
        self.name = tle_list[0][2:]
        self.tle_1 = tle_list[1]
        self.tle_2 = tle_list[2]

    def _calculate_current_position(self):
        """Assigns the current position"""
        try:
            self.ephem_satellite = ephem.readtle(self.name, self.tle_1, self.tle_2)
            self.ephem_satellite.compute(datetime.datetime.utcnow())
            self.lat = math.degrees(self.ephem_satellite.sublat)
            self.lng = math.degrees(self.ephem_satellite.sublong)
            self.alt = self.ephem_satellite.elevation
            return True
        except RuntimeError:
            return False
    
    def _get_haversine_distance(self, obs_lat, obs_lng):
        earth_radius = 6373.0
        obs_lat = math.radians(obs_lat)
        obs_lng = math.radians(obs_lng)
        sat_lat = math.radians(self.lat)
        sat_lng = math.radians(self.lng)
        delta_lat = obs_lat - sat_lat
        delta_lng = obs_lng - sat_lng
        a = math.sin(delta_lat / 2)**2 + math.cos(sat_lat) * math.cos(obs_lat) * math.sin(delta_lng / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return float(earth_radius * c)

    def serialize_if_is_in_radius(self, lat, lng, radius_km):
        """Serializes the object if it falls within the radius"""
        if self._calculate_current_position():
            obs_distance = self._get_haversine_distance(lat, lng)
            if obs_distance < radius_km:
                sat_dict = self._get_serialized_dict()
                sat_dict['observerDistance'] = round(obs_distance, 3)
                return sat_dict
        return False

    def _get_serialized_dict(self):
        """Returns the serialized dict"""
        return {
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
            'alt': int(self.alt),
            'isDebris': self.is_debris(),
        }

    def is_debris(self):
        """Returns if the satellite is debris"""
        return self.name.endswith(' DEB')

    def is_valid(self):
        """Determine if the satellite object is valid from the TLE"""
        try:
            if self._calculate_current_position():
                return True
            return False
        except Exception:
            return False

    def serialize(self):
        """Returns a serialized dict of the satellite's current position"""
        if self._calculate_current_position():
            return self._get_serialized_dict()
        return False

    def print_position(self):
        """Prints the position to stdout"""
        out = self.name + ': ' + str(self.lat) + ' °N, ' + str(self.lng) + ' °E'
        print(out)
