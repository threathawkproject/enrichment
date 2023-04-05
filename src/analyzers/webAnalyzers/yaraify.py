import json
import requests
from analyzers.classes import WebAnalyzer


class YARAify(WebAnalyzer):
    def run(self, ioc, type):
        # Housekeeping
        self._ioc = ioc
        self._type = type

        if type == "file":
            # Set the endpoint URL
            url = "https://yaraify-api.abuse.ch/api/v1/"

            # Create the headers

        elif type == "hash":
            # Set the endpoint URL
            url = "https://yaraify-api.abuse.ch/api/v1/"

            # Create the headers
            headers = {
                "accept": "application/json"
            }

            # Create the payload
            data = {"query": "lookup_hash",
                    "search_term": f"{ioc}"}
            data = json.dumps(data)

            # Send the request
            try:
                response = requests.request(
                    method="POST", url=url, headers=headers, data=data)
                response.raise_for_status()
                return response.json()

            except Exception as e:
                print(e)
                return None

        else:
            return None
