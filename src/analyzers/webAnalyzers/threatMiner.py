from analyzers.classes import WebAnalyzer
import requests


class ThreatMiner(WebAnalyzer):

    def run(self, ioc, type, node_id = None):
        self._ioc = ioc
        self._type = type

        if self._type == "ip":
            base_url = "https://api.threatminer.org/v2/host.php"

        if self._type == "domain":
            base_url = "https://api.threatminer.org/v2/domain.php"

        try:
            url = f"{base_url}?q={ioc}&rt=2"
            response = requests.request(method='GET', url=url)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(e)
            return None
