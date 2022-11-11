import requests
import logging

from getpass import getpass


logging.basicConfig(level=logging.INFO)


def get_current_moisture(location: str) -> int:
    """
    Makes GET request to weatherstack API and returns the current moisture %
    https://weatherstack.com/documentation

    Parameters:
        location (str) : The location we want weather data for

    Returns:
        (int) : Humidity level % for the provided location
    """
    weatherstack_api_key = getpass("Weatherstack api key: ")
    try:
        weather_details = requests.get(f"http://api.weatherstack.com/current?access_key={weatherstack_api_key}&query={location}")
        weather_details.raise_for_status()

        weather_details = weather_details.json()
        if not weather_details.get("success", True):
            error_message = f"something's fucked: {weather_details}"
            logging.error(error_message)
            raise requests.exceptions.HTTPError(error_message)

    except requests.exceptions.HTTPError as e:
        logging.error("Request to weatherstack failed")
        raise e

    current_moisture = int(weather_details['current']['humidity'])

    logging.info(f"Current moisture levels in {location} are {current_moisture}%")

    return current_moisture