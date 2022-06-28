import requests
from flight_data import FlightData
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv(override=True)

API_KEY = os.environ.get("API_KEY")
TEQUILA_ENDPOINT = os.environ.get("TEQUILA_ENDPOINT")


class FlightSearch:

    def __init__(self):
        self.city_codes = []

    def get_iata_code(self, city_names):
        print("get destinations codes triggered")
        query_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": API_KEY}
        for city in city_names:
            parameters = {"term": city, "location_types": "city"}
            response = requests.get(query_endpoint, params=parameters, headers=headers)
            results = response.json()["locations"]
            code = results[0]["code"]
            self.city_codes.append(code)
        return self.city_codes

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        print(f"Check flights triggered for {destination_city_code}")
        headers = {"apikey": API_KEY}
        parameters = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 30,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response = requests.get(
            f"{TEQUILA_ENDPOINT}/v2/search",
            params=parameters,
            headers=headers
        )

        try:
            data = response.json()["data"][0]
        except IndexError:
            parameters["max_stopovers"] = 1
            response = requests.get(
                f"{TEQUILA_ENDPOINT}/v2/search",
                params=parameters,
                headers=headers
            )
            try:
                data = response.json()["data"][0]
                pprint(data)
            except IndexError:
                return None
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                print(f"{flight_data.destination_city}: £{flight_data.price}")
                return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
