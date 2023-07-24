import json
import consts
import requests
import os

def check_type(type: str):
    for investigation_type in consts.investigation_types:
        if type == investigation_type["value"]:
            return True
    return False 

def get_analyzers(type: str):
    analyzers = []
    with open("../src/configurations/analyzers.json") as jsonFile:
        analyzers_configuration = json.load(jsonFile)
        for analyzer_name, configuration in analyzers_configuration.items():
            if type in configuration["type"]:
                analyzers.append(analyzer_name)
        jsonFile.close()
    return analyzers



def encode(type, data):
    ENCODING_URL = os.getenv('ENCODING_URL', default="http://localhost:8081")
    try:
        URL = ""
        if type == "sdo":
            URL = f"{ENCODING_URL}/generate_sdo"
        elif type == "sro":
            URL = f"{ENCODING_URL}/generate_sro"
        elif type == "sco":
            URL = f"{ENCODING_URL}/generate_sco"
        else:
            raise Exception("provide the type of encoding!")
        resp = requests.post(
            url=URL,
            json=data
        )
        resp.raise_for_status()
        stix_obj = resp.json()
        return stix_obj
    except Exception as e:
        print(f"An exception occurred while encoding \n error: {str(e)}")
        return None
    

def add_report(client, report):
    ioc_report_str = json.dumps(report)
    data = json.loads(ioc_report_str)
    result = client.index("reports").search(report["ioc"])

    if len(result["hits"]) == 0:
        print(f"Addding document!")
        c = client.index("reports").add_documents(data)

    else:
        print(f"Updating document!")
        report_id = result["hits"][0]["id"]
        client.index('reports').delete_document(report_id)
        client.index("reports").add_documents(data)
