import json


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
