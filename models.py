"""
models.py

App Engine datastore models

"""
from math import radians, cos, sin, asin, sqrt
from google.appengine.ext import ndb
from cons import PLACE_TYPES, PLACE, EVENT
from ingest_engine.google_places_ingest import gpi
import random


class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    picture = ndb.StringProperty(required=True)
    seen_places = ndb.KeyProperty(repeated=True)
    seen_events = ndb.KeyProperty(repeated=True)
    favourite_places = ndb.KeyProperty(repeated=True)
    favourite_events = ndb.KeyProperty(repeated=True)

    @classmethod
    def get(cls, email=None):
        results = cls.query(cls.email == email)
        result = results.get()
        if result:
            return result
        else:
            return False


class BaseModel(ndb.Model):

    @classmethod
    def haversine(cls, coordinate_pair1, coordinate_pair2, radius):
        '''
        Check if 2 coordinates are within a given radius distance
        :param coordinate_pair1: (lat, long)
        :param coordinate_pair2: (lat, long)
        :param radius: In km
        :return: true/false
        '''
        lat1, lat2 = map(radians, [float(coordinate_pair1[0]), float(coordinate_pair2[0])])
        lon1, lon2 = map(radians, [float(coordinate_pair1[1]), float(coordinate_pair2[1])])

        # haversine formula
        distance_lat = lat2 - lat1
        distance_lon = lon2 - lon1
        a = sin(distance_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(distance_lon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers
        value = c * r
        return value <= radius  # If true, it's within the area

    @classmethod
    def geopt_to_tuple(cls, coordinates):
        '''
        Converts NDB coordinates type to tuple of (lat, long)
        :param coordinates: NDB coordinates type value
        :return: (lat, long)
        '''
        return (coordinates.lat, coordinates.lon)


class Place(BaseModel):
    '''
    String property has a 1500 character limit (1500 bytes)
    '''
    name = ndb.StringProperty(required=True)
    place_type = ndb.StringProperty(required=True)
    coordinates = ndb.GeoPtProperty(required=True)
    address = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    country = ndb.StringProperty(required=True)
    maps_url = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    description = ndb.StringProperty()
    # Consists of list of DailyHours entities
    open_hours = ndb.JsonProperty()
    average_rating = ndb.FloatProperty()
    tags = ndb.TextProperty(repeated=True)
    url = ndb.StringProperty()
    twitter = ndb.StringProperty()
    facebook = ndb.StringProperty()
    photos = ndb.StringProperty(repeated=True)
    analysed = ndb.BooleanProperty(required=True, default=False)

    @classmethod
    def get(cls, place_type, user_coordinates, radius, city, seen_ids=None,
                  vegan_friendly=False, vegetarian_friendly=False, halal=False):
        '''
        Randomizes the selection of an available place
        :param place_type: from PLACE_TYPES in cons.py
        :param user_coordinates: (lat, long)
        :param radius: radius in km
        :param city:
        :param seen_ids: The ids of places seen by the user already
        :param vegan_friendly: Boolean
        :param vegetarian_friendly: Boolean
        :param halal: Boolean
        :return: One random place of the passed type, if none found, returns False
        '''
        valid_keys = []

        results = cls.query(cls.place_type == place_type, cls.city == city)

        if place_type in PLACE_TYPES.RESTAURANT:
            results = results.filter(cls.halal == halal)

        if place_type in [PLACE_TYPES.RESTAURANT, PLACE_TYPES.CAFE]:
            results = results.filter(cls.vegan_friendly == vegan_friendly)
            results = results.filter(cls.vegetarian_friendly == vegetarian_friendly)

        results = results.fetch(projection=[cls.coordinates])
        # results = results.fetch(limit=10, projection=[cls.coordinates])
        if results:
            for result in results:
                # Check if place coordinates and user coordinates are within 5km of eachother (nearby search)
                coordinates = result.coordinates
                coordinates = cls.geopt_to_tuple(coordinates)
                if cls.haversine(coordinates, user_coordinates, radius):
                    valid_keys.append(result.key)

            if valid_keys:
                random_key = random.sample(valid_keys, 1)
                random_place = random_key[0].get().to_dict()

            else:
                return False

            dict_result = {
                PLACE.ID: [random_key[0].urlsafe()],
                PLACE.NAME: random_place[PLACE.NAME],
                PLACE.COORDINATES: cls.geopt_to_tuple(random_place[PLACE.COORDINATES]),
                PLACE.ADDRESS: random_place[PLACE.ADDRESS],
                PLACE.CITY: random_place[PLACE.CITY],
                PLACE.COUNTRY: random_place[PLACE.COUNTRY],
                PLACE.PHONE_NUMBER: random_place[PLACE.PHONE_NUMBER],
                PLACE.ANALYSED: random_place[PLACE.ANALYSED]
            }

            # Extra place information which is not mandatory
            if random_place[PLACE.PHONE_NUMBER]:
                dict_result[PLACE.PHONE_NUMBER] = random_place[PLACE.PHONE_NUMBER]

            if random_place[PLACE.MAPS_URL]:
                dict_result[PLACE.MAPS_URL] = random_place[PLACE.MAPS_URL]

            if random_place[PLACE.DESCRIPTION]:
                dict_result[PLACE.DESCRIPTION] = random_place[PLACE.DESCRIPTION]

            if random_place[PLACE.AVERAGE_RATING]:
                dict_result[PLACE.AVERAGE_RATING] = random_place[PLACE.AVERAGE_RATING]

            if random_place[PLACE.TAGS]:
                if not random_place[PLACE.ANALYSED]:  # If not analysed yet by watson API
                    text = " ".join(random_place[PLACE.TAGS])
                    try:
                        if text:
                            dict_result[PLACE.TAGS] = gpi.get_text_information(text, 0.6)
                            dict_result[PLACE.ANALYSED] = True
                    except:
                        dict_result[PLACE.TAGS] = random_place[PLACE.TAGS]
                        dict_result[PLACE.ANALYSED] = False
                else:
                    dict_result[PLACE.TAGS] = random_place[PLACE.TAGS]
                    dict_result[PLACE.ANALYSED] = False

            if random_place[PLACE.URL]:
                dict_result[PLACE.URL] = random_place[PLACE.URL]

            if random_place[PLACE.OPEN_HOURS]:
                dict_result[PLACE.OPEN_HOURS] = random_place[PLACE.OPEN_HOURS]

            if random_place[PLACE.FACEBOOK]:
                dict_result[PLACE.FACEBOOK] = random_place[PLACE.FACEBOOK]

            if random_place[PLACE.TWITTER]:
                dict_result[PLACE.TWITTER] = random_place[PLACE.TWITTER]

            return dict_result

        return False


class EatingPlace(Place):
    vegan_friendly = ndb.BooleanProperty(required=True)
    vegetarian_friendly = ndb.BooleanProperty(required=True)
    halal = ndb.BooleanProperty(required=True)


class Event(BaseModel):
    url = ndb.StringProperty()
    name = ndb.StringProperty(required=True)
    description = ndb.TextProperty()
    start = ndb.StringProperty(required=True)
    end = ndb.StringProperty()
    venue_name = ndb.StringProperty()
    venue_url = ndb.StringProperty()
    city = ndb.StringProperty(required=True)
    region = ndb.StringProperty()
    country = ndb.StringProperty(required=True)
    coordinates = ndb.GeoPtProperty(required=True)

    @classmethod
    def get(cls, city, user_coordinates, radius):
        '''
        :param city: city searching for events in
        :param user_coordinates: (lat, long) of user
        :param radius:
        :return: Random event dict, or false if no results
        '''
        valid_keys = []
        results = cls.query(cls.city == city)

        results = results.fetch(projection=[cls.coordinates])

        if results:
            for result in results:
                # Check if place coordinates and user coordinates are within given radius of eachother (nearby search)
                coordinates = result.coordinates
                coordinates = cls.geopt_to_tuple(coordinates)
                if cls.haversine(coordinates, user_coordinates, radius):
                    valid_keys.append(result.key)

            if valid_keys:
                random_key = random.sample(valid_keys, 1)
                random_event = random_key[0].get().to_dict()

            else:
                return False

            random_event[EVENT.ID] = [random_key[0].urlsafe()]
            return random_event

        else:
            return False


    
    




