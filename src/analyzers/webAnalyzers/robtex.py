import requests
from analyzers.classes import WebAnalyzer


class Robtex(WebAnalyzer):

    def run(self, ioc, type, node_id = None):
        print(ioc)
        self._ioc = ioc
        baseUrl = "https://freeapi.robtex.com/ipquery"
        try:
            url = f"{baseUrl}/{self._ioc}"
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()
            print(data)
            return data
        except Exception as e:
            return None
