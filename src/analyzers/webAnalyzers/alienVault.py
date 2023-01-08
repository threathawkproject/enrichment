from analyzers.classes import WebAnalyzer
from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes
import json


class AlienVault(WebAnalyzer):

    def run(self, ioc, type):
        # Housekeeping
        self._ioc = ioc
        self._type = type

        # Load the API key
        with open("../src/configurations/analyzers.json") as jsonFile:
            configurations = json.load(jsonFile)
            jsonFile.close()
        self._key = configurations["alienVault"]["key"]
        otx = OTXv2(self._key)

        # Determine which indicator type to use
        if type == "file":
            pass

        # File hashes
        elif type == "sha1":
            indicatorType = IndicatorTypes.FILE_HASH_SHA1

        elif type == "sha256":
            indicatorType = IndicatorTypes.FILE_HASH_SHA256

        elif type == "md5":
            indicatorType = IndicatorTypes.FILE_HASH_MD5

        elif type == "url":
            indicatorType = IndicatorTypes.URL

        elif type == "domain":
            indicatorType = IndicatorTypes.DOMAIN

        elif type == "ip":
            indicatorType = IndicatorTypes.IPv4

        else:
            pass

        # response = otx.get_indicator_details_full(
        #    indicator_type=indicatorType, indicator=ioc)

        response = otx.get_indicator_details_by_section(
            indicator_type=indicatorType, indicator=ioc, section="general")

        return response
