import requests
from analyzers.classes import WebAnalyzer


class PhishTank(WebAnalyzer):
    def run(self, ioc, type, node_id = None):
        # Housekeeping
        self._ioc = ioc
        self._type = type

        if type == "url":
            # Set the endpoint URL
            url = "http: // checkurl.phishtank.com/checkurl/"

            # Create the paramters
            params = {"url": f"{ioc}",
                      "format": "json"}

            # Create the headers
            headers = {"accept": "application/json"}

            # Send the request
            try:
                response = requests.request(
                    method="POST", url=url, headers=headers, params=params)
                response.raise_for_status()
                return response.json()

            except Exception as e:
                print(e)
                return None

        else:
            return None
