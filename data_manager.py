import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)

SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")


class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(SHEET_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def put_iata_codes(self):
        for city in self.destination_data:
            put_params = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(f"{SHEET_ENDPOINT}/{city['id']}", json=put_params)
