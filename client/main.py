#!/usr/bin/env python3

from configparser import ConfigParser
from common.client import Client
import logging
import os


def convert_time_to_seconds(time_str):
    time_str = time_str.strip('"')
    minutes, seconds = time_str.split('m')
    seconds = seconds.rstrip('s')
    return int(minutes) * 60 + int(seconds)


def initialize_config():
    """ Parse env variables or config file to find program config params

    Function that search and parse program configuration parameters in the
    program environment variables first and the in a config file. 
    If at least one of the config parameters is not found a KeyError exception 
    is thrown. If a parameter could not be parsed, a ValueError is thrown. 
    If parsing succeeded, the function returns a ConfigParser object 
    with config parameters
    """

    config = ConfigParser(os.environ)
    # If config.ini does not exists original config object is not modified
    config.read("config/config.ini")

    config_params = {}
    try:
        config_params["id"] = int(os.getenv('ID', config["DEFAULT"]["CLI_ID"]))
        config_params["server_address"] = os.getenv('SERVER_ADDRESS', config["DEFAULT"]["SERVER_ADDRESS"])
        config_params["logging_level"] = os.getenv('LOGGING_LEVEL', config["DEFAULT"]["LOGGING_LEVEL"])
        config_params["lapse"] = convert_time_to_seconds(os.getenv('LAPSE', config["DEFAULT"]["LAPSE"]))
        config_params["period"] = convert_time_to_seconds(os.getenv('PERIOD', config["DEFAULT"]["PERIOD"]))
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    return config_params

def main():
    config_params = initialize_config()
    id = config_params["id"]
    logging_level = config_params["logging_level"]
    server_address = config_params["server_address"]
    lapse = config_params["lapse"]
    period = config_params["period"]

    initialize_log(logging_level)

    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug(f"action: config | result: success | client_id: {id} | "
                  f"server_address: {server_address} | loop_lapse: {lapse} | "
                  f"loop_period: {period} | log_level: {logging_level}")

    # Initialize server and start server loop
    client = Client(id, server_address, lapse, period)
    client.run()

def initialize_log(logging_level):
    """
    Python custom logging initialization

    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )


if __name__ == "__main__":
    main()
