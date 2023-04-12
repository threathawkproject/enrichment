from analyzers.classes import WebAnalyzer
import json
import base64
import requests


class VirusTotal(WebAnalyzer):

    def run(self, ioc, type, node_id = None):
        # Housekeeping
        self._ioc = ioc
        self._type = type

        # Load the API key
        with open("../src/configurations/analyzers.json") as jsonFile:
            configurations = json.load(jsonFile)
            jsonFile.close()
        self._key = configurations["virusTotal"]["key"]

        # Determine which endpoint to use
        if type == "file":
            return "File received"

        elif type == "hash":
            # Set the endpoint URL
            url = "https://www.virustotal.com/api/v3/files/" + ioc

        elif type == "url":
            # Generate a valid URL identifier for the URL
            url_id = base64.urlsafe_b64encode(ioc.encode()).decode().strip("=")

            # Set the endpoint URL
            url = "https://www.virustotal.com/api/v3/urls/" + url_id

        elif type == "domain":
            # Set the endpoint URL
            url = "https://www.virustotal.com/api/v3/domains/" + ioc

        elif type == "ip":
            # Set the endpoint URL
            url = "https://www.virustotal.com/api/v3/ip_addresses/" + ioc

        else:
            url = "NULL"

        # Create the headers
        headers = {"accept": "application/json", "x-apikey": self.key}

        # Send the request
        try:
            response = requests.request(
                method="GET", url=url, headers=headers)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"Error: {e}")
            return None
