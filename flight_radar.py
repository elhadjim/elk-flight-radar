import time
import json
import schedule
# from geopy.geocoders import Nominatim
from FlightRadar24.api import FlightRadar24API
LOG_FILE_PATH = "/mnt/c/Users/elhad/OneDrive/Bureau/curious/observability/log/flight_radar/flight_radar.log"


# geolocator = Nominatim(user_agent="my-app")

def fetch_flight_data():
    fr_api = FlightRadar24API()
    
    # Vous pouvez modifier les paramètres de recherche selon vos besoins
    flights = fr_api.get_flights()
    flight_data_list = []
    airports = fr_api.get_airports()
    airport_dict = {}
    for airport in airports:
        airport_iata = airport.iata
        airport_dict[airport_iata] = {'name':airport.name, 'country':airport.country}
    for flight in flights:
        # try:
        #     location_address = geolocator.reverse((flight.latitude,flight.longitude)).raw['address']
        # except Exception as e:
        #     location_address = {}
        # origin_airport = airport_dict.get(flight.origin_airport_iata,flight.origin_airport_iata)
        destination_info = airport_dict.get(flight.destination_airport_iata, {})
        destination_name = destination_info.get("name", flight.destination_airport_iata)
        origin_info = airport_dict.get(flight.origin_airport_iata, {})
        origin_name = origin_info.get("name", flight.origin_airport_iata)
        flight_data = {
            'id': flight.id,
            'aircraft_code': flight.aircraft_code,
            'airline_iata': flight.airline_iata,
            'airline_icao': flight.airline_icao,
            'callsign': flight.callsign,
            'origin': origin_name,
            'destination': destination_name,
            'latitude': flight.latitude,
            'longitude': flight.longitude,
            'altitude': flight.altitude,
            'speed': flight.ground_speed,
            'heading': flight.heading,
            'timestamp': flight.time,
            'location': {
                'lat': flight.latitude,
                'lon': flight.longitude
            }
            #'location_country': location_address.get('country', ''),
            #'location_city': location_address.get('city', '')
            
        }
        flight_data_list.append(flight_data)

    with open(LOG_FILE_PATH, "a") as log_file:
        for entry in flight_data_list:
            log_file.write(json.dumps(entry) + "\n")

    print(f"Data written to log file: {LOG_FILE_PATH}")

schedule.every(5).minutes.do(fetch_flight_data)

fetch_flight_data()

while True:
    schedule.run_pending()
    time.sleep(1)
