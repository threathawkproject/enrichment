from analyzers.classes import WebAnalyzer
import requests
from src.utils import encode
import json
class AbuseIPDB(WebAnalyzer):

    def make_relationship(self, data, source_id):
        sdo = json.loads(data)
        target_id = sdo["id"]
        relationship_data = {
            "source": target_id,
            "target": source_id,
            "rel_type": "domain of"
        }
        relationship = encode("sro", relationship_data)
        return relationship

    def convert(self, data, node_id):
        encoded_data = []
        host_names = []
        domain = data["domain"]
        if domain != "" and domain is not None:
            host_names.append(domain)
        if data["hostnames"] is not None and len(data["hostnames"]) > 0:
            host_names.extend(data["hostnames"])
        for host_name in host_names:
            domain_name = {
                "value": host_name
            }
            data_to_send = {
                "type": "domain-name",
                "data": domain_name
            }
            result = encode("sco", data_to_send)
            if result is not None:
                encoded_data.append(json.loads(result))
                sro = self.make_relationship(result, node_id)
                if sro is not None:
                    encoded_data.append(json.loads(sro))
        return encoded_data

    def run(self, ioc, type, node_id):
        self._ioc = ioc
        self._type = type

        # Defining the api-endpoint
        url = 'https://api.abuseipdb.com/api/v2/check'
        querystring = {
            'ipAddress': ioc
        }

        headers = {
            'Accept': 'application/json',
            'Key': '02241dd0b2496a7dcc6ae14ec1791d8c4cb29cdc1ee5207ad82ab96cc4721a17b931a6420003a2a0'
        }
        try:
            response = requests.request(
                method='GET', url=url, headers=headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            abuse_ip_db_data = data["data"]
            encoded_data = self.convert(abuse_ip_db_data, node_id)
            return encoded_data
        except Exception as e:
            print(e)
            return None
