# This will start as a CLI based program that will evolve to a frontend where the user can interact with a Leaflet map and import data there.
# More evolvement will follow when bulk search is enabled. Point a CSV to the program and it will make an API call and import location data.

# Menu for starters.
import json
import shlex
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from functions import * 


# Main.
def main():
    # Load the JSON file when the program starts.
    with open("mcc-mnc-networks-2026-09-21.json", "r", encoding="utf-8") as file:
        data = json.load(file)


    # Base URL for the API endpoint.
    base_url = "https://opencellid.org/cell/get"

    # API-key to OpenCellID.
    load_dotenv()
    api_key = os.getenv("MY_API_KEY")

    while True:
        user_input = input("> ").strip()

        if not user_input:
            continue

        args = user_input.split()
        command = args[0]

        if command == "exit":
            print("Exiting the program.")
            break

        # **OPERATOR** Search for the operator based on the MCC and MNC. Format will be for example "operator 244 05"
        elif command == "operator":

            # Captures the command and arguments and turns them into variables.
            mcc = args[1]
            mnc = args[2]

            # Loop through the JSON and search for a record that has both the MCC and MNC. Ouptuts the country and operator.
            for record in data["data"]:
                if record["mcc"] == mcc and record["mnc"] == mnc:
                    print(f"Country: {record["country"]}\nOperator: {record["operator"]}")

        # **LOCATION** Makes an API call to OpenCellID and retrieves the location information based on the MCC, MNC, LAC/TAC and Cell ID.
        elif command == "location":

            # If the command includes a flag -i or --input-file the program reads the given file and uses the information to make several a request to the API endpoint.
            if args[1] == "-i" or args[1] == "--input-file":
                file = args[2]

                # Makes API requests in a bulk to the API endpoint.
                API_request_bulk(api_key,base_url,file)

            # If no flags are given the program runs in default.
            else:
                # Defining variables for the arguments given.
                mcc = args[1]
                mnc = args[2]
                lac = args[3]
                cellid = args[4]

                # Makes a single request to the API endpoint based on the user input.
                API_request_single(api_key,base_url,mcc,mnc,lac,cellid)

        # **HELP** See information about the commands.
        elif command == "help":
            print("Commands:\noperator <mcc> <mnc> -- Shows the country and the operator based on the given MCC and MNC.")
            print("location <mcc> <mnc> <lac/tac> <cell-id> -- Retrives the location information of the cell tower.")

if __name__=="__main__":
    main()