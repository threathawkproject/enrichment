import geoip2.webservice
from src.analyzers.classes import WebAnalyzer


class GeoIP2(WebAnalyzer):

    def run(self, ioc, type):
        self._ioc = ioc
        with geoip2.webservice.Client(771503, 'fKh4TiE6RFjEKDo9', host='geolite.info') as client:
            # You can also use `client.city` or `client.insights`
            # `client.insights` is not available to GeoLite2 users
            response = client.country(self._ioc)

            return response.raw
