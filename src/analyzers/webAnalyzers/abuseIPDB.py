from src.analyzers.classes import WebAnalyzer
import requests
import json


class AbuseIPDB(WebAnalyzer):

    def run(self, ioc, type):
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
            response = requests.request(method='GET', url=url, headers=headers, params=querystring)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None 

