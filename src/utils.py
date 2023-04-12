import json
import consts
import requests

def encode(type, data):
    try:
        URL = ""
        if type == "sdo":
            URL = consts.ENCODING_SDO_URL
        elif type == "sro":
            URL = consts.ENCODING_SRO_URL
        elif type == "sco":
            URL = consts.ENCODING_SCO_URL
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
