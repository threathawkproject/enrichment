from honeydb import api
from analyzers.classes import WebAnalyzer

class HoneyDB(WebAnalyzer):

    def run(self, ioc):
        self._ioc = ioc
        honeydb = api.Client("2a7247b71a923763bb17dbf0185320742a972f64e5757ef9c0d5fe9918e4ec7c", "d72b1b4ff45ab4ba4284f62d6190963fbb88f2578974f02a5e7b6dbf0c24ee6d")
        try:
            twitter = honeydb.twitter_threat_feed(ipaddress=ioc)
            return twitter
        except Exception as e:
            print(e)
            return None