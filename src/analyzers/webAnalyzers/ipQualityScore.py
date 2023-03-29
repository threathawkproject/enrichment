import json
import requests
from analyzers.classes import WebAnalyzer


class IPQualityScore(WebAnalyzer):
    def run(self, ioc, type):
        # Housekeeping
        self._ioc = ioc
        self._type = type

        if type == "ip":
            # Load the API key
            with open("../src/configurations/analyzers.json") as jsonFile:
                configurations = json.load(jsonFile)
                jsonFile.close()
                self._key = configurations["ipQualityScore"]["key"]

            # Set the endpoint URL
            # We're using the URL that returns JSON data
            url = f"https://ipqualityscore.com/api/json/ip/{self.key}/{ioc}/"

            # Create the headers
            # These are specified in the API documentation
            headers = {
                "allow_public_access_points": "true",
                "mobile": "true",
                "fast": "true",
                "strictness": "0",
                "lighter_penalties": "true"
            }

            # Send the request
            try:
                response = requests.request(
                    method="GET", url=url, headers=headers)
                response.raise_for_status()
                print(response.json())
                return response.json()

            except Exception as e:
                print(f"Error: {e}")
                return None

        else:
            return None
