from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "LON"

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()

if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    data_manager.destination_data = flight_search.get_iata_code(city_names)
    data_manager.put_iata_codes()
    sheet_data = data_manager.get_destination_data()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination_code in destinations:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination_code,
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight is None:
        continue

    if flight.price < destinations[destination_code]["price"]:
        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to" \
                  f" {flight.destination_city}-{flight.destination_airport}, from {flight.out_date}" \
                  f" to {flight.return_date}."

        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            print(message)

        print(message)
        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
        notification_manager.send_emails(message, link)
        # notification_manager.send_message(message)
