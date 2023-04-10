from analyzers.classes import WebAnalyzer
from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes
import json

from src.utils import encode

class AlienVault(WebAnalyzer):

    def make_relationship(self, data, source_id):
        sdo = json.loads(data)
        target_id = sdo["id"]
        relationship_data = {
            "source": source_id,
            "target": target_id,
            "rel_type": "indicates"
        }
        print(relationship_data)
        relationship = encode("sro", relationship_data)
        return relationship
    

    def convert(self, data, node_id):
        pulse_info = data["pulse_info"]
        pulses = pulse_info["pulses"]
        encoded_data = []
        if len(pulses) > 0:
            for pulse in pulses:
                # getting the location
                for country in pulse["targeted_countries"]:
                    data = {
                        "name": country,
                        "country": country,
                        "latitude": 0,
                        "longitude": 0,
                    }
                    data_to_send = {
                        "type": "location",
                        "data": data
                    }
                    result = encode("sdo", data_to_send)
                    if result is not None:
                        encoded_data.append(result)
                        sro = self.make_relationship(result, node_id)
                        if sro is not None:
                            encoded_data.append(sro)
                        

                # storing the ttps!
                for attack_id in pulse["attack_ids"]:
                    name = attack_id["name"] 
                    tid = attack_id["id"]
                    description = attack_id["display_name"]
                    external_references=[
                        {
                            "source_name": "ATT&CK",
                            "external_id": tid
                        }
                    ]
                    data = {
                        "name":name,
                        "description": description,
                        "external_references": external_references
                    }
                    data_to_send = {
                        "type": "attack-pattern",
                        "data": data
                    }
                    result = encode("sdo", data_to_send)
                    if result is not None:
                        encoded_data.append(result)
                        sro = self.make_relationship(result, node_id)
                        if sro is not None:
                            encoded_data.append(sro)
        return encoded_data


    def run(self, ioc, type, node_id):
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
        data = self.convert(response, node_id)
        # data_to_send = {
        #     "data": data
        # }
        return data
